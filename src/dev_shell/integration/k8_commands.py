import shutil
import subprocess


class K8sCommands:
    @staticmethod
    def _run(command, interactive=False):
        if shutil.which("kubectl") is None:
            print("kubectl is not installed.")
            return

        try:
            if interactive:
                subprocess.run(command, check=False)  # noqa: S603
                return

            result = subprocess.run(  # noqa: S603
                command,
                text=True,
                capture_output=True,
                check=False,
            )

            if result.stdout:
                print(result.stdout, end="")

            if result.stderr:
                print(result.stderr, end="")

        except KeyboardInterrupt:
            print("\nCommand interrupted.")

        except OSError as e:
            print(f"Error: {e}")

    @staticmethod
    def help():
        print("""
Kubernetes Commands
===================

Cluster
-------

k8s cluster-info
k8s version
k8s api-resources
k8s api-versions
k8s get nodes
k8s get componentstatuses
k8s top nodes
k8s top pods
k8s describe node <node>

Contexts
--------

k8s config get-contexts
k8s config current-context
k8s config use-context <context>
k8s config rename-context <old> <new>
k8s config delete-context <context>
k8s config get-clusters
k8s config view

Namespaces
----------

k8s get namespaces
k8s get ns
k8s create namespace <namespace>
k8s delete namespace <namespace>
k8s describe namespace <namespace>

Pods
----

k8s get pods
k8s get pods -A
k8s get pods -o wide
k8s get pod <pod>
k8s describe pod <pod>
k8s logs <pod>
k8s logs -f <pod>
k8s logs <pod> -c <container>
k8s logs --previous <pod>
k8s exec -it <pod> -- bash
k8s exec -it <pod> -- sh
k8s port-forward <pod> <local>:<remote>
k8s delete pod <pod>
k8s run <name> --image=<image>

Deployments
-----------

k8s get deployments
k8s get deploy
k8s get deployment <deployment>
k8s describe deployment <deployment>
k8s create deployment <name> --image=<image>
k8s set image deployment/<name> <container>=<image>
k8s scale deployment <name> --replicas=<number>
k8s rollout status deployment/<name>
k8s rollout history deployment/<name>
k8s rollout pause deployment/<name>
k8s rollout resume deployment/<name>
k8s rollout restart deployment/<name>
k8s rollout undo deployment/<name>
k8s rollout undo deployment/<name> --to-revision=<revision>
k8s delete deployment <deployment>

ReplicaSets
-----------

k8s get replicasets
k8s get rs
k8s describe replicaset <replicaset>
k8s scale replicaset <replicaset> --replicas=<number>
k8s delete replicaset <replicaset>

StatefulSets
------------

k8s get statefulsets
k8s get sts
k8s describe statefulset <statefulset>
k8s scale statefulset <statefulset> --replicas=<number>
k8s rollout status statefulset/<statefulset>
k8s rollout restart statefulset/<statefulset>
k8s delete statefulset <statefulset>

DaemonSets
----------

k8s get daemonsets
k8s get ds
k8s describe daemonset <daemonset>
k8s rollout status daemonset/<daemonset>
k8s rollout restart daemonset/<daemonset>
k8s delete daemonset <daemonset>

Services
--------

k8s get services
k8s get svc
k8s get service <service>
k8s describe service <service>
k8s expose deployment <deployment> --port=<port>
k8s port-forward service/<service> <local>:<remote>
k8s delete service <service>

Ingress
-------

k8s get ingress
k8s get ing
k8s describe ingress <ingress>
k8s delete ingress <ingress>

ConfigMaps
----------

k8s get configmaps
k8s get cm
k8s describe configmap <configmap>
k8s create configmap <name>
k8s create configmap <name> --from-file=<file>
k8s create configmap <name> --from-literal=<key>=<value>
k8s delete configmap <configmap>

Secrets
-------

k8s get secrets
k8s describe secret <secret>
k8s create secret generic <name>
k8s create secret generic <name> --from-literal=<key>=<value>
k8s create secret generic <name> --from-file=<file>
k8s delete secret <secret>

Jobs
----

k8s get jobs
k8s describe job <job>
k8s create job <name> --image=<image>
k8s delete job <job>

CronJobs
--------

k8s get cronjobs
k8s get cj
k8s describe cronjob <cronjob>
k8s create cronjob <name> --image=<image>
k8s delete cronjob <cronjob>
k8s create job --from=cronjob/<cronjob> <job>

Storage
-------

k8s get persistentvolumes
k8s get pv
k8s describe pv <pv>
k8s delete pv <pv>

k8s get persistentvolumeclaims
k8s get pvc
k8s describe pvc <pvc>
k8s delete pvc <pvc>

k8s get storageclasses
k8s get sc
k8s describe storageclass <storageclass>
k8s delete storageclass <storageclass>

RBAC
----

k8s get roles
k8s describe role <role>
k8s create role <name>
k8s delete role <role>

k8s get rolebindings
k8s describe rolebinding <binding>
k8s create rolebinding <name>
k8s delete rolebinding <binding>

k8s get clusterroles
k8s describe clusterrole <role>
k8s delete clusterrole <role>

k8s get clusterrolebindings
k8s describe clusterrolebinding <binding>
k8s delete clusterrolebinding <binding>

Service Accounts
----------------

k8s get serviceaccounts
k8s get sa
k8s describe serviceaccount <serviceaccount>
k8s create serviceaccount <name>
k8s delete serviceaccount <serviceaccount>

Networking
----------

k8s get networkpolicies
k8s get netpol
k8s describe networkpolicy <policy>
k8s delete networkpolicy <policy>

Autoscaling
-----------

k8s get hpa
k8s get horizontalpodautoscalers
k8s describe hpa <hpa>
k8s autoscale deployment <deployment> --min=<min> --max=<max> --cpu-percent=<percent>
k8s delete hpa <hpa>

Resource Management
-------------------

k8s get all
k8s get all -A
k8s get events
k8s get events --sort-by=.metadata.creationTimestamp
k8s get pods,services,deployments
k8s get <resource>
k8s describe <resource> <name>
k8s explain <resource>
k8s explain <resource>.<field>

Labels
------

k8s label pod <pod> <key>=<value>
k8s label deployment <deployment> <key>=<value>
k8s label service <service> <key>=<value>
k8s label <resource> <name> <key>=<value> --overwrite

Annotations
-----------

k8s annotate pod <pod> <key>=<value>
k8s annotate deployment <deployment> <key>=<value>
k8s annotate service <service> <key>=<value>
k8s annotate <resource> <name> <key>=<value> --overwrite

Apply / Configuration
---------------------

k8s apply -f <file>
k8s apply -f <directory>
k8s apply -k <directory>
k8s delete -f <file>
k8s delete -f <directory>
k8s replace -f <file>
k8s diff -f <file>

Patch / Edit
------------

k8s edit deployment <deployment>
k8s edit service <service>
k8s edit pod <pod>
k8s patch <resource> <name> --patch=<patch>

Debugging
---------

k8s describe <resource> <name>
k8s logs <pod>
k8s logs -f <pod>
k8s logs --previous <pod>
k8s exec -it <pod> -- bash
k8s exec -it <pod> -- sh
k8s attach <pod>
k8s cp <pod>:<path> <local-path>
k8s cp <local-path> <pod>:<path>
k8s debug <pod>

Rollouts
--------

k8s rollout status <resource>/<name>
k8s rollout history <resource>/<name>
k8s rollout pause <resource>/<name>
k8s rollout resume <resource>/<name>
k8s rollout restart <resource>/<name>
k8s rollout undo <resource>/<name>

Resource Usage
--------------

k8s top nodes
k8s top pods
k8s top pods -A

Discovery
---------

k8s api-resources
k8s api-versions
k8s explain <resource>
k8s get <resource>

Cluster Administration
----------------------

k8s cordon <node>
k8s uncordon <node>
k8s drain <node>
k8s taint nodes <node> <key>=<value>:<effect>

Certificates
------------

k8s certificate approve <csr>
k8s certificate deny <csr>
k8s certificate delete <csr>
k8s get certificatesigningrequests

Plugins
-------

k8s plugin list

Aliases
-------

nodes
pods
all-pods
deployments
replicasets
statefulsets
daemonsets
services
ingress
configmaps
secrets
jobs
cronjobs
pv
pvc
storage
roles
rolebindings
clusterroles
clusterrolebindings
serviceaccounts
networkpolicies
hpa
events
namespaces
contexts
current-context
all
all-namespaces
top-nodes
top-pods
api-resources
api-versions
""")

    def execute(self, args):
        if not args:
            self.help()
            return

        command = args[0]

        aliases = {
            # Cluster
            "nodes": ["get", "nodes"],
            "top-nodes": ["top", "nodes"],
            "top-pods": ["top", "pods"],
            # Pods
            "pods": ["get", "pods"],
            "all-pods": ["get", "pods", "-A"],
            # Workloads
            "deployments": ["get", "deployments"],
            "replicasets": ["get", "replicasets"],
            "statefulsets": ["get", "statefulsets"],
            "daemonsets": ["get", "daemonsets"],
            # Networking
            "services": ["get", "services"],
            "ingress": ["get", "ingress"],
            "networkpolicies": ["get", "networkpolicies"],
            # Configuration
            "configmaps": ["get", "configmaps"],
            "secrets": ["get", "secrets"],
            # Jobs
            "jobs": ["get", "jobs"],
            "cronjobs": ["get", "cronjobs"],
            # Storage
            "pv": ["get", "persistentvolumes"],
            "pvc": ["get", "persistentvolumeclaims"],
            "storage": ["get", "storageclasses"],
            # RBAC
            "roles": ["get", "roles"],
            "rolebindings": ["get", "rolebindings"],
            "clusterroles": ["get", "clusterroles"],
            "clusterrolebindings": [
                "get",
                "clusterrolebindings",
            ],
            # Service Accounts
            "serviceaccounts": [
                "get",
                "serviceaccounts",
            ],
            # Autoscaling
            "hpa": [
                "get",
                "horizontalpodautoscalers",
            ],
            # Namespaces
            "namespaces": ["get", "namespaces"],
            # Events
            "events": ["get", "events"],
            # Contexts
            "contexts": [
                "config",
                "get-contexts",
            ],
            "current-context": [
                "config",
                "current-context",
            ],
            # Resources
            "all": ["get", "all"],
            "all-namespaces": ["get", "all", "-A"],
            # Discovery
            "api-resources": ["api-resources"],
            "api-versions": ["api-versions"],
        }

        if command in aliases:
            self._run(["kubectl"] + aliases[command] + args[1:])
            return

        interactive_commands = {
            "exec",
            "attach",
            "edit",
            "debug",
            "port-forward",
        }

        self._run(
            ["kubectl", *args],
            interactive=command in interactive_commands,
        )
