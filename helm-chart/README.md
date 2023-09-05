

## Helm chart for running doccano docker image

How to run:
1. In the helm-chart directory run ``` helm dependency update ```
2. ``` helm upgrade --install doccano-app . ```

If you are using microk8s then start both of the above commands like so: ``` microk8s helm <commands> ``` or ```sudo microk8s <commands> ``` depending on your user privileges.

### Docker image options

The doccano version and repository can be changed in this line of the ``` values.yml ``` file:
```
repository: doccano/doccano
tag: "1.8"
```
This is useful if you have built your own image and pushed it to a cloud/local container image registry.
