# Use Python 3.13 slim as the base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables:
# - Prevent Python from writing pyc files
# - Ensure Python output is sent straight to terminal without buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy dependency files first for better build caching
# (This layer will only be rebuilt when these files change)
COPY pyproject.toml uv.lock README.md ./

# Copy application code
COPY my_package ./my_package/

# Install project dependencies using uv:
# - --system flag installs packages globally instead of in a virtual environment
# - The dot (.) installs the current project, which includes only core dependencies (not dev)
RUN uv pip install --system .

# Command to run when the container starts
# Run the main.py module from the my_package package
CMD ["python", "-m", "my_package.main"]
