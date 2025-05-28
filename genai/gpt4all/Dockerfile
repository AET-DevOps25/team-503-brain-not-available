FROM ubuntu:25.10

# Update systemm
RUN apt-get update && apt-get upgrade -y

# Install dependencies
RUN apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment and install dependencies
RUN python3 -m venv /venv && \
    /venv/bin/pip install gpt4all && \
    /venv/bin/pip install fastapi && \
    /venv/bin/pip install uvicorn && \
    /venv/bin/pip install weaviate-client && \

# Deploy the genAI component
COPY genAI.py /app/genAI.py

# Set PATH so the venv's python is default
ENV PATH="/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Set default command (change as needed)
CMD [ "python", "genAI.py" ]