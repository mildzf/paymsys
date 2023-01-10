# Pull base image
FROM python:3.10-alpine


# Set Python environment variable
#FROM python:${PYTHON_VERSION}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set work directory called `code`

RUN mkdir -p /code
WORKDIR /code

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN apk add py3-pip py3-pillow py3-cffi py3-brotli gcc musl-dev python3-dev pango
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

# Copy local project
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Use gunicorn on port 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "django_project.wsgi"]
