import sys
from ..parser import parser


def main():
    try:
        args = parser().parse_args()
    except:
        print("hera_k8s_utils: unable to retrieve configuration/args. Exiting.")
        sys.exit(1)
    print("Parsed configuration/args:", args)
    print("hera_k8s_utils: configuration/args parsing is OK.")


if __name__ == "__main__":
    main()
