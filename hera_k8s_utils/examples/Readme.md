# Tests and examples (of hera_utils)

- [Tests and examples (of hera\_utils)](#tests-and-examples-of-hera_utils)
  - [Using ConfigMaps](#using-configmaps)
  - [Print containers environment and assert volume claim mounting](#print-containers-environment-and-assert-volume-claim-mounting)

In order to run the following examples (as `hera_k8s_utils` module), make sure you already [installed `hera_k8s_utils`](../README.md/##hera_utils-package-installation).
Also notice that each example requires a specific `hera.config` configuration.

## Using ConfigMaps

The usage scenario assumes that the cluster administrator chose to set up an [http proxy server](https://stackoverflow.com/questions/7155529/how-does-http-proxy-work) thus constraining the containers (requiring http access) to configure that proxy.
In this `hera_k8s_utils` example, a container requires to dynamically [install a python package with the `pip` command](https://stackoverflow.com/questions/19080352/how-to-get-pip-to-work-behind-a-proxy-server).  
Let us further assume that the cluster administrator chose to transmit (to the cluster users) the URL of that proxy through a [ConfigMap (Configuration Mapping)](https://hera.readthedocs.io/en/stable/api/workflows/hera/?h=configmap#hera.workflows.ConfigMapEnvFrom).

First, let us temporarily take the role of the administrator, and manually define [this `define_http_proxy_configmap.yml` ad-hoc ConfigMap](./configmap_for_pip_proxy/define_http_proxy_configmap.yml) with e.g. the following commands

```bash
cd `git rev-parse --show-toplevel`/hera_k8s_utils/examples/configmap_for_pip_proxy
# Define cluster specific variables
kubectl -n argo apply -f define_http_proxy_configmap.yml
# Assert the configmap was properly created (note that the ConfigMap 
# name is defined within define_http_proxy_configmap.yml)
kubectl -n argo get configmaps hera-utils-proxy-environment -o yaml
```

Then proceed with configuring `hera_k8s_utils` for this example. For example copy [this hera.config.tmpl file](./configmap_for_pip_proxy/hera.config.tmpl) and customize/decline it for your argo server and the underlying k8s cluster and provide your credentials. Assert the configuration is still coherent by running the test modules

```bash
python -m hera_k8s_utils.tests.parser   # Assert the configuration is complete
python -m hera_k8s_utils.tests.check_k8s_server_availability
```

Then assert that the previously defined ConfigMap can be accessed from Workflow tasks with

```bash
python -m hera_k8s_utils.examples.configmap_for_pip_proxy.print_config_map
```

Eventually you can now make some usage (through the `pip install` command that recognizes the `HTTPS_PROXY` environment variable) of that ConfigMap values by running the following WorkFlow

```bash
python -m hera_k8s_utils.examples.configmap_for_pip_proxy.use_configmap_for_pip
```

## Print containers environment and assert volume claim mounting
FIXME
The second example requires

- a more specific `hera_utils` configuration (file) that defines a volume claim name. Refer to the [./environment_and_volumes/hera.config.tmpl](./environment_and_volumes/hera.config.tmpl) and compare it with the simplest [hera.config.tmpl](./hera.config.tmpl). Customize (define the `k8s_volume_claim_name` variable) the [./environment_and_volumes/hera.config.tmpl](./environment_and_volumes/hera.config.tmpl) and place the declined results in [./environment_and_volumes/hera.config](./environment_and_volumes/hera.config) file,
- using an [`environment_and_volumes/environment.py` script](./environment_and_volumes/environment.py) that defines a `mount path` for the `volume claim`,
- using a [`environment_and_volumes/parse_arguments.py` script](./environment_and_volumes/parse_arguments.py) in order to customize the configuration parser.

```bash
cd `git rev-parse --show-toplevel`/examples
python environment_and_volumes/print_environment.py
python environment_and_volumes/check_volume_claim_and_mount_point.py
```

