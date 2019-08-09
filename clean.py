import sys
import rancher
from kubernetes import client, config

delete_prtbs = False
delete_ns = False

cluster_id = ""

access=sys.argv[1]
secret=sys.argv[2]
rancherurl=sys.argv[3]

for key, arg in enumerate(sys.argv):
    if arg == "-d":
        delete_prtbs = True
    if arg == "-c":
        cluster_id = sys.argv[key+1]
    if arg == "-dn":
        delete_ns = True


rclient = rancher.Client(url=rancherurl + "/v3",
                        access_key=access,
                        secret_key=secret)


projects = rclient.list_project()

def just_project(proj):
    fragments = str.split(proj, ":")
    return fragments[len(fragments) - 1]


def just_cluster(proj):
    fragments = str.split(proj, ":")
    return fragments[0]

project_id_set = set(map(lambda x: just_project(x.id), projects))
project_to_cluster = {}

prtbs = rclient.list_project_role_template_binding()

for prtb in prtbs:
    proj_id = just_project(prtb.projectId)
    clus_id = just_cluster(prtb.projectId)
    # using prtb to get proj to cluster dict including deleted projects

    project_to_cluster[proj_id] = clus_id

    if (proj_id not in project_id_set) and (cluster_id == "" or project_to_cluster[proj_id] == cluster_id):
        if delete_prtbs:
            print("deleting prtb:", prtb.id)
            rclient.delete(prtb)
        else:
            print("remnant prtb:", prtb.id)

for proj in projects:
    project_to_cluster[just_cluster(proj.id)] = just_project(proj.id)
config.load_kube_config()
v1 = client.CoreV1Api()

namespaces = v1.list_namespace()
for ns in namespaces.items:
    ns_name = ns.metadata.name
    if ns_name not in project_id_set:
        if str.startswith(ns_name, "p-") and (cluster_id == "" or project_to_cluster[ns_name] == cluster_id):
            if delete_ns:
                print("deleting namespace:", ns_name)
                try:
                    v1.delete_namespace(ns_name)
                except:
                    print("didnt delete:", ns_name)
            else:
                print("remnant namespace:", ns_name)

