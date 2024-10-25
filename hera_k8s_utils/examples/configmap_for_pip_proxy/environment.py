from hera_k8s_utils import k8s_cluster
from hera_k8s_utils import num_exp_environment


class environment(num_exp_environment):

    def __init__(self, args, verbose=False):

        num_exp_environment.__init__(self, args, verbose)

        ### Some tasks require to retrieve cluster specific environment
        # ressources (e.g. HTTP_PROXY) values at runtime. This retrieval is
        # done through an ad-hoc k8s configuration map. Assert this map indeed
        # exists (and is accessible).
        self.k8s.assert_configmap(args.k8s_configmap_name)
        # Store the configmap name in the environment for task definition to
        # consume it.
        self.cluster.configmap = args.k8s_configmap_name
