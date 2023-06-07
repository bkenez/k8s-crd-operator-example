# To use

1. Build docker image in operator dir and tag it cat-operator:v1
2. Apply crd.yaml to cluster
3. Apply the deployment, rbac, and sa yamls
4. Apply the cats, cat pods should be created
5. Delete a cat and its pod should also be deleted