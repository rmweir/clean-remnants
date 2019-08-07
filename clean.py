import sys
import rancher

delete_prtbs = False

if len(sys.argv) > 1:
    delete_prtbs = True

client = rancher.Client(url='https://bf57de7d.ngrok.io/v3',
                        access_key='token-m82xm',
                        secret_key='zqtkq9fzpqtnkw8ndwm5z8dtffvznv7hrp7mdz2n2pfh424jz6r4zb')

projects = client.list_project()
project_id_set = set(map(lambda x: x.id, projects))

prtbs = client.list_project_role_template_binding()

for prtb in prtbs:
    if prtb.projectId not in project_id_set:
        if delete_prtbs:
            client.delete(prtb)
        else:
            print(prtb)

