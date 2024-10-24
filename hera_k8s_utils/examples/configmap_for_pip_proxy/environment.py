from hera_utils import argo_server
from hera_k8s_utils import k8s_cluster
from hera_k8s_utils.num_exp_environment import num_exp_environment, Struct


class environment(num_exp_environment):

    def __init__(self, args, verbose=False):

        num_exp_environment.__init__(self, args, verbose)

        k8s = k8s_cluster(args)
        k8s.assert_cluster()

        ### Some tasks require to retrieve cluster specific environment
        # (e.g. HTTP_PROXY) values at runtime. This retrieval is done through an
        # ad-hoc k8s configuration map. Assert this map exists.
        k8s.assert_configmap(args.k8s_configmap_name)
        self.cluster.configmap = args.k8s_configmap_name
