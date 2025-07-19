# CI Actions

## Testing

CI actions that run tests for the client and the backend are executed when a Pull Request is created. 

## Linting

CI actions that lint the client and the backend code are executed when a Pull Request is created. 

## Build and Publish Docker Images

After merging a PR to `main`, a CI action builds all docker containers and pushes them to the GitHub Container Registry.

## ASE cluster deployment

After the `Build and Publish Docker Images` step, the helm deployment CI action is automatically run to update the deployment on the ASE cluster. Read more in the [Helm README](../../helm/wiki/README.md).

## AWS deployment

The CI action to update the AWS deployment is triggered manually. This action runs the wiki software using docker compose. Read more about the AWS deployment in the [project README](../../README.md).
