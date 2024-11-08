# Using ConfigMaps example <!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Create the required k8s ressource (a configuration map)](#create-the-required-k8s-ressource-a-configuration-map)
- [Configuring the example for `hera_k8s_utils`](#configuring-the-example-for-hera_k8s_utils)
- [Running the example](#running-the-example)

## Create the required k8s ressource (a configuration map)

The usage scenario assumes that the cluster administrator chose to set up an [http proxy server](https://stackoverflow.com/questions/7155529/how-does-http-proxy-work) thus constraining the containers (requiring http access) to configure that proxy.
In this `hera_k8s_utils` example, a container requires to dynamically [install a python package with the `pip` command](https://stackoverflow.com/questions/19080352/how-to-get-pip-to-work-behind-a-proxy-server).  
Let us further assume that the cluster administrator chose to transmit (to the cluster users) the URL of that proxy through a [ConfigMap (Configuration Mapping)](https://hera.readthedocs.io/en/stable/api/workflows/hera/?h=configmap#hera.workflows.ConfigMapEnvFrom).

First, let us temporarily take the role of the administrator, and manually define [this `define_http_proxy_configmap.yml` ad-hoc ConfigMap](./define_http_proxy_configmap.yml) with e.g. the following commands

```bash
# The namespace depends on your credentials
kubectl config set-context --current --namespace=argo-dev
# Define cluster specific variables
kubectl apply -f define_http_proxy_configmap.yml
# Assert the configmap was properly created (note that the ConfigMap 
# name is defined within define_http_proxy_configmap.yml)
kubectl get configmaps hera-utils-proxy-environment -o yaml
```

## Configuring the example for `hera_k8s_utils`

This example is considered simple, because it makes no usage of its access to the k8s cluster.
The underlying `hera_k8s_utils` mechanism only asserts that the k8s cluster was properly designated and that access rights are correct.
It then prints the environment variables as seen from the cluster.

In order to run the following simple example (as `hera_k8s_utils` module), first make sure you already [installed `hera_k8s_utils`](../README.md/##hera_utils-package-installation).
Then configure `hera_k8s_utils` for this example.
For example copy [this hera.config.tmpl file](./hera.config.tmpl) to the `hera.config` file

```bash
cd `git rev-parse --show-toplevel`/hera_k8s_utils/examples/configmap_for_pip_proxy
cp hera.config.tmpl hera.config
```

and customize that file to your argo server as well as the underlying k8s cluster and provide associated credentials.

Eventually assert that the provided configuration is coherent by running the following test modules

```bash
python -m hera_k8s_utils.examples.configmap_for_pip_proxy.parser   # Assert the configuration is complete
```

## Running the example

 the previously defined ConfigMap can be accessed from Workflow tasks with

```bash
python -m hera_k8s_utils.examples.configmap_for_pip_proxy.print_config_map
```

Eventually you can now make some usage (through the `pip install` command that recognizes the `HTTPS_PROXY` environment variable) of that ConfigMap values by running the following WorkFlow

```bash
python -m hera_k8s_utils.examples.configmap_for_pip_proxy.use_configmap_for_pip
```
