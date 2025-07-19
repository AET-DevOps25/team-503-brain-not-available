# Team 503 Wiki Platform

A collaborative, AI-powered wiki platform for organizations, inspired by Confluence. Employees can create, edit, and organize wiki pages, and leverage integrated GenAI to generate content, improve writing, and answer questions based on the wiki's knowledge.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Local Deployment](#local-deployment)
- [Deployment to Rancher/Kubernetes](#deployment-to-rancherkubernetes)
- [Usage](#usage)
- [License](#license)

---

## Features

- **Wiki Pages:** Create, edit, and organize pages in a folder-like structure with tags.
- **User Management:** Register, authenticate, and manage users.
- **AI Integration:** Use GenAI to generate content, improve writing, and answer questions based on wiki content.
- **Search:** Quickly find relevant pages.
- **Monitoring:** Integrated monitoring stack (Prometheus, Grafana, etc.).
- **Database:** MariaDB for persistent storage.

---

## Project Structure

```
.
├── .github/         # GitHub workflows, etc.
├── .vscode/         # VSCode workspace settings and recommendations
├── backend/         # Spring Boot REST API for wiki, users, and authentication
├── client/          # Frontend (likely Vue/React) for user interaction
├── genai/           # GenAI (GPT4All + Weaviate) for AI-powered features
├── helm/            # Helm charts for Kubernetes deployment
├── monitoring/      # Monitoring stack (Prometheus, Grafana, etc.)
├── server/          # (Reserved for additional backend services)
├── UML/             # UML diagrams and documentation
├── README.md        # This file
├── docker-compose.yml
└── ...
```

---

## Local Deployment

### Prerequisites

- Docker & Docker Compose
- Java 21+ (for backend development)
- Node.js (for client development)

### 1. Clone the Repository

```sh
git clone <repo-url>
cd team-503-brain-not-available
```

### 2. Start All Services

```sh
docker-compose build
docker-compose up
```

This will start:
- Backend API (Spring Boot)
- Frontend client
- GenAI (gpt4all + Weaviate)
- MariaDB database
- Monitoring stack (Prometheus, Grafana, etc.)

### 3. Access the Services

- **Wiki Frontend:** http://localhost:80
- **phpMyAdmin:** http://localhost:8088
- **Grafana:** http://localhost:3000

---

## Deployment to ASE Rancher Cluster

### 1. Package and Deploy with Helm

```sh
cd helm/wiki
helm upgrade --install wiki ./helm/wiki --namespace wiki --create-namespace --recreate-pods
```

- All services (backend, frontend, GenAI, DB, monitoring) are deployed as part of the Helm chart.

### 2. Access Services

- **Wiki Frontend:** https://wiki-devops25.student.k8s.aet.cit.tum.de/
- **Grafana:** https://wiki-devops25.student.k8s.aet.cit.tum.de/grafana
- **phpMyAdmin:** https://phpmyadmin.wiki-devops25.student.k8s.aet.cit.tum.de/

---

## Deployment to AWS

- Use an ubuntu EC2 instance with enouth storage for the AI, we use t3.medium with 30GB storage.

- Set up the instance:
   ```sh
   # Add Docker's official GPG key:
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # Add the repository to Apt sources:
   echo \
   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
   $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update

   # Install Docker
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

   # Allow user to run Docker commands
   sudo usermod -a -G docker ubuntu
   ```

- open port _1111_ for accessing the API in the AWS settings

- Configure the _AWS_EC2_PRIVATE_KEY_ secret and the _EC2_PUBLIC_IP_ variable in GitHub

- Run the _Deploy Docker Images to AWS_ action

---

## Usage

1. **Login:** Login to your account to access and edit wiki pages.
2. **Create/Edit Pages:** Use the frontend to add or modify wiki articles.
3. **Organize Content:** Group pages in folders and add tags for easy navigation.
4. **AI Assistance:**
   - Generate new content from bullet points or drafts.
   - Improve writing quality with AI suggestions.
   - Ask questions; GenAI will answer based on wiki content.
5. **Search:** Use the search bar to find relevant pages quickly.
6. **Monitor:** Access Grafana dashboards for system health and usage metrics.

---

## Responsibilities

- client (Manuel)
- backend (Felix)
- genai (Andreas)
- monitoring (Andreas)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for