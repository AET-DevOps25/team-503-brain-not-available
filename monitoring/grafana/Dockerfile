FROM grafana/grafana:latest

EXPOSE 3000

# Environment variables
ENV GF_SECURITY_ADMIN_PASSWORD=admin \
    GF_USERS_ALLOW_SIGN_UP=false \
    GF_AUTH_ANONYMOUS_ENABLED=true \
    GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer \
    GF_AUTH_ANONYMOUS_ORG_ID=1 \
    GF_SERVER_SERVE_FROM_SUB_PATH=true

# Copy provisioning files into the image
COPY provisioning/datasources /etc/grafana/provisioning/datasources
COPY provisioning/dashboards /etc/grafana/provisioning/dashboards

VOLUME ["/var/lib/grafana"]