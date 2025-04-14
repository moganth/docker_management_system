import docker
from docker.errors import APIError
from fastapi.responses import JSONResponse
from config import DOCKER_REGISTRY

client = docker.from_env()


# Docker Login
def docker_login(username: str, password: str):
    try:
        login_response = client.login(username=username, password=password, registry=DOCKER_REGISTRY)
        return {"status": "success", "message": "Logged in to Docker Hub"}
    except APIError as e:
        return {"error": str(e)}

# Push Image to Docker Hub
def build_image(dockerfile_path: str, image_name: str, dockerfile_name: str = "Dockerfile"):
    try:
        image, logs = client.images.build(
            path=dockerfile_path,
            tag=image_name,
            dockerfile=dockerfile_name,
            rm=True
        )
        log_output = ""
        for chunk in logs:
            if 'stream' in chunk:
                log_output += chunk['stream']
        return f"Image '{image_name}' built successfully.\nLogs:\n{log_output}"
    except Exception as e:
        raise Exception(f"Build failed: {e}")

def push_image(local_image_name: str, repository_name: str, username: str, password: str):
    try:
        # Login to Docker Hub
        client.login(username=username, password=password)

        # Tag the local image with the Docker Hub repository name
        image = client.images.get(local_image_name)
        image.tag(repository_name)

        # Push the image to Docker Hub
        response = client.images.push(repository_name)
        return f"Image '{local_image_name}' pushed as '{repository_name}' to Docker Hub.\nResponse:\n{response}"
    except Exception as e:
        raise Exception(f"Push failed: {e}")


def pull_image(image_name: str, repository_name: str):
    try:
        full_image_name = f"{repository_name}:{image_name.split(':')[-1]}"
        image = client.images.pull(full_image_name)
        return {"status": "success", "message": f"Image '{full_image_name}' pulled successfully"}
    except APIError as e:
        return {"error": str(e)}



# List Images
def list_images():
    images = client.images.list()
    image_list = []
    for img in images:
        image_list.append({
            "id": img.id,
            "tags": img.tags,
            "short_id": img.short_id
        })
    return image_list

# Delete Image
def delete_image(image_name: str):
    try:
        # Optional: validate image exists
        client.images.get(image_name)
        client.images.remove(image_name, force=True)
        return {"status": "success", "message": f"Image {image_name} removed"}
    except docker.errors.ImageNotFound:
        return {"error": f"Image {image_name} not found"}
    except APIError as e:
        return {"error": str(e)}


def get_logs(container_name: str):
    try:
        container = client.containers.get(container_name)
        logs = container.logs().decode('utf-8')
        return {"container": container_name, "logs": logs}
    except Exception as e:
        raise Exception(f"Failed to get logs for container '{container_name}': {e}")

def docker_ps():
    try:
        containers = client.containers.list()
        result = []
        for container in containers:
            result.append({
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags
            })
        return result
    except Exception as e:
        raise Exception(f"Failed to list containers: {e}")

# New Functions for Container Operations
def run_container(image_name: str, container_name: str, ports: dict = None, environment: dict = None):
    try:
        container = client.containers.run(image_name, name=container_name, ports=ports, environment=environment, detach=True)
        return {"status": "success", "message": f"Container '{container_name}' started successfully", "container_id": container.id}
    except Exception as e:
        return {"error": str(e)}

def stop_container(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.stop()
        return {"status": "success", "message": f"Container '{container_name}' stopped"}
    except Exception as e:
        return {"error": str(e)}

def start_container(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.start()
        return {"status": "success", "message": f"Container '{container_name}' started"}
    except Exception as e:
        return {"error": str(e)}

def restart_container(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.restart()
        return {"status": "success", "message": f"Container '{container_name}' restarted"}
    except Exception as e:
        return {"error": str(e)}

def remove_container(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.remove()
        return {"status": "success", "message": f"Container '{container_name}' removed"}
    except Exception as e:
        return {"error": str(e)}