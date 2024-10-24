import os
import sys
import configargparse
import hera_utils


class parser:
    """Define a command line parser by extending the hera_utils one.
    Note: the configuration file(s) is implicitly shared with the hera_utils configuration files
    """

    def __init__(self, hera_utils_parser=None):

        self.parser = None

        if hera_utils_parser:
            print(
                "Warning: expected type of existing parser is ",
                type(configargparse.ArgParser()),
            )
            print("   Provide existing parser is of type:", type(hera_utils.parser))
            self.parser = hera_utils_parser
        else:
            self.parser = hera_utils.parser().get_parser()

        self.parser.add(
            "--k8s_config_file",
            help="Path to kubernetes configuration file. Default is the value of the KUBECONFIG environment variable.",
            type=str,
            default=os.environ.get("KUBECONFIG"),
        )

    @staticmethod
    def verify_args(args):
        """The parser was run and we want to assert the resulting args fulfill
        the configuration needs."""

        if not hasattr(args, "k8s_config_file") or args.k8s_config_file is None:
            print("hera_k8s_utils: K8s configuration file pathname not defined.")
            print("hera_k8s_utils: either try")
            print("   - setting the KUBECONFIG environment variable")
            print("   - setting the --k8s_config_file argument.")
            print("hera_k8s_utils: exiting.")
            sys.exit(1)

        if not os.path.exists(args.k8s_config_file):
            print("hera_k8s_utils: unfound kubeconfig file", args.k8s_config_file)
            print("hera_k8s_utils: exiting.")
            sys.exit(1)

    def parse_args(self):
        return self.parser.parse_args()

    def get_parser(self):
        return self.parser
