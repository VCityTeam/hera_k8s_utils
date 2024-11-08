# A simple example<!-- omit from toc -->

This example is considered simple, because it makes no usage of its access to the k8s cluster.
The underlying `hera_k8s_utils` mechanism only asserts that the k8s cluster was properly designated and that access rights are correct.
It then prints the environment variables as seen from the cluster.

In order to run the following simple examples (as `hera_k8s_utils` module), first make sure you already [installed `hera_k8s_utils`](../README.md/##hera_utils-package-installation).
Then configure `hera_k8s_utils` for this example.
For example copy [this hera.config.tmpl file](./hera.config.tmpl) to the `hera.config` file

```bash
cd `git rev-parse --show-toplevel`/hera_k8s_utils/examples/simple
cp hera.config.tmpl hera.config
```

and customize that file to your argo server as well as the underlying k8s cluster and provide associated credentials.

Eventually assert that the provided configuration is coherent by running the following test modules

```bash
python -m hera_k8s_utils.tests.parser   # Assert the configuration is complete
python -m hera_k8s_utils.tests.check_k8s_server_availability
```

You can then run the simple example per se with

```bash
python -m hera_k8s_utils.examples.simple.print_environment
```

and use Argo UI to refer retrieve the logs that should display the environment variables.
