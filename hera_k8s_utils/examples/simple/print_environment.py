# Test, at HERA level, whether the environment is properly defined.
from hera.workflows import (
    script,
)


@script()
def print_environment():
    import os
    import json

    print("Hera on PaGoDa can run python scripts...")
    print(
        "Retrieve the python script environment variables: ",
        json.dumps(dict(os.environ), indent=4),
    )
    print("Done.")


if __name__ == "__main__":
    # A workflow that tests whether the defined environment is correct as
    # seen and used from within the Argo server engine (at Workflow runtime)
    from hera_k8s_utils import parser, num_exp_environment
    from hera.workflows import (
        Container,
        DAG,
        Task,
        Workflow,
    )

    # Load configuration, assert servers (k8s and argo) access and define the environment
    environment = num_exp_environment(parser().parse_args())

    with Workflow(generate_name="print-environment-", entrypoint="main") as w:
        cowsayprint = Container(
            name="cowsayprint",
            image="docker/whalesay",
            command=[
                "cowsay",
                "Print environment as seen from within the k8s cluster.",
            ],
        )
        with DAG(name="main"):
            t1 = Task(name="cowsayprint", template=cowsayprint)
            t2 = print_environment()
            t1 >> t2
    w.create()
