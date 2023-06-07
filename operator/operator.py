import time
from kubernetes import client, config, watch

def create_pod(cat_name, cat_colour,cat_kind):
    config.load_incluster_config() # Load the Kubernetes configuration from the default location
    
    api_instance = client.CoreV1Api()
    
    # Define the Pod spec
    pod_manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": f"cat-pod-{cat_name}",
        },
        "spec": {
            "containers": [
                {
                    "name": "cat-container",
                    "image": "nginx",
                    "env": [
                        {
                            "name": "CAT_NAME",
                            "value": cat_name,
                        },
                        {
                            "name": "CAT_COLOUR",
                            "value": cat_colour,
                        },
                        {
                            "name": "CAT_KIND",
                            "value": cat_kind,
                        },
                    ],
                }
            ]
        }
    }

    api_instance.create_namespaced_pod(
        body=pod_manifest,
        namespace="default"
    )
    
    print(f"Created Pod: cat-pod-{cat_name}")

def delete_pod(pod_name):
    config.load_incluster_config()  # Load the Kubernetes configuration from the default location
    
    api_instance = client.CoreV1Api()
    
    api_instance.delete_namespaced_pod(
        name=pod_name,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy="Foreground",
            grace_period_seconds=5
        )
    )
    
    print(f"Deleted Pod: {pod_name}")

def watch_crd():
    config.load_incluster_config()  # Load the Kubernetes configuration from the default location
    
    api_instance = client.CustomObjectsApi()
    
    resource_version = ''
    while True:
        # Watch the Cat resource events
        stream = watch.Watch().stream(
            api_instance.list_cluster_custom_object,
            group='example.crd.com',
            version='v1',
            plural='cats',
            resource_version=resource_version,
        )

        for event in stream:
            cat = event['object']
            event_type = event['type']
            metadata = cat['metadata']
            cat_name = metadata['name']
            cat_colour = cat['spec']['colour']
            cat_kind = cat['spec']['kind']
            
            if event_type == 'ADDED':
                create_pod(cat_name, cat_colour,cat_kind)
            elif event_type == 'DELETED':
                pod_name = f"cat-pod-{cat_name}"
                delete_pod(pod_name)
        
            resource_version = metadata['resourceVersion']

        time.sleep(1)

if __name__ == '__main__':
    watch_crd()
