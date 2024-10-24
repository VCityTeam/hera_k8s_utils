import sys
from ..k8s_cluster import k8s_cluster as cluster
from ..parser import parser


def main():

    args = parser().parse_args()
    try:
        k8s_cluster = cluster(args)
    except:
        print(
            "hera_k8s_utils: k8s_cluster not properly configured for Hera usage. Exiting."
        )
        sys.exit(1)
    k8s_cluster.print_config()
    print("K8s cluster properly set for usage with Hera.")


if __name__ == "__main__":
    main()
