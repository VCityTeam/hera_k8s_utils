import types
import json
from hera_k8s_utils.k8s_cluster import k8s_cluster
from hera_utils import argo_server


class Struct:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class num_exp_environment(Struct):
    """
    The role of the NUMerical EXPeriment ENVIRONMENT class consists in
    separating the CLI command arguments into three distinctive sub-environments
    (blocks of concerns):
    - the sub-environment concerning the underlying k8s cluster,
    - the sub-environment concerning the Argo server,
    - the numerical experiment environment per se that gathers remaining
      arguments that are technically required to run the workflows.
    """

    def __init__(self, args, verbose=False):
        """
        :param args: the CLI arguments holding the environment tidbits.
        """
        self.assert_k8s_and_argo_servers(args, verbose)

        # In opposition to the above temporary variables, the information that
        # is "close/related" to k8s server, and that will be required to run
        # the workflows, shall be stored in this environment placeholder.
        self.cluster = types.SimpleNamespace()

    def assert_k8s_and_argo_servers(self, args, verbose):
        ### First start by asserting that the argo server was properly
        # configured (by the args) and "initialize" the Hera library.
        # Notice that this Hera initialization is a technical side effect of
        # this constructor. Yet this class does NOT need to keep a reference of
        # this argo server.
        argo = argo_server(args)
        if verbose:
            argo.print_config()
            print("Argo server looks ok.")

        ### Then proceed by asserting that the k8s cluster access was properly
        # configured (by the args).
        self.k8s = k8s_cluster(args)
        self.k8s.assert_cluster()
        if verbose:
            self.k8s.print_config()
            print("Kubernetes cluster seems ok.")

    def print_config(self):
        print("Environment of numerical experiment (at Python level):")
        print(self.toJSON())
