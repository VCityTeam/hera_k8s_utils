# Test, at HERA level, whether
# 1. a ConfigMap environment properly defines an HTTP_PROXY variable
# 2. that proxy is effective for installing a python package with pip (across
#    that proxy)

from hera.workflows import (
    ConfigMapEnvFrom,
    Parameter,
    script,
)


@script(
    env_from=[
        # Assumes the corresponding config map is defined at k8s level
        ConfigMapEnvFrom(
            name="{{inputs.parameters.config_map_name}}",
            optional=False,
        )
    ],
)
def assert_configmap_environment(
    # Config_map_name argument is only used by the @script decorator and is
    # present here only because Hera seems to require it
    config_map_name,
):
    import os
    import sys
    import json

    environment_variables = dict(os.environ)
    if "HTTPS_PROXY" in environment_variables:
        print("HTTPS_PROXY environment variable found and (probably) defined")
        print("in the ", config_map_name, " ConfigMap.")
        print("HTTPS_PROXY value: ", environment_variables["HTTPS_PROXY"])
    else:
        print("HTTPS_PROXY environment variable NOT found.")
        print(
            "Something went wrong when defining of accessing the ",
            config_map_name,
            " ConfigMap.",
        )
        print("List of retrieved environment variables: ")
        print(json.dumps(dict(os.environ), indent=4))
        sys.exit(1)
    print("Exiting.")


@script(
    env_from=[
        # Assumes the corresponding config map is defined at k8s level
        ConfigMapEnvFrom(
            name="{{inputs.parameters.config_map_name}}",
            optional=False,
        )
    ],
)
def list_mounted_partitions(
    # This script starts with the installation, with pip, of a python package
    # (the "psutil" package). When the ArgoWorflow server is behind a firewall,
    # this script will (most often/might) need a proxy for pip to be able to
    # reach PyPI package archive.
    config_map_name,
):
    import subprocess
    import sys

    # Installing a package with pip requires an http access to PyPi (by default)
    # which can be blocked by the cluster networking configuration and might
    # thus require the configuration of an http proxy server.
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    print("Psutil python package successfully installed.")
    import psutil

    print("List of mounted partitions (none required)", psutil.disk_partitions())
    print("Exiting")


if __name__ == "__main__":
    # A workflow that tests whether the defined environment is correct as
    # seen and used from within the Argo server engine (at Workflow runtime)
    from parser import parser
    from environment import environment
    from hera.workflows import (
        Container,
        DAG,
        Task,
        Workflow,
    )

    environment = environment(parser().parse_args())

    with Workflow(generate_name="config-map-for-pip-proxy-", entrypoint="main") as w:
        cowsayprint = Container(
            name="cowsayprint",
            image="docker/whalesay",
            command=[
                "cowsay",
                "Testing access to " + environment.cluster.configmap + " ConfigMap.",
            ],
        )
        with DAG(name="main"):
            t1 = Task(name="cowsayprint", template=cowsayprint)

            t2 = assert_configmap_environment(
                arguments=Parameter(
                    name="config_map_name",
                    value=environment.cluster.configmap,
                ),
            )
            t3 = list_mounted_partitions(
                arguments=[
                    Parameter(
                        name="config_map_name",
                        value=environment.cluster.configmap,
                    ),
                ],
            )
            t1 >> t2 >> t3
    w.create()
