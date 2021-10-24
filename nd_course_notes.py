"""
Kubeconfig file 

o access a Kubernetes cluster a kubeconfig file is required. A kubeconfig file has all the necessary cluster metadata and authentication details, that grants the user permission to query the cluster objects. Usually, the kubeconfig file is stored locally under the ~/.kube/config file. However, k3s places the kubeconfig file within /etc/rancher/k3s/k3s.yaml path. Additionally, the location of a kubeconfig file can be set through the --kubeconfig kubectl flag or via the KUBECONFIG environmental variable.

A Kubeconfig file has 3 main distinct sections:

Cluster - encapsulates the metadata for a cluster, such as the name of the cluster, API server endpoint, and certificate authority used to check the identity of the user.
User - contains the user details that want access to the cluster, including the user name, and any authentication metadata, such as username, password, token or client, and key certificates.
Context - links a user to a cluster. If the user credentials are valid and the cluster is up, access to resources is granted. Also, a current-context can be specified, which instructs which context (cluster and user) should be used to query the cluster.
Here is an example of a kubeconfig file:

apiVersion: v1
# define the cluster metadata 
clusters:
- cluster:
    certificate-authority-data: {{ CA }}
    server: https://127.0.0.1:63668
  name: udacity-cluster
# define the user details 
users:
# `udacity-user` user authenticates using client and key certificates 
- name: udacity-user
  user:
    client-certificate-data: {{ CERT }}
    client-key-data: {{ KEY }}
# `green-user` user authenticates using a token
- name: green-user
  user:
    token: {{ TOKEN }}
# define the contexts 
contexts:
- context:
    cluster: udacity-cluster
    user: udacity-user
  name: udacity-context
# set the current context
current-context: udacity-context

# Inspect  the endpoints for the cluster and installed add-ons 
kubectl cluster-info

# List all the nodes in the cluster. 
# To get a more detailed view of the nodes, the `-o wide` flag can be passed
kubectl get nodes [-o wide] 

# Describe a cluster node.
# Typical configuration: node IP, capacity (CPU and memory), a list of running pods on the node, podCIDR, etc.
kubectl describe node {{ NODE NAME }}

Solution: Deploy Your First Kubernetes Cluster
The kubeconfig file and kubectl commands are the 2 main components that permits the interaction with a Kubernetes cluster.

Let's take a closer look at cluster configuration details.

kubeconfig

K3s stores the kubeconfig file under /etc/rancher/k3s/k3s.yaml path
API server - https://127.0.0.1:6443
authentication mechanism - username (admin) and password
kubectl commands

kubectl cluster-info to get the control plane and add-ons endpoints

Kubernetes master is running at https://127.0.0.1:6443
CoreDNS is running at https://127.0.0.1:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://127.0.0.1:6443/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy
kubectl get nodes - to get all the nodes in the cluster

NAME        STATUS   ROLES    AGE   VERSION
localhost   Ready    master   74m   v1.18.9+k3s1
kubectl get nodes -o wide - to get extra details about the nodes, including internal IP

NAME        STATUS   ROLES    AGE   VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION            CONTAINER-RUNTIME
localhost   Ready    master   74m   v1.18.9+k3s1   10.0.2.15     <none>        openSUSE Leap 15.2   5.3.18-lp152.47-default   containerd://1.3.3-k3s2
kubectl describe node node-name - to get all the configuration details about the node, including the allocated pod CIDR

kubectl describe node localhost | grep CIDR
PodCIDR:                      10.42.0.0/24
PodCIDRs:                     10.42.0.0/24

Kubernetes provides a rich collection of resources that are used to deploy, configure, and manage an application. Some of the widely used resources are:

Pods - the atomic element within a cluster to manage an application
Deployments & ReplicaSets - oversees a set of pods for the same application
Services & Ingress - ensures connectivity and reachability to pods
Configmaps & Secrets - pass configuration to pods
Namespaces - provides a logical separation between multiple applications and their resources
Custom Resource Definition (CRD) - extends Kubernetes API to support custom resources

A pod is the anatomic element within a cluster that provides the execution environment for an application. Pods are the smallest manageable units in a Kubernetes cluster. Every pod has a container within it, that executes an application from a Docker image (or any OCI-compliant image). There are use cases where 2-3 containers run within the same pod, however, it is highly recommended to keep the 1:1 ratio between your pods and containers.

All the pods are placed on the cluster nodes. A note can host multiple pods for different applications.

A pod is the anatomic element within a cluster that provides the execution environment for an application. Pods are the smallest manageable units in a Kubernetes cluster. Every pod has a container within it, that executes an application from a Docker image (or any OCI-compliant image). There are use cases where 2-3 containers run within the same pod, however, it is highly recommended to keep the 1:1 ratio between your pods and containers.

All the pods are placed on the cluster nodes. A note can host multiple pods for different applications.

Diagram of the pod anatomy
Pod architecture, showcasing a container running a Docker image

Deployments and ReplicaSets
Diagram of application deployment using Kubernetes resources 
Application management using a Deployment and ReplicaSet

To deploy an application to a Kubernetes cluster, a Deployment resource is necessary. A Deployment contains the specifications that describe the desired state of the application. Also, the Deployment resource manages pods by using a ReplicaSet. A ReplicaSet resource ensures that the desired amount of replicas for an application are up and running at all times.

To create a deployment, use the kubectl create deployment command, with the following syntax:

# create a Deployment resource
# NAME - required; set the name of the deployment
# IMAGE - required;  specify the Docker image to be executed
# FLAGS - optional; provide extra configuration parameters for the resource
# COMMAND and args - optional; instruct the container to run specific commands when it starts 
kubectl create deploy NAME --image=image [FLAGS] -- [COMMAND] [args]

# Some of the widely used FLAGS are:
-r, --replicas - set the number of replicas
-n, --namespace - set the namespace to run
--port - expose the container port
For example, to create a Deployment for the Go hello-world application, the following command can be used:

# create a go-helloworld Deployment in namespace `test`
kubectl create deploy go-helloworld --image=pixelpotato/go-helloworld:v1.0.0 -n test
It is possible to create headless pods or pods that are not managed through a ReplicaSet and Deployment. Though it is not recommended to create standalone pods, these are useful when creating a testing pod.

To create a headless pod, the kubectl run command is handy, with the following syntax:

# create a headless pod
# NAME - required; set the name of the pod
# IMAGE - required;  specify the Docker image to be executed
# FLAGS - optional; provide extra configuration parameters for the resource
# COMMAND and args - optional; instruct the container to run specific commands when it starts 
kubectl run NAME --image=image [FLAGS] -- [COMMAND] [args...]

# Some of the widely used FLAGS are:
--restart - set the restart policy. Options [Always, OnFailure, Never]
--dry-run - dry run the command. Options [none, client, server]
-it - open an interactive shell to the container
For example, to create a busybox pod, the following command can be used:

# example: create a busybox pod, with an interactive shell and a restart policy set to Never 
kubectl run -it busybox-test --image=busybox --restart=Never
Rolling Out Strategy
The Deployment resource comes with a very powerful rolling out strategy, which ensures that no downtime is encountered when a new version of the application is released. Currently, there are 2 rolling out strategies:

RollingUpdate - updates the pods in a rolling out fashion (e.g. 1-by-1)
Recreate - kills all existing pods before new ones are created
For example, in this case, we upgrade a Go hello-world application from version 1.0.0 to version 2.0.0:

Diagram of the rolling update of an application
Rolling update of an application, between different versions

Where:

The Go hello-world application is running version v1.0.0 in a pod managed by a ReplicaSet
The version of Go hello-world application is set to v2.0.0
A new ReplicaSet is created that controls a new pod with the application running in version v2.0.0
The traffic is directed to the pod running v2.0.0 and the pod with the old configuration (v1.0.0) is removed

# Application version: v1.0.0
# port exposed: 6111
package main

import (
    "fmt"
    "net/http"
)

func helloWorld(w http.ResponseWriter, r *http.Request){
    fmt.Fprintf(w, "Hello World")
}

func main() {
    http.HandleFunc("/", helloWorld)
    http.ListenAndServe(":6111", nil)
}

# Application version: v2.0.0
# port exposed: 6112
package main

import (
    "fmt"
    "net/http"
)

func helloWorld(w http.ResponseWriter, r *http.Request){
    fmt.Fprintf(w, "Hello World")
}

func main() {
    http.HandleFunc("/", helloWorld)
    http.ListenAndServe(":6112", nil)
}

New terms
Pod - smallest manageable uint within a cluster that provides the execution environment for an application
ReplicaSet - a mechanism to ensure a number of pod replicas are up and running at all times
Deployment - describe the desired state of the application to be deployed
Further reading

Within a cluster, every pod is allocated 1 unique IP which ensures connectivity and reachability to the application inside the pod. This IP is only routable inside the cluster, meaning that external users and services will not be able to connect to the application.

For example, we can connect a workload within the cluster to access a pod directly via its IP. However, if the pod dies, all future requests will fail, as these are routes to an application that is not running. The remediation step is to configure the workload to communicate with a different pod IP. This is a highly manual process, which brings complexity to the accessibility of an application. To automate the reachability to pods, a Service resource is necessary.

Services
Diagram of the pod connectivity through a service resource
Pods accessibility through a Service resource

A Service resource provides an abstraction layer over a collection of pods running an application. A Service is allocated a cluster IP, that can be used to transfer the traffic to any available pods for an application.

As such, as shown in the above image, instead of accessing each pod independently, the workload (1) should access the service IP (2), which routes the requests to available pods (3).

There are 3 widely used Service types:

ClusterIP - exposes the service using an internal cluster IP. If no service type is specified, a ClusterIP service is created by default.
NodePort - expose the service using a port exposed on all nodes in the cluster.
LoadBalancer - exposes the service through a load balancer from a public cloud provider such as AWS, Azure, or GCP. This will allow the external traffic to reach the services within the cluster securely.
To create a service for an existing deployment, use the kubectl expose deployment command, with the following syntax:

# expose a Deployment through a Service resource 
# NAME - required; set the name of the deployment to be exposed
# --port - required; specify the port that the service should serve on
# --target-port - optional; specify the port on the container that the service should direct traffic to
# FLAGS - optional; provide extra configuration parameters for the service
kubectl expose deploy NAME --port=port [--target-port=port] [FLAGS]

# Some of the widely used FLAGS are:
--protocol - set the network protocol. Options [TCP|UDP|SCTP]
--type - set the type of service. Options [ClusterIP, NodePort, LoadBalancer]
For example, to expose the Go hello-world application through a service, the following command can be used:

# expose the `go-helloworld` deployment on port 8111
# note: the application is serving requests on port 6112
kubectl expose deploy go-helloworld --port=8111 --target-port=6112
Ingress
Diagram of Ingress resource enabling access from the external users to services within the cluster
Ingress resources enabling access from the external users to services within the cluster

To enable the external user to access services within the cluster an Ingress resource is necessary. An Ingress exposes HTTP and HTTPS routes to services within the cluster, using a load balancer provisioned by a cloud provider. Additionally, an Ingress resource has a set of rules that are used to map HTTP(S) endpoints to services running in the cluster. To keep the Ingress rules and load balancer up-to-date an Ingress Controller is introduced.

For example, as shown in the image above, the customers will access the go-helloworld.com/hi HTTP route (1), which is managed by an Ingress (2). The Ingress Controller (3) examines the configured routes and directs the traffic to a LoadBalancer (4). And finally, the LoadBalancer directs the requests to the pods using a dedicated port (5).

Application Reachability Demo

Summary
This demo provides a step-by-step guide on how to expose the Go hello-world application through a ClusterIP service. Additionally, an alpine pod is used to showcase how a workload can connect to the Go hello-world application through the service IP and port from within the cluster.

New terms
Service - an abstraction layer over a collection of pods running an application
Ingress - a mechanism to manage the access from external users and workloads to the services within the cluster

Kubernetes Resources Part 3
Application Configuration And Context

Summary
In the implementation phase, a good development practice is to separate the configuration from the source code. This increased the portability of an application as it can cover multiple customer use cases. Kubernetes has 2 resources to pass data to an application: Configmaps and Secrets.

ConfigMaps
ConfigMaps are objects that store non-confidential data in key-value pairs. A Configmap can be consumed by a pod as an environmental variable, configuration files through a volume mount, or as command-line arguments to the container.

To create a Configmap use the kubectl create configmap command, with the following syntax:

# create a Configmap
# NAME - required; set the name of the configmap resource
# FLAGS - optional; define  extra configuration parameters for the configmap
kubectl create configmap NAME [FLAGS]

# Some of the widely used FLAGS are:
--from-file - set path to file with key-value pairs 
--from-literal - set key-value pair from command-line 
For example, to create a Configmap to store the background color for a front-end application, the following command can be used:

# create a Configmap to store the color value
kubectl create configmap test-cm --from-literal=color=yellow
Secrets
Secrets are used to store and distribute sensitive data to the pods, such as passwords or tokens. Pods can consume secrets as environment variables or as files from the volume mounts to the pod. It is noteworthy, that Kubernetes will encode the secret values using base64.

To create a Secret use the kubectl create secret generic command, with the following syntax:

# create a Secret
# NAME - required; set the name of the secret resource
# FLAGS - optional; define  extra configuration parameters for the secret
kubectl create secret generic NAME [FLAGS]

# Some of the widely used FLAGS are:
--from-file - set path to file with the sensitive key-value pairs 
--from-literal - set key-value pair from command-line 
For example, to create a Secret to store the secret background color for a front-end application, the following command can be used:

# create a Secret to store the secret color value
kubectl create secret generic test-secret --from-literal=color=blue
Namespaces
A Kubernetes cluster is used to host hundreds of applications, and it is required to have separate execution environments across teams and business verticals. This functionality is provisioned by the Namespace resources. A Namespace provides a logical separation between multiple applications and associated resources. In a nutshell, it provides the application context, defining the environment for a group of Kubernetes resources that relate to a project, such as the amount of CPU, memory, and access. For example, a project-green namespace includes any resources used to deploy the Green Project. These resources construct the application context and can be managed collectively to ensure a successful deployment of the project.

Each team or business vertical is allocated a separate Namespace, with the desired amount of CPU, memory, and access. This ensures that the application is managed by the owner team and has enough resources to execute successfully. This also eliminates the "noisy neighbor" use case, where a team can consume all the available resources in the cluster if no Namespace boundaries are set.

To create a Namespace we can use the kubectl create namespace command, with the following syntax:

# create a Namespace
# NAME - required; set the name of the Namespace
kubectl create ns NAME
For example, to create a test-udacity Namespace, the following command can be used:

# create a `test-udacity` Namespace
kubectl create ns test-udacity

# get all the pods in the `test-udacity` Namespace
kubectl get po -n test-udacity
Demo - Application Configuration

Summary
This demo is a step-by-step guide on how to create a Namespace resource and retrieve resources from a specific Namespace.

New terms
Configmap - a resource to store non-confidential data in key-value pairs.
Secret - a resource to store confidential data in key-value pairs. These are base64 encoded.
Namespace - a logical separation between multiple applications and associated resources.

********************
ubectl provides a rich set of actions that can be used to interact, manage, and configure Kubernetes resources. Below is a list of handy kubectl commands used in practice.

Note: In the following commands the following arguments are used:

RESOURCE is the Kubernetes resource type
NAME sets the name of the resource
FLAGS are used to provide extra configuration
PARAMS are used to provide the required configuration to the resource
Create Resources
To create resources, use the following command:

kubectl create RESOURCE NAME [FLAGS]
Describe Resources
To describe resources, use the following command:

kubectl describe RESOURCE NAME 
Get Resources
To get resources, use the following command, where -o yaml instructs that the result should be YAML formated.

kubectl get RESOURCE NAME [-o yaml]
Edit Resources
To edit resources, use the following command, where -o yaml instructs that the edit should be YAML formated.

kubectl edit RESOURCE NAME [-o yaml]
Label Resources
To label resources, use the following command:

kubectl label RESOURCE NAME [PARAMS]
Port-forward to Resources
To access resources through port-forward, use the following command:

kubectl port-forward RESOURCE/NAME [PARAMS]
Logs from Resources
To access logs from a resource, use the following command:

kubectl logs RESOURCE/NAME [FLAGS]
Delete Resources
To delete resources, use the following command:

kubectl delete RESOURCE NAME

Exercise: Kubernetes Resources
Now you have learned many Kubernetes recourses, in this exercise, you will deploy the following resources using the kubectl command.

a namespace
name: demo
label: tier: test
a deployment:
image: nginx:alpine
name:nginx-apline
namespace: demo
replicas: 3
labels: app: nginx, tag: alpine
a service:
expose the above deployment on port 8111
namespace: demo
a configmap:
name: nginx-version
containing key-value pair: version=alpine
namespace: demo
Note: Nginx is one of the public Docker images, that you can access and use for your exercises or testing purposes.

Solution: Kubernetes Resources
Below is a snippet creating a namespace and labeling it, a deployment, a service, and a configmap using the kubectl operations.

# create the namespace 
# note: label option is not available with `kubectl create`
kubectl create ns demo

# label the namespace
kubectl label ns demo tier=test

# create the nginx-alpine deployment 
kubectl create deploy nginx-alpine --image=nginx:alpine  --replicas=3 --namespace demo

# label the deployment
kubectl label deploy nginx-alpine app=nginx tag=alpine --namespace demo

# expose the nginx-alpine deployment, which will create a service
kubectl expose deployment nginx-alpine --port=8111 --namespace demo

# create a config map
kubectl create configmap nginx-version --from-literal=version=alpine --namespace demo
Spoiler alert: in the next section, you will learn and practice how to deploy Kubernetes resources using a different approach.

;

Declarative Kubernetes Manifests

Summary
Kubernetes is widely known for its support for imperative and declarative management techniques. The imperative approach enables the management of resources using kubectl commands directly on the live cluster. For example, all the commands you have practiced so far (e.g. kubectl create deploy [...]) are using the imperative approach. This technique is best suited for development stages only, as it presents a low entry-level bar to interact with the cluster.

On the other side, the declarative approach uses manifests stored locally to create and manage Kubertenest objects. This approach is recommended for production releases, as we can version control the state of the deployed resources. However, this technique presents a high learning curve, as an in-depth understanding of the YAML manifest structure is required. Additionally, using YAML manifests unlocks the possibility of configuring more advanced options, such as volume mounts, readiness and liveness probes, etc.

YAML Manifest structure
A YAML manifest consists of 4 obligatory sections:

apiversion - API version used to create a Kubernetes object
kind - object type to be created or configured
metadata - stores data that makes the object identifiable, such as its name, namespace, and labels
spec - defines the desired configuration state of the resource
To get the YAML manifest of any resource within the cluster, use the kubectl get command, associated with the -o yaml flag, which requests the output in YAML format. Additionally, to explore all configurable parameters for a resource it is highly recommended to reference the official Kubernetes documentation.

Deployment YAML manifest
In addition to the required sections of a YAML manifest, a Deployment resource covers the configuration of ReplicaSet, RollingOut strategy, and containers. Bellow is a full manifest of a Deployment explaining each parameter:

## Set the API endpoint used to create the Deployment resource.
apiVersion: apps/v1
## Define the type of the resource.
kind: Deployment
## Set the parameters that make the object identifiable, such as its name, namespace, and labels.
metadata:
  annotations:
  labels:
    app: go-helloworld
  name: go-helloworld
  namespace: default
## Define the desired configuration for the Deployment resource.
spec:
  ## Set the number of replicas.
  ## This will create a ReplicaSet that will manage 3 pods of the Go hello-world application.
  replicas: 3
  ## Identify the pods managed by this Deployment using the following selectors.
  ## In this case, all pods with the label `go-helloworld`.
  selector:
    matchLabels:
      app: go-helloworld
  ## Set the RollingOut strategy for the Deployment.
  ## For example, roll out only 25% of the new pods at a time.
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  ## Set the configuration for the pods.
  template:
    ## Define the identifiable metadata for the pods.
    ## For example, all pods should have the label `go-helloworld`
    metadata:
      labels:
        app: go-helloworld
    ## Define the desired state of the pod configuration.
    spec:
      containers:
        ## Set the image to be executed inside the container and image pull policy
        ## In this case, run the `go-helloworld` application in version v2.0.0 and
        ## only pull the image if it's not available on the current host.
      - image: pixelpotato/go-helloworld:v2.0.0
        imagePullPolicy: IfNotPresent
        name: go-helloworld
        ## Expose the port the container is listening on.
        ## For example, exposing the application port 6112 via TCP.
        ports:
        - containerPort: 6112
          protocol: TCP
        ## Define the rules for the liveness probes.
        ## For example, verify the application on the main route `/`,
        ## on application port 6112. If the application is not responsive, then the pod will be restarted automatically. 
        livenessProbe:
           httpGet:
             path: /
             port: 6112
        ## Define the rules for the readiness probes.
        ## For example, verify the application on the main route `/`,
        ## on application port 6112. If the application is responsive, then traffic will be sent to this pod.
        readinessProbe:
           httpGet:
             path: /
             port: 6112
        ## Set the resource requests and limits for an application.
        resources:
        ## The resource requests guarantees that the desired amount 
        ## CPU and memory is allocated for a pod. In this example, 
        ## the pod will be allocated with 64 Mebibytes and 250 miliCPUs.
          requests:
            memory: "64Mi"
            cpu: "250m"
        ## The resource limits ensure that the application is not consuming 
        ## more than the specified CPU and memory values. In this example, 
        ## the pod will not surpass 128 Mebibytes and 500 miliCPUs.
          limits:
            memory: "128Mi"
            cpu: "500m"
Service YAML manifest
In addition to the required sections of a YAML manifest, a Service resource covers the configuration of service type and ports the service should configure. Bellow is a full manifest of a Service explaining each parameter:

## Set the API endpoint used to create the Service resource.
apiVersion: v1
## Define the type of the resource.
kind: Service
## Set the parameters that make the object identifiable, such as its name, namespace, and labels.
metadata:
  labels:
    app: go-helloworld
  name: go-helloworld
  namespace: default
## Define the desired configuration for the Service resource.
spec:
  ## Define the ports that the service should serve on. 
  ## For example, the service is exposed on port 8111, and
  ## directs the traffic to the pods on port 6112, using TCP.
  ports:
  - port: 8111
    protocol: TCP
    targetPort: 6112
  ## Identify the pods managed by this Service using the following selectors.
  ## In this case, all pods with the label `go-helloworld`.
  selector:
    app: go-helloworld
  ## Define the Service type, here set to ClusterIP.
  type: ClusterIP
Useful command
Kubernetes YAML manifests can be created using the kubectl apply command, with the following syntax:

# create a resource defined in the YAML manifests with the name manifest.yaml
kubectl apply -f manifest.yaml
To delete a resource using a YAML manifest, the kubectl delete command, with the following syntax:

# delete a resource defined in the YAML manifests with the name manifest.yaml
kubectl delete -f manifest.yaml
Kubernetes documentation is the best place to explore the available parameters for YAML manifests. However, a support YAML template can be constructed using kubectl commands. This is possible by using the --dry-run=client and -o yamlflags which instructs that the command should be evaluated on the client-side only and output the result in YAML format.

# get YAML template for a resource 
kubectl create RESOURCE [REQUIRED FLAGS] --dry-run=client -o yaml
For example, to get the template for a Deployment resource, we need to use the create command, pass the required parameters, and associated with the --dry-run and -o yaml flags. This outputs the base template, which can be used further for more advanced configuration.

# get the base YAML templated for a demo Deployment running a nxing application
 kubectl create deploy demo --image=nginx --dry-run=client -o yaml
Declarative Kubernetes Manifests Walkthrough

Exercise: Declarative Kubernetes Manifests
Kubernetes is widely known for its imperative and declarative management techniques. In the previous exercise, you have deployed the following resources using the imperative approach. Now deploy them using the declarative approach.

a namespace

name: demo
label: tier: test
a deployment:

image: nginx:alpine
name:nginx-apline
namespace: demo
replicas: 3
labels: app: nginx, tag: alpine
a service:

expose the above deployment on port 8111
namespace: demo
a configmap:

name: nginx-version
containing key-value pair: version=alpine
namespace: demo
Note: Nginx is one of the public Docker images, that you can access and use for your exercises or testing purposes.



*********************************

Solution: Declarative Kubernetes Manifests
Declarative Approach
The declarative approach consists of using a full YAML definition of resources. As well, with this approach, you can perform directory level operations.

Examine the manifests for all of the resources in the exercises/manifests.

To create the resources, use the following command:

kubectl apply -f exercises/manifests/
To inspect all the resources within the namespace, use the following command:

kubectl get all -n demo

NAME                                READY   STATUS    RESTARTS   AGE
pod/nginx-alpine-798fb5b8bb-8rzq9   1/1     Running   0          12s
pod/nginx-alpine-798fb5b8bb-ms28l   1/1     Running   0          12s
pod/nginx-alpine-798fb5b8bb-qgqb2   1/1     Running   0          12s

NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/nginx-alpine   ClusterIP   10.109.197.180   <none>        8111/TCP   18s

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx-alpine   3/3     3            3           12s

NAME                                      DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-alpine-798fb5b8bb   3         3         3       12s


Lesson 3:
Container Orchestration with Kubernetes
 1. Introduction
 2. Transitions from VMs to Containers
 3. Docker for Application Packaging
 4. Docker Walkthrough
 5. Useful Docker Commands
 6. Quizzes: Docker for Application Packaging
 7. Exercise: Docker for Application Packaging
 8. Solution: Docker for Application Packaging
 9. Kubernetes - The Container Orchestrator Framework
 10. Quizzes: Kubernetes - The Container Orchestrator Framework
 11. Deploy Your First Kubernetes Cluster
 12. Kubeconfig
 13. Quizzes: Deploy Your First Kubernetes Cluster
 14. Exercise: Deploy Your First Kubernetes Cluster
 15. Solution: Deploy Your First Kubernetes Cluster
 16. Kubernetes Resources Part 1
 17. Kubernetes Resources Part 2
 18. Kubernetes Resources Part 3
 19. Useful kubectl Commands
 20. Quizzes: Kubernetes Resources
 21. Exercise: Kubernetes Resources
 22. Solution: Kubernetes Resources
 23. Declarative Kubernetes Manifests
 24. Quizzes: Declarative Kubernetes Manifests
 25. Exercise: Declarative Kubernetes Manifests
 26. Solution: Declarative Kubernetes Manifests
 27. Edge Case: Failing Control Plane for Kubernetes
 28. Lesson Review
Edge Case: Failing Control Plane for Kubernetes
Edge Case: Failing Control Plane for Kubernetes

Summary
Failure is expected in any technology stack. However, it is more important to have efficient remediations steps rather than plan for no-failure scenarios. Kubernetes provides methods to handle some of the low-level failures and ensure the application is healthy and accessible. Some of these resources are:

ReplicaSets - to ensure that the desired amount of replicas is up and running at all times
Liveness probes - to check if the pod is running, and restart it if it is in an errored state
Readiness probes - ensure that traffic is routed to that pods that are ready to handle requests
Services - to provide one entry point to all the available pods of an application
These services, prompt the automatic recovery of an application if an error is encountered. However, failure can happen at the cluster-level, for example, a control plane failure. In this case, a subset or all control plane components are compromised. While the situation is disastrous, the applications are still running and handling traffic. The downside of the control plane failure is that no new workloads can be deployed and no changes can be applied to the existing workloads.

The engineering team needs to recover the control plane components as a critical priority. However, they should not worry about recovering applications, as these will be intact and still handling requests.

Summary
In this lesson, we have covered how to package an application using Docker and store it in DockerHub. Then, we practiced how to bootstrap a cluster using k3s and deploy an application using Kubernetes resources. For more advanced configurations, we have evaluated Kubernetes YAML manifests that are the basis of declarative management techniques.

Overall, in this lesson, we covered:

Docker for Application Packaging
Container Orchestration with Kubernetes
Kubernetes Resources
Declarative Kubernetes Manifests
Glossary
Dockerfile - set of instructions used to create a Docker image
Docker image - a read-only template used to spin up a runnable instance of an application
Docker registry - a central mechanism to store and distribute Docker images
CRD - Custom Resource Definition provides the ability to extend Kubernetes API and create new resources
Node - a physical or virtual server
Cluster - a collection of distributed nodes that are used to manage and host workloads
Master node - a node from the Kubernetes control plane, that has installed components to make global, cluster-level decisions
Worker node - a node from the Kubernetes data plane, that has installed components to host workloads
Bootstrap - the process of provisioning a Kubernetes cluster, by ensuring that each node has the necessary components to be fully operational
Kubeconfig - a metadata file that grants a user access to a Kubernetes cluster
Pod - smallest manageable uint within a cluster that provides the execution environment for an application
ReplicaSet - a mechanism to ensure a number of pod replicas are up and running at all times
Deployment - describe the desired state of the application to be deployed
Service - an abstraction layer over a collection of pods running an application
Ingress - a mechanism to manage the access from external users and workloads to the services within the cluster
Configmap - a resource to store non-confidential data in key-value pairs.
Secret - a resource to store confidential data in key-value pairs. These are base64 encoded.
Namespace - a logical separation between multiple applications and associated resources.
Imperative configuration - resource management technique, that operates and interacts directly with the live objects within the cluster.
Declarative configuration - resource management technique, that operates and manages resources using YAML manifests stored locally.

PaaS Mechanisms

Summary
The industry is abundant with cloud-computing offerings that offer variate level of attraction of services. Some of the widely used cloud-computing services are:

On-premise - where an engineering team has full control over the platform, including the physical servers
IaaS or Infrastructure as a Service - where a team consumes compute, network, and storage resources from a vendor
PaaS or Platform as a Service - where the infrastructure is fully managed by a provider, and the team is focused on application deployment
Diagram of widely used cloud-computing service 
Widely used cloud-computing offerings

Releasing a product to a production environment implies that a platform has been build to host this particular product. A platform consists of multiple services that need to be configured, wired, and maintained together. These services are:

Networking - establish communication between internal and external systems, such as internet connection, firewalls, routers, and cables
Storage- collect and store digital data, such as files, blocks, or objects
Servers - physical machines that provide compute services for a platform
Virtualization - abstracts physical servers, storage, and networking. For example, we have learned that hypervisors are used to virtualize servers.
O/S - operating systems that connect the software to physical resources (e.g. Linux, Ubuntu, Windows, etc)
Middleware - help the developers to build an application by making it easy to consume platform capabilities (e.g. messaging, API, data management)
Runtime - execution context for an application. For example, using JVM (or Java Virtual Machine) as a Java runtime
Data - tools for collection and storage of data that is required by an application during execution(e.g. MySQL, MongoDB, or CockroachDB)
Applications - the business logic for a product
On-premise
On-premise represents a cloud-computing offering where the engineering team has full control of the platform services (from networking to applications). This solution is suitable for organizations that have sufficient engineering power and regulations that demand full control of their technology stack and operations within it.

IaaS
IaaS solutions provide the abstraction of networking, storage, server, and virtualization layers. As a result, these services are consumed on-demand by the engineering teams. Additionally, IaaS provides a suitable abstraction for the management of self-hosted Kubernetes clusters, which depend on compute, network, and storage components for a successful bootstrap process.

The most common IaaS solutions are delivered by public cloud providers such as AWS, GCP, Microsoft Azure, and many more.

PaaS
PaaS is a cloud-computing offering that enables an engineering team to fully focus on application development. It abstracts all services except the application and the data associated with it. As a result, the team is required to manage the code base and any database service that the product needs to be fully operational.

Popular PaaS solutions are App Engine from GCP, Heroku, Cloud Foundry, Beanstalk from AWS, and many more.

Advantages:

Time-efficiency - engineering focus is shifter toward development rather than infrastructure management
Scalability and high availability - on-demand resource consumption enables an application to easily scale and fail-over
Rich application catalog - integration of external service (e.g. databases) with minimal effort
Disadvantages:

Vendor lock-in - it is challenging to interchange PaaS providers without service disruption
Data security - since data is managed by a 3rd party, an extra layer of complexity is added to ensure data confidentiality
Operational limitations - the service catalog is limited to the services offered by the integrated cloud provider
Diagram of different service that a cloud-computing service is capable of managing 
Variate levels of service management from cloud-computing offerings

Throughout its evolution, an organization might use one or a subset of available cloud-computing services. It is essential to select an offering that closely meets business requirements. However, it is important to consider the following traits of cloud-computing services:

The fewer components are delegated to external providers, the more control there is over available functionalities
The more ownership there is across the stack, the more complexity is introduced in managing and delivering the product
The fewer components are managed by an engineering team, the quicker is the usability of the stack. As such, with a PaaS offering the engineering team can deploy their application immediately. While if choosing an on-premise solution, the release of a product is possible only after the platform is built.
Diagram showcasing the level of complexity vs usability of each cloud-computing service
Complexity vs Usability for each cloud-computing offering

New terms
On-premise - cloud-computing service, where a team owns the entire technology stack.
IaaS - cloud-computing service that offers the abstraction of networking, storage, server, and virtualization layers.
PaaS - cloud-computing service, where the infrastructure components are managed fully by a 3rd party provider, and a team manages only the application and the data associated with it.

By default, the PaaS solutions offer the management of the underlying infrastructure, such as storage, databases, compute, hosting, and many more. Also, the majority of solutions will provide data analytics, security, and advanced scheduling.

As such, the web-store project will benefit from the following PaaS capabilities:

database - for storing the customer details, orders, and products details
compute - accessible scalability for the application to serve millions of customers
networking - hosting and serving the requests with no downtime
analytics - an add-on to collect data and provide metrics and logs about customer interaction with the web-store

Cloud Foundry

Summary
Integrating PaaS solutions within an organization shifts the engineering effort from infrastructure management to product development. Additionally, it provides a powerful developer experience throughout the release process of an application, where the main functionalities are consumed through a UI or console. However, there is one major downside with this offering: vendor and application catalog lock-in. If an application is deployed using a PaaS offering from GCP, the application catalog of external services is narrowed down to GCP services mainly. Consequently, the open-source fundamentals were applied to PaaS offerings, resulting in an open-source PaaS such as Cloud Foundry.

Cloud Foundry is an open-source PaaS, a stand-alone software package that can be installed on any available infrastructure; private, public, or hybrid cloud. Due to its open-source nature, there is no vendor lock-in and the community can contribute to its future releases and definition of the roadmap. As such, Cloud Foundry offers a production-grade release process through a solid developer experience, that enables any application to be deployed with ease.

Note: some offerings of Cloud Foundry, can be deployed on top of Kubernetes, meaning that its main components are running as pods within a cluster.

Cloud Foundry consists of multiple components that provide these core capabilities:

Routing - handle the incoming external traffic and route it to applications
Authentication - identity management to user accounts
Application lifecycle - controls the application deployments, monitors their status, and reconciles any new changes to reach the desired state of the application.
Application storage and execution - handle the availability of artifacts to applications
Service - use service brokers to provisions on-demand the dependency services for an application, such as a database or third-party APIs
Messaging - ensure the communication between Cloud Foundry components
Metrics and logging - aggregates the system and application metrics and logs
In the following sections, we will explore Cloud Foundry using SUSE Cloud Application Platform Developer Sandbox. However, you can explore Cloud Foundry's functionalities using the following offerings as well:

IBM Cloud Foundry
SAP Cloud Platform
Anynines
Could Foundry Walkthrough - Part 1
Let's explore the release of an application using Cloud Foundry!

Note: The walkthrough demos aim to highlight the simplified developer experience to release an application without the need to manage infrastructure components. Learning and understanding each Cloud Foundry functionality and implementation details is not an objective for this course.


Summary
This demo showcases the main capabilities of the Stratos console and Cloud Foundry.

Some of the noteworthy sections are:

Marketplace and Services - research the service catalog and explore any integrated services
Organizations - used to manage multi-tenancy, quotas, and access to applications
Routes - list all available endpoints used to access deployed applications
Build Packs - explore available buildpacks packages used to build an application
Security groups - configure the endpoints that the application can communicate with
Could Foundry Walkthrough - Part 2
Note: This demo references the Python hello-world application.


Summary
This demo provides a step-by-step guide on how to deploy a simple Python hello-world application to Cloud Foundry.

Noteworthy steps in this demo:

Python hello-world is a simple Flask application, serving on port 8080
Cloud Foundry can use a manifest.yml file to store the configuration of the application, such as name and quotas
Routes are used to access the application and can be configured or created randomly

Solution: Cloud Foundry
It is pivotal to understand the application functionalities and available resources. This is especially the case when a microservice-based design is chosen, and solutions suck as IaaS (Infrastructure as a Service), PaaS (Platform as a Service), SaaS (Software as a Service) are available from a multitude of vendors. Choosing the most suitable deployment tooling will lead to the efficient delivery of the product.

Considering that the application code is available, these are the steps to adopt each proposed solution:

Kubernetes
create an OCI (Open Container Initiative) compliant image, usually created by using Docker
deploy a Kubernetes cluster with a valid ingress controller for the routing of requests
deploy an observability stack, including logs and metrics
create the YAML manifests for the application deployment
create a CI/CD pipeline to push the Kubernetes resources to the cluster
Cloud Foundry
write a manifest file to provide main application deployment parameters
deploy Cloud Foundry or use Cloud Foundry PaaS solutions from 3rd part vendors
deploy the application to Cloud Foundry (via CLI or UI)
Note: Cloud Foundry will create the OCI compliant image by default, and it will provide the routing capacities as well.
Cloud Foundry provides a better developer experience for application deployment, as it offers a greater level of component abstraction (no need to manage the underlying infrastructure). However, a PaaS solution locks-in the customer to a specific vendor. On the other side, Kubernetes offers full control over the container orchestration, providing more flexible management of the application.

Edge Case: Function as a Service

Summary
An organization will always explore the most efficient offering to deploy a product to consumers. PaaS solutions are lightweight on initial setup, as a team can release the code in production within days.

However, there are use cases where customers interact with a service only once a day or for a couple of hours within a day. For example, a service to update a timetable with the new bus schedule once a day. In this case, using a PaaS offering has one major downside: it is not cost-efficient. For example, with Cloud Foundry there will always be an instance of the application up and running, even if the service is used once a day. However, the team is billed for a full day.

For this scenario, a FaaS or Function as a Service is a more suitable offering. FaaS is an event-driven cloud-computing service that allows the execution of code without any management of the infrastructure and configuration files. As a result, the timetable update service is invoked only once a day, and for the rest of the time, there are no replicas of this service. A team will be billed only for the time the service is executed.

Popular FaaS solutions are AWS Lambda, Azure Functions, Cloud Functions from GCP, and many more.

Throughout the release process, a FaaS solution only requires the application code that is built and executed immediately. In comparison with a PaaS offering, this FaaS has a quicker usability rate, as no data management or configuration files are necessary.

Diagram of FaaS offering dependencies to deploy an application
FaaS dependencies to deploy an application

New Terms
FaaS or Function as a Service - event-driven cloud-computing service that requires only the application code to execute successfully.

Big Picture: Application Releases

Summary
Up to this stage, we have practiced the packaging of an application using Docker and its deployment to a Kubernetes cluster using kubectl commands. As well, we have explored the simplified developer experience of application release with Cloud Foundry. However, in both cases, a user has to manually trigger and complete all the operations. This is not sustainable if tens and hundreds of releases are performed within a day. Automation of the release process is fundamental!

In the case of a PaaS offering, the release of a new feature is managed by the provider. For example, Cloud Foundry monitors the repository with the source code, and when a new commit is identified, the user can easily deploy the latest changes with a click of a button. On the other side, releasing an application to a Kubernetes cluster consists of a series of manually typed docker and kubectl commands. At this stage, this approach has no automation integrated.

In this lesson, we will not cover how a PaaS automates the release process, since this is already solutionized by the 3rd party providers. Instead, we will focus on building a delivery pipeline to automate the deployment to Kubernetes using cloud-native tooling.

Continuous Application Deployment

Summary
Every company has the same goal: to deliver value to customers and maintain customer satisfaction. To achieve this, an organization needs to be fast in integrating customer feedback and release new features.

It is possible to manually deploy every release for a small product. However, this is not viable for a product that has thousands of microservices developed by hundreds of engineers. A delivery pipeline is essential for continuous and automated deployment of new functionalities.

A delivery pipeline includes stages that can test, validate, package, and push new features to a production environment. It is common practice for the main branch commits to proceed through all stages of the pipeline to reach the end-users. Overall, a delivery pipeline is triggered when a new commit is available. The new changes should traverse the following stages:

Build - compile the application source code and its dependencies. If this stage fails the developer should address it immediately as there might be missing dependencies or errors in the code.
Test - run a suite of tests, such as unit testing, integration, UI, smoke, or security tests. These tests aim to validate the behavior of the code. If this stage fails, then developers must correct it to prevent dysfunctional code from reaching the end-users.
Package - create an executable that contains the latest code and its dependencies. This is a runnable instance of the application that can be deployed to end-users.
Deploy - push the packaged application to one or more environments, such as sandbox, staging, and production. Usually, the sandbox and staging deployments are automatic, and the production deployment requires engineering validation and triggering.
It is common practice to push an application through multiple environments before it reaches the end-users. Usually, these are categorized as follows:

Sandbox - development environment, where new changes can be tested with minimal risk.
Staging - an environment identical to production, and where a release can be simulated without affecting the end-user experience.
Production - customer-facing environment and any changes in this environment will affect the customer experience.
Diagram of the Continuous Deployment pipeline and included stages 
Continuous Deployment pipeline

Overall, a delivery pipeline consists of two phases:

Continuous Integration (or CI) includes the build, test, and package stages.
Continuous Delivery (or CD) handles the deploy stage.
Advantages of a CI/CD pipeline
Frequent releases - automation enables engineers to ship new code as soon as it's available and improves responsiveness to customer feedback.
Less risk - automation of releases eliminates the need for manual intervention and configuration.
Developer productivity - a structured release process allows every product to be released independently of other components
New Terms
Continuous Integration - a mechanism that produces the package of an application that can be deployed.
Continuous Delivery - a mechanism to push the packaged application through multiple environments, including production.
Continuous Deployment - a procedure that contains the Continuous Integration and Continuous Delivery of a product.

The CI Fundamentals

Summary
Continuous Integration (CI) is a mechanism that produces the package of an application that can be deployed to consumers. As such, every commit to the main branch is built, tested, and packaged, if it meets the expected behavior. Within the cloud-native, the result of Continuous Integration represents a Docker image or an artifact that is OCI compliant.

Let's explore the commands and tools associated with each Continuous Integration stage!

Diagram of stages included in the Continuous Integration
Continuous Integration stages

Build
The build stage compiles the application source code and associated dependencies. We have explored this stage as part of the Dockerfile. For example, the Dockerfile for the Python hello-world application instructed the installation of dependencies from requirements.txt file and execution of the app.py at the container start.

# use pip to install any application dependencies 
RUN pip install -r requirements.txt

# execute command  on the container start
CMD [ "python", "app.py" ]
Test
The technology landscape provides an abundance of frameworks, libraries, and tools to test and validate the behavior of an application. For Python application, some of the well-known frameworks are:

pytest - for functional testing of the application
pylint - for static code analysts of the application codebase
Package
The result of the package stage is an executable that contains the latest features and their dependencies. With Docker, this stage is implemented using docker build and docker push commands. These create a Docker image using a Dockerfile, and stores the image to a registry, such as DockerHub. For example, to create and store the image for Python hello-world application, the following commands are used:

# build an image using a Dockerfile
docker build -t python-helloworld .

# store and distribute an image using DockerHub
docker push pixelpotato/python-helloworld:v1.0.0
Note: Buildbacks does not require a Dockerfile to create an OCI compliant image or artifact.

Github Actions

Summary
There are plenty of tools that automate the Continuous Integration stages, such as Jenkins, CircleCI, Concourse, and Spinnaker. However, in this lesson, we will explore GitHub Actions to build, test, and package an application.

GitHub Actions are event-driven workflows that can be executed when a new commit is available, on external or scheduled events. These can be easily integrated within any repository and provide immediate feedback if a new commit passes the quality check. Additionally, GitHub Actions are supported for multiple programming languages and can offer tailored notifications (e.g. in Slack) and status badges for a project.

A GitHub Action consists of one or more jobs. A job contains a sequence of steps that execute standalone commands, known as actions. When an event occurs, the GitHub Action is triggered and executes the sequence of commands to perform an operation, such as code build or test.

Diagram of the GitHub Actions structure 
GitHub Actions structure

Let's configure a GitHub Action that prints the Python version!

GitHub Actions are configured using YAML syntax, hence uses the .yaml or .yml file extensions. These files are stored in .github/workflows directory within the code repository. Within this folder, the python-version.yml contains the following sections:

## file location and name: # .github/workflows/python-version.yml

##  Named of the workflow.
name: Python version
## Set the trigger policy.
## In this case, the workflow is execute on a `push` event,
## or when a new commit is pushed to the repository
on: [push]
## List the steps to be executed by the workflow
jobs:
  ## Set the name of the job
  check-python-version:
    ## Configure the operating system the workflow should run on.
    ## In this case, the job on Ubuntu
    runs-on: ubuntu-latest
    ## Define a sequence of steps to be executed 
    steps:
      ## Use the public `checkout` action in version v2  
      ## to checkout the existing code in the repository
      - uses: actions/checkout@v2
      ## Use the public `setup-python` action  in version v2  
      ## to install python on the  Ubuntu based environment 
      - uses: actions/setup-python@v2
      ## Executes the `python --version` command
      - run: python --version
On the successful execution of the workflow, the Python version is printed. For example, Python 3.9.0.

Github Actions Walkthrough
Note: To follow this demo make sure you fork the course repository and reference the python-helloworld application.

This demo provides a step-by-step guide of how to write a GitHub Action to run a suite of pytests.

Pytest is a framework that is used to write functional testing for an application. In this example, within the test_with_pytest.py we create a mock test that will always execute successfully.


Summary
## Define a test that will always pass successfully
def test_always_passes():
    assert True
Once we have completed writing the test, we can construct a GitHub Action that will execute the tests using pytest tool. For this purpose, a new workflow is defined in the pytest.yml file within the .github/workflows directory.

To trigger the workflow a new commit is necessary (e.g. editing the README.md fie). On the successful execution of the GitHub Action, we should see an output mentioning that all the test passed successfully (as expected):

Run pytest
============================= test session starts ==============================
platform linux -- Python 3.8.6, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
rootdir: /home/runner/work/nd064_course_1/nd064_course_1
collected 1 item

solutions/python-helloworld/test_with_pytest.py .                        [100%]

============================== 1 passed in 0.02s ===============================
Also, this demo showcases the "Python version" GitHub Action that was used as an example in the slides.

GitHub has a rich library of upstream actions that can be easily integrated with any repository. The suite includes a Build and push Docker images action which uses 3 main components:

login - to logging into DockerHub
setup-buildx - to use an extended Docker CLI build capabilities
setup-qemu - to enable the execution of different multi-architecture containers
The following snippet showcases the Docker build and push of the application, under .github/workflows/docker-build.yaml file:

# This is a basic workflow to help you get started with Actions

name: Docker Build and Push

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      -
        name: Checkout
        uses: actions/checkout@v2
      -
        name: Set up QEMU
        uses: docker/setup-qemu-action@v1
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      -
        name: Login to DockerHub
        uses: docker/login-action@v1 
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      -
        name: Build and push
        uses: docker/build-push-action@v2
        with:
          context: .
          file: ./Dockerfile
          platforms: linux/amd64
          push: true
          tags: {{ YOUR_DOCKERHUB_REPOSITORY }}/python-helloworld:latest
The Docker build and push workflow can be found in course repository. Make sure to move this file to .github/workflows/docker-build.yaml location to execute it.

The CD Fundamentals

Summary
Once an engineering team has automated the packaging of an application, the next phase is to release it to customers. Before the application is pushed to a production environment, it is important to check the functionality of an application when deployed and integrated with platform components. Only when the application meets the excepted behavior, it is deployed to a customer-facing environment. The process of propagating an application through multiple environments, until it reached the end-users, is known as the Continuous Delivery (or CD) stage.

It is common practice to push the code through at least 3 environments: sandbox, staging, and production. A reminder of each environment's purpose :

Sandbox - development environment, where new changes can be tested with minimal risk.
Staging - an environment identical to production, and where a release can be simulated without affecting the end-user experience.
Production - customer-facing environment and any changes in this environment will affect the customer experience.
The sandbox and staging environments are fully automated. As such, if the deployment to sandbox is successful and meets the expected behavior, then the code will be propagated to the staging automatically. However, the push to production requires engineering validation and triggering, as this is the environment that the end-users will interact with. The production deployment can be fully automated, however, doing so implies a high confidence rate that the code will not introduce customer-facing disruptions.

Diagram of Continuous Delivery stages 
Continuous Delivery stages

Within the deployment pipeline, Continuous Delivery covers the deploy stage. Throughout this course, we have practiced the deployment of an application while using kubectl commands.

Kubernetes CLI (kubectl), support the management of imperative and declarative configuration. With the imperative approach, a Python hello-world application is deployed by creating a Deployment resource and referencing the desired Docker image:

# deploy `python-helloworld` using the imperative approach 
kubectl create deploy python-helloworld --image=pixelpotato/python-helloworld:v1.0.0
On the other side, with the declarative approach, the Python hello-world Deployment is store in a YAML manifest and is created using the kubectl apply command:

# deploy `python-helloworld` using the declarative approach
kubectl apply -f deployment.yaml
Note: The declarative approach is the recommended way to deploy resources within a production environment. Hence, this configuration management technique will be referenced in the next sections.

Argo CD

Summary
The ecosystem is rich in the collection of tools that automate the Continuous Delivery stage, such as Jenkins, CircleCI, Concourse, and Spinnaker. However, in this lesson, we will explore ArgoCD to propagate an application to multiple Kubernetes clusters.

ArgoCD is a declarative Continuous Delivery tool for Kubernetes, which follows the GitOps patterns. As such, ArgoCD operates on configuration stored in manifests (declarative) and uses Git repositories as the source of truth for the desired state of an application (GitOps pattern). As such, ArgoCD monitors the new commits to Git repositories and applies the latest changes reconciled automatically or on a manual trigger. Additionally, ArgoCD offers deployment to target environments and multiple clusters, and support for multiple config management tools (such as plain YAML, Helm, Kustomize).

For application deployment through multiple environments, ArgoCD provides CRDs (Custom Resource Definitions) to configure and manage the application release.

Project resource
The Project resource is a CRD that provides a logical grouping of applications, including access to source and destination repositories, and permissions to resources within the cluster. This resource is handy to segregate and control the deployment to multiple clusters.

Application resource
The Application resource that stores the configuration of how an application should be deployed and managed.
Let's explore how a Python hello-world application is deployed using an ArgoCD Application resource: Note: It is assumed that the declarative manifests for Python hello-world are available ((e.g. deploy.yaml, service.yaml, etc).

## API endpoint used to create the Application resource
apiVersion: argoproj.io/v1alpha1
kind: Application
## Set the name of the resource and namespace where it should be deployed.
## In this case the Application resource name is set to  `python-helloworld `
## and it is deployed in the `argocd` namespace
metadata:
  name: python-helloworld 
  namespace: argocd
spec:
  ## Set the target cluster and namespace to deploy the Python hello-world application.
  ## For example, the Python hello-world application is deployed in the `default` namespace
  ## within the local cluster or `https://kubernetes.default.svc`
  destination:
    namespace: default
    server: https://kubernetes.default.svc
  ## Set the project the application belongs to.
  ## In this case the `default` project is used.
  project: default
  ## Define the source of the Python hello-world application manifests.
  ## In this example, the manifests are stored in the `argocd-demo` repository
  ## under the `python-manifests` folder. Additionally, the latest commit within
  ## the repository is targeted or `HEAD`.
  source:
    path: python-manifests
    repoURL:
    https://github.com/kgamanji/argocd-demo
    targetRevision: HEAD
  # # Set the sync policy. 
  ## If left empty, the sync policy will default to manual.
  syncPolicy: {}
App of Apps
Diagram of a web-store Application that manages the configuration multiple microservices 
App of Apps: manage the Application CRDs for multiple microservices with a single Application CRD

ArgoCD provides an “app-of-apps” technique that enables a group of applications to be deployed and configured together. This technique is useful if a product is developed using a microservice-based architecture, and a single point of orchestration is necessary to deploy all microservices. For example, a Web-store Application CRD can be used to manage the Application CRDs for the UI, Login, and Payment units. In this case, one point of control is provisioned to release and manage multiple microservices.

New Terms
GitOps - an operating model that refers to the Git repositories as the source of truth for declarative infrastructure and applications.
Further Reading
Explore the GitOps pattern and ArgoCD resources:

ArgoCD Walkthrough
Installation

Summary
This demo is a walkthrough of the process of installing and accessing ArgoCD.

Here are some noteworthy steps:

Use the official ArgoCD install page
The YAML manifest for the NodePort service can be found under the argocd-server-nodeport.yaml file in the course repository
Access the ArgoCD UI by going to https://192.168.50.4:30008 or http://192.168.50.4:30007
When accessing the ArgoCD UI, a browser SSL warning is encountered. This is happening because the ArgoCD server is not setup with SSL certificates to authenticate the server. Hence, an insecure connection is established with the server. As a result, the warning prompt is encountered and you should just bypass the warning page
Login credentials can be retrieved using the steps in the credentials guide
Application Deployment
This demo provides a step by step guide on how to deploy an application using ArgoCD.

To follow the demo closely, use the following resources:

Python-manifests folder contains the YAML configuration for the Python hello-world application
argocd-python manifest for the Application CRD to used to deploy the Python hello-world application

Solution: The CD Fundamentals Exercise

ArgoCD is a Kubernetes-native tool that is capable of automating the life cycle management of application YAML manifests. With the GitOps model, configuration changes reconcile with minimal manual intervention, reaching an efficient deployment mechanism.

The following snippet highlights the commands to deploy ArgoCD and expose it using a NodePort service:

# deploy ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
# Create the NodePort service for ArgoCD server by using the 
# `kubectl apply -f argocd-server-nodeport.yaml` command
apiVersion: v1
kind: Service
metadata:
  annotations:
  labels:
    app.kubernetes.io/component: server
    app.kubernetes.io/name: argocd-server
    app.kubernetes.io/part-of: argocd
  name: argocd-server-nodeport
  namespace: argocd
spec:
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 8080
    nodePort: 30007
  - name: https
    port: 443
    protocol: TCP
    targetPort: 8080
    nodePort: 30008
  selector:
    app.kubernetes.io/name: argocd-server
  type: NodePort
The Nodeport service for ArgoCD can be found in the course repository.

Once logged in to the ArgoCD server, applications can be created. The declarative manifest for nginx-alpine Application CRD can be found below:

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-alpine
  namespace: argocd
spec:
  destination:
    namespace: default
    server: https://kubernetes.default.svc
  project: default
  source:
    path: exercises/manifests 
    repoURL: https://github.com/udacity/nd064_course_1 
    targetRevision: HEAD
  # Sync policy
  syncPolicy: {}
The nginx-alpine Application CRD can be found in the course repository.

An overview of the deployed nginx-alpine resources can be found below:

Configuration Managers

Summary
A CI/CD pipeline is essential to automate and standardize the application release process. New changes are propagated through multiple environments, including the production cluster, and ensure that the consumers can use the latest features. In an ideal situation, all clusters are similarly configured, such that the engineering team can inspect a realistic simulation of a production deployment. This implies that a set of nearly similar manifests are required for each cluster, sandbox, staging, and production. To reduce the management overhead of overseeing a similar suite configuration for each cluster, templating is necessary.

For example, to deploy the nginx-alpine application 4 resource manifests were necessary: Namespace, Deployment, Service, and Configmap. However, this suite of manifests represents the deployment to a single environment, e.g sandbox. The application should be propagated through staging and production environment, which reference a separate set of manifests. It is essential to ensure that the application configuration is tailored for each environment, for example, allocate more CPU and memory to the application in production since it handles more traffic, or have a different number of replicas for each cluster. In this case, an engineering team ends up managing 3 sets of manifests, 1 for each cluster.

Diagram showcasing the amount of manifests a team needs to manage for all enviroments
A team has to manage multiple manifests, one for each enviroment, to deploy an application successfully to ptoduction

However, the number of manifests grows exponentially when the application is distributed across multiple regions. As such, if the application is released in AP(Asia Pacific) and the US, a team ends up managing 9 different sets of manifests.

Diagram highlighting the growing amount of manifests a team has to manage if the application is distributed  across different regions
Application distribution across multiple regions implies a larger number of manifests that a team should manage

It is clear that it is necessary to introduce a mechanism to store and manage manifests in a reliable, scalable, and flexible way. This capability is offered by configuration management tools, such as:

Helm - package manager that templates exiting manifests, and uses input files to tailor configuration for each environment
Kustomize - a template-free mechanism that uses a base and multiple overlays, to manage the configuration for each environment
Jsonnet - a programming language, that enables the templating of manifests as JSON files, that can be easily consumed by Kubernetes
In the following sections, we will deep-dive into Helm, as the template manager of choice for this course.

Helm

Summary
Helm is a package manager, that manages Kubernetes manifests through charts. A Helm chart is a collection of YAML files that describe the state of multiple Kubernetes resources. These files can be parametrized using Go template.

A Helm chart is composed of the following files:

Chart.yaml - expose chart details, such as description, version, and dependencies
templates/ folder - contains templates YAML manifests for Kubernetes resources
values.yaml - default input configuration file for the chart. If no other values file is supplied, the parameters in this file will be used.
Helm Chart structure including a chart configuration, input file and templated manifests  
Helm Chart structure

Chart.yaml
A Chart.yaml file encompasses the details of the chart, such as version, description, and maintainer list. For example, a Python hello-world Helm chart contains the following Chart.yaml configuration:

## The chart API version
apiVersion: v1
## The name of the chart. 
## In this case,  the chart name is`python-helloworld `.
name: python-helloworld 
## A single-sentence description of this project
description: Install Python HelloWorld
## A list of keywords about this project to quickly identify the chart's capabilities.
keywords:
- python
- helloworld 
## The chart version, here set to `3.7.0`
version: 3.7.0
## List of maintainers, their names, and method of contact
maintainers:
- name: kgamanji 
  email: kgamanji@xyz.com
Templates folder
The templates/ folder is a directory containing templated YAML manifests, that require an input file to generate valid Kubernetes resources. For example, the templates/ folder contains the manifests for Deployment and Namespace resources, used to deploy the Python hello-world application:

templates/
├── deployment.yaml
└── namespace.yaml
These manifests can be templated using Go template. For example, instead of hardcoding the name of the Namespace, it can be parameterized as following:

apiVersion: v1
kind: Namespace
metadata:
  name: {{ .Values.namespace.name }}
Note: The .Values object is used to access the parameters passed from the input values.yaml file.

values.yaml
The values.yaml file contains default input parameters for a Helm chart. The parameters are consumed by the templated YAML manifests through the .Values object. The end result is a suite of valid Kubernetes resources that can be successfully deployed. For example, to provide the configuration for the Deployment and Namespace resources, the values.yaml has the following structure:

## provide the name of the namespace
namespace:
  name: test

## define the image to execute with the Deployment 
image:
  repository:
     pixelpotato/python-helloworld 
  tag: v1.0.0

## set the number of replicas for an application 
replicaCount: 3
It is noteworthy, that any fields within the Kubernetes resources can be parameterized. Additionally, the values.yaml file can be overwritten fully or partially, depending if changes are required to all parameters or just to a subset of them. If no override input file is provided, the Helm chart will fallback to using the default values.yaml file (included with the chart).

For example, to override the name of the Namespace to prod the following values-prod.yaml file can be constructed:

## override the name of the namespace
namespace:
  name: prod
The end result will be a valid Kubernetes Namespace object:

apiVersion: v1
kind: Namespace
metadata:
  name: prod
Argo CD and Helm

Summary
So far, we have explored how an engineering team can use Helm charts to template the manifests for multiple clusters. The next stage consists of integrating the Helm charts in the deploy phase of the CI/CD pipeline.

ArgoCD supports the deployment of manifests that are managed by a Helm chart. To implement this approach, the Application CRD requires to change the source of manifests to a Helm chart. An example of the manifest can be found below:

[...]
  source:
    ## change the source of manifests to a Helm chart
    helm:
      ## define the input values file
      valueFiles:
      - values.yaml
    ## set the path to the folder where the Helm chart is stored
    path: solutions/helm/python-helloworld
    ## set the base repository that contains the Helm chart
    repoURL: https://github.com/udacity/nd064_course_1 
    targetRevision: HEAD
The full YAML representation of the Application CRD that deploys a Helm chart can be found in the course repository.

New Terms
Helm - package manager tool used to template a suite of Kubernetes manifests.
Helm chart - a collection of configuration, input, and templated YAML files used to deploy Kubernetes resources.
Solution: Configuration Managers
Create Helm Chart

Helm provides a powerful mechanism to inject values to templated YAML manifests.

The full Helm chart for nginx-deployment can found in the course repository.

The Helm chart is defined in the Chart.yaml file, which contains the API version, name and version of the chart:

apiVersion: v1
name: nginx-deployment
description: Install Nginx deployment manifests 
keywords:
- nginx 
version: 1.0.0
maintainers:
- name: kgamanji 
An example of the values.yaml file can be found below:

namespace:
  name: demo

service:
  port: 8111
  type: ClusterIP

image:
  repository: nginx 
  tag: alpine
  pullPolicy: IfNotPresent

replicaCount: 3

resources:
  requests:
    cpu: 50m
    memory: 256Mi

configmap:
  data: "version: alpine"
The above configuration represents the default parameters of application deployment if it is not overwritten by a different values file.

Below is an example of the values-prod.yaml file, which will override the default parameters:

namespace:
  name: prod 

service:
  port: 80
  type: ClusterIP

image:
  repository: nginx 
  tag: 1.17.0
  pullPolicy: IfNotPresent

replicaCount: 2

resources:
  requests:
    cpu: 70m
    memory: 256Mi

configmap:
  data: "version: 1.17.0"
The values-staging.yaml can be found in the course repository.

Deploy Helm Chart

And finally, here is ArgoCD application CRD for the nginx-prod deployment:

apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-prod
  namespace: argocd
spec:
  destination:
    namespace: default
    server: https://kubernetes.default.svc
  project: default
  source:
    helm:
      valueFiles:
      - values-prod.yaml
    path: helm
    repoURL: https://github.com/kgamanji/argocd-demo
    targetRevision: HEAD
The nginx-staging.yaml Application for ArgoCD can be found in the course repository.

Edge Case: Push and Pull methodologies for CI/CD

Summary
Within the CI/CD ecosystem, tools have a variate level of capabilities that offer the deployment of an application to production environments. At a high level, these tools are using a push-based or pull-based model to release new features.

Let's explore each CI/CD model in more detail!

Push-based CI/CD
In a push-based model, as shown in the image below, the developer commits new code to the Git repository (1), which triggers the Continuous Integration stages (2). The code is packaged and distributed using an image registry, such as DockerHub (3). The Continuous Delivery stage is triggered once the YAML manifests are updated to reference the new image tag (4). A Continuous Delivery tool then pushed the updated manifests to multiple clusters (5).

Flow diagram showcasing how the push-based CI/CD model works 
Push-based CI/CD workflow

This model is fully operational and many tools within the ecosystem offer this deployment approach, e.g. Jenkins and CircleCI. However, there is one downside to this model: changes should be actively propagated to all environments. If this is not fulfilled, a scenario might be reached where multiple changes need to be deployed to production, which increases the failure rate and complicated the recovery procedures. Hence, wide awareness is required of features pushed to a production environment.

Pull-based CI/CD
In a pull-based CI/CD approach, the release process is still be triggered by a developer that pushed new features to the source code (1). The package (2) of the application is similar, resulting in a new image stored in DockerHub (3). However, once the YAML manifests are updated with the new image tag, a pull-based Continuous Delivery tool identifies new changes (4) and applies them to a Kubernetes cluster (5). As a result, this simplifies the process of application release, as new features can be applied automatically as soon as they are available. Tools that offer this CI/CD model are ArgoCD and Flux.

Flow diagram showcasing how the pull-based CI/CD model works 
Pull-based CI/CD workflow

It is paramount to build a deployment pipeline that fits the business requirements closely and automates the release process. There is no "golden path" that would cover all engineering requirements. However, the pull and push-based CI/CD tools contribute to the ultimate goal to ships code securely, automatically, and reliably.

Lesson Conclusion

Summary
Once a team has developed a product, it is paramount to automate the release process. The building, testing, packaging, and deploying an application to multiple clusters should be highly automated. Building a structured and well-defined CI/CD process is the key to a successful product release. In this lesson, we have explored GitHub Actions to implement the Continuous Integration stages and ArgoCD to perform the Continuous Delivery stages. Additionally, we have covered Helm, as a template configuration manager, that allows the parameterization of YAML manifests and their easy deployment across multiple Kubernetes clusters.

Overall, in this lesson we have explored:

Continuous Application Deployment
The CI Fundamentals
The CD Fundamentals
Configuration Managers
New Terms
Continuous Integration - a mechanism that produces the package of an application that can be deployed.
Continuous Delivery - a mechanism to push the packaged application through multiple environments, including production.
Continuous Deployment - a procedure that contains the Continuous Integration and Continuous Delivery of a product.
GitOps - an operating model that refers to the Git repositories as the source of truth for declarative infrastructure and applications.
Helm - package manager tool used to template a suite of Kubernetes manifests.
Helm chart - a collection of configuration, input, and templated YAML files used to deploy Kubernetes resources.

Summary
Throughout the Microservice Fundamentals course, we walked through a realistic example of how to choose an architecture for an application, package it using Docker, and deployed it to a Kubernetes cluster using a CI/CD pipeline.

We have started off with an overview of the cloud-native ecosystem and the tools it hosts. Then we've learned different application designs, such as monoliths and microservice, and implied trade-offs. We then moved to package an application using Docker and deploy it to a Kubernetes cluster using imperative and declarative configurations. Then, we transitioned into Platform as a Service (or PaaS) solutions and explored Cloud Foundry as an approach to deploy an application without worrying about the underlying infrastructure. And we finished this course, by practicing cloud-native tooling to construct a CI/CD pipeline. We deep-dived into GitHub Actions and ArgoCD and explored template configuration managers, such as Helm.

Microservice Fundamentals course outline
Microservice Fundamentals course outline

Overall, in this course we have covered the following lessons:

Welcome
Architecture Considerations
Container Orchestration
Open Source PaaS
Cloud Native CI/CD
"""