# Monitoring Service

This directory contains the monitoring stack for the project, enabling observability and resource tracking for all major services.

## Components

- **Prometheus**: Collects and stores metrics from containers and services.
  - Configuration: [`monitoring/prometheus/prometheus.yml`](prometheus/prometheus.yml)
  - Dockerfile: [`monitoring/prometheus/Dockerfile`](prometheus/Dockerfile)
- **Grafana**: Visualizes metrics and provides dashboards for monitoring.
  - Dashboard provisioning: [`monitoring/grafana/provisioning/dashboards/dashboard.json`](grafana/provisioning/dashboards/dashboard.json)
  - Dockerfile: [`monitoring/grafana/Dockerfile`](grafana/Dockerfile)
- **cAdvisor**: Exposes container resource usage and performance metrics.
- **Node Exporter**: Collects hardware and OS metrics from the host.

## Accessing Grafana

Once the monitoring stack is running, access the Grafana dashboard at: http://localhost:3000

The main dashboard is titled **"Container Status & Resource Usage"** and is automatically loaded from the provisioning directory.