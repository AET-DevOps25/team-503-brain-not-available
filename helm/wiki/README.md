# Helm Chart for Wiki

This Helm chart deploys a set of services for the Wiki project, including a database, monitoring tools, and a user interface for managing and visualizing data.

## Prerequisites

- Kubernetes cluster
- Helm 3.x installed

## Installation

To install the chart, use the following command:

```bash
helm install <release-name> ./wiki
```

Replace `<release-name>` with a name for your release.

## Configuration

You can customize the deployment by modifying the `values.yaml` file. This file contains default configuration values for the chart.

## Services Included

- **Database**: MariaDB for data storage.
- **phpMyAdmin**: Web interface for managing the database.
- **Grafana**: Visualization tool for monitoring data.
- **Prometheus**: Monitoring and alerting toolkit.
- **cAdvisor**: Resource usage and performance characteristics of running containers.
- **Node Exporter**: Exposes hardware and OS metrics.
- **gpt4all**: AI model service.
- **Weaviate**: Vector search engine.

## Accessing the Services

After installation, you can access the services using the following URLs:

- phpMyAdmin: `http://<your-k8s-cluster-ip>:8088`
- Grafana: `http://<your-k8s-cluster-ip>:3000`
- Prometheus: `http://<your-k8s-cluster-ip>:9090`
- cAdvisor: `http://<your-k8s-cluster-ip>:8081`
- Node Exporter: `http://<your-k8s-cluster-ip>:9100`
- gpt4all: `http://<your-k8s-cluster-ip>:5000`
- Weaviate: `http://<your-k8s-cluster-ip>:8080`

## License

This project is licensed under the MIT License. See the LICENSE file for details.