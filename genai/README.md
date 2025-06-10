# Project Title: GenAI

## Overview
GenAI is a component that integrates a GPT based conversational AI with Weaviate, a vector search engine. This setup allows for efficient querying and interaction with AI-generated responses.

## Components

### gpt4all
- **Dockerfile**: Defines the Docker image for the gpt4all application. It uses Ubuntu as the base image, installs Python and necessary dependencies, creates a virtual environment, installs the gpt4all and Flask libraries, copies the `genAI.py` file into the image.
- **genAI.py**: Contains a Flask application that sets up a REST API endpoint `/chat`. It uses the GPT4All model to generate responses based on prompts received in POST requests.

### weaviate
- **Dockerfile**: Defines the Docker image for the Weaviate application. It uses a specific Weaviate image from a container registry and exposes ports 8080 and 50051.

### docker-compose.yml
- This file defines the services for the gpt4all and Weaviate containers, including the network configuration and port mappings to allow communication between the two services.

## Setup Instructions

2. **Build and Run the Containers**
   Use Docker Compose to build and run the services:
   ```
   docker-compose up --build
   ```

3. **Access the Services**
   - The gpt4all service will be available at `http://localhost:5000/chat`.
   - The Weaviate service will be available at `http://localhost:8080`.

## Usage
To interact with the gpt4all service, send a POST request to the `/chat` endpoint with a JSON body containing the prompt and optional max_tokens parameter. For example:
```json
{
  "prompt": "Hello, how can I help you?"
}
```