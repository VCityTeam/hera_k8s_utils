import os
import sys
from hera_k8s_utils import parser as hera_k8s_utils_parser


class parser:
    """Extend the default parser with the local needs"""

    def __init__(self):
        self.parser = hera_k8s_utils_parser().get_parser()

        # Add the locally defined parser extensions
        self.parser.add(
            "--k8s_configmap_name",
            help="Name of the k8s configuration map used by cluster admin to transmit cluster specific configurations.",
            type=str,
            default=os.environ.get("KUBECONFIGMAP"),
        )

    @staticmethod
    def verify_args(args):
        # Eventually assert that the local extension is satisfied
        if not hasattr(args, "k8s_config_file") or args.k8s_configmap_name is None:
            print("The optional name of the k8s configuration map (used by")
            print("cluster admin to transmit cluster specific configurations).")
            print("was not provided. When needed either try")
            print("  - setting the KUBECONFIGMAP environment variable")
            print("  - setting the --k8s_configmap_name argument")
            print("hera_k8s_utils: exiting.")
            sys.exit(1)

    def parse_args(self):
        parsed_args = self.parser.parse_args()
        parser.verify_args(parsed_args)
        return parsed_args

    def get_parser(self):
        return self.parser


if __name__ == "__main__":
    try:
        args = parser().parse_args()
        parser.verify_args(args)
    except:
        print("Unable to retrieve a complete configuration/args. Exiting.")
        sys.exit(1)
    print("Parsed configuration/args:", args)
    print("Configuration/args parsing is OK.")
