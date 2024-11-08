# Assert volume claim mounting example<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Create the required k8s ressources (a volume mount)](#create-the-required-k8s-ressources-a-volume-mount)
- [Configuring the example for `hera_k8s_utils`](#configuring-the-example-for-hera_k8s_utils)
- [Running the example](#running-the-example)

## Create the required k8s ressources (a volume mount)

In this `hera_k8s_utils` example, a container requires the usage of a volume that can be defined at k8s cluster level with the following commands

```bash
# The namespace depends on your credentials
kubectl config set-context --current --namespace=argo-dev
# Creation of the workflow I/O placeholder (including results)
kubectl apply -f define_pvc.yaml
# Assert volume was properly created
kubectl get pvc vcity-pvc
```

## Configuring the example for `hera_k8s_utils`

This example requires a specific `hera_k8s_utils` configuration (file) that announces the usage of a volume (with the naming of a volume claim name).

In order to run this volume related example (as `hera_k8s_utils` module), first make sure you already [installed `hera_k8s_utils`](../README.md/##hera_utils-package-installation).
Then configure `hera_k8s_utils` for this example.
For example copy [this hera.config.tmpl file](./hera.config.tmpl) to the `hera.config` file

```bash
cd `git rev-parse --show-toplevel`/hera_k8s_utils/examples/volumes
cp hera.config.tmpl hera.config
```

and customize that file to your argo server as well as the underlying k8s cluster and provide associated credentials.

Eventually assert that the provided configuration is coherent by running the following test modules

```bash
python -m hera_k8s_utils.examples.volumes.parser   # Assert the configuration is complete
```

## Running the example

```bash
python -m hera_k8s_utils.examples.volumes.check_volume_claim_and_mount_point
```

You can then give a look at the following sources

- [`environment.py` script](./environment.py) that defines a `mount path` for the `volume claim`,
- [`volumes/parser.py` script](./parser.py) that defines the customized configuration parser.
