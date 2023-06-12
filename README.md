# Example Helm Chart for CRD and Operator Deployment

This Helm chart allows you to deploy a Custom Resource Definition (CRD) and an Operator to a Kubernetes cluster. The Operator's job is to create a pod whenever an instance of the custom resource is created, as well as to delete the pod when the corresponding instance is deleted.

## Prerequisites

Before you begin, make sure you have the following:

- Kubernetes cluster up and running
- Helm installed and configured to work with your cluster

## Installation Steps

Follow these steps to deploy the CRD and Operator using the Helm chart:

1. Build Docker image: Navigate to the operator directory and build the Docker image for the Operator using the provided Dockerfile. Make sure you have Docker installed and running. You can use the following command:

   ```shell
   cd operator
   docker build -t your-image-tag .
   ```

   Replace `your-image-tag` with the desired tag for your Docker image. Push it to your repository of choice, or keep it local for testing.

2. Set the image in values.yaml: Open the `values.yaml` file in the root directory of this Helm chart. Find the `image` field and update it with the correct Docker image details. For example:

   ```yaml
    image: your-docker-repo/your-image:your-image-tag
   ```

   Replace `your-docker-repo/your-image` with the repository (if not locally testing) and image name where you pushed your Docker image, and `your-image-tag` with the specific tag you used. 

3. Install the Helm chart: Run the following command to install the chart in your Kubernetes cluster:

   ```shell
   helm install your-release-name .
   ```

   Replace `your-release-name` with the desired name for your Helm release.

4. Apply the custom resource instances: Create instances of the custom resource (cats) by applying the provided YAML files located in the `example-cats` folder within the repository. For example:

   ```shell
   kubectl apply -f example-cats/sprinkles.yaml
   ```

   This will create instances of the custom resource, and the Operator should create corresponding pods for each instance.

5. Verify pod creation: Use the following command to check if the pods have been created:

   ```shell
   kubectl get pods
   ```

   You should see pods with names corresponding to the created cat instances.

6. Delete a custom resource instance: Delete one of the custom resource instances using the following command:

   ```shell
   kubectl delete -f example-cats/sprinkles.yaml
   ```

   The Operator should detect the deletion and delete the corresponding pod.

7. Verify pod deletion: Use the following command to check if the pod has been deleted:

   ```shell
   kubectl get pods
   ```

   The pod associated with the deleted cat instance should no longer be present.

## Cleanup

To uninstall the Helm chart and remove all the deployed resources, run the following command:

```shell
helm uninstall your-release-name
```

Replace `your-release-name` with the name of your Helm release.
