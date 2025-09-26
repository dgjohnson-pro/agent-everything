FROM ollama/ollama:latest
## Run as need

# USER root
# Ensure ca-certificates exists, install your CA, update trust
# RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
# COPY my-root-ca.crt /usr/local/share/ca-certificates/
# RUN update-ca-certificates

# Help Go/other libs find the bundle
# ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
# ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# If you use a corporate proxy, also set:
# ENV HTTP_PROXY=http://proxy.example.com:port  
# ENV HTTPS_PROXY=http://proxy.example.com:port  
# ENV NO_PROXY=localhost,127.0.0.1,ollama
