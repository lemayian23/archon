FROM python:3.11-slim

WORKDIR /workspace

# Install minimal dependencies
RUN pip install pandas==2.1.3 numpy==1.25.2 plotly==5.17.0

# Create non-root user
RUN useradd -m -s /bin/bash archon
USER archon

# Set safe environment
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

CMD [\"python\", \"--version\"]
