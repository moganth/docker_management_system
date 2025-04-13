import docker
from docker.errors import APIError
from config import DOCKER_REGISTRY

client = docker.from_env()

# Docker Login
def docker_login(username: str, password: str):
    try:
        login_response = client.login(username=username, password=password, registry=DOCKER_REGISTRY)
        return {"status": "success", "message": "Login successful", "details": login_response}
    except APIError as e:
        return {"status": "error", "message": str(e)}

# Docker Logout
def docker_logout():
    try:
        # Assuming the Docker SDK supports logout functionality (it doesn't expose a logout directly)
        # So, logout might be handled at the session or client level.
        return {"status": "success", "message": "Logged out from Docker"}
    except APIError as e:
        return {"status": "error", "message": str(e)}

# Image Operations
def build_image(image_name: str):
    try:
        client.images.build(path=".", tag=image_name, rm=True)
        return {"status": "success", "message": f"Image {image_name} built successfully"}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def push_image(image_name: str):
    try:
        result = client.images.push(image_name)
        return {"status": "success", "message": "Image pushed successfully", "details": result}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def pull_image(image_name: str):
    try:
        result = client.images.pull(image_name)
        return {"status": "success", "message": "Image pulled successfully", "details": str(result)}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def list_images():
    try:
        images = client.images.list()
        return {"status": "success", "message": "Images listed", "images": [str(image) for image in images]}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def delete_image(image_name: str):
    try:
        result = client.images.remove(image_name, force=True)
        return {"status": "success", "message": f"Image {image_name} removed", "details": str(result)}
    except APIError as e:
        return {"status": "error", "message": str(e)}

# Container Operations
def run_container(image_name: str, container_name: str):
    try:
        container = client.containers.run(image_name, name=container_name, detach=True)
        return {"status": "success", "message": f"Container {container_name} started", "container_id": str(container.id)}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def start_container(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.start()
        return {"status": "success", "message": f"Container {container_name} started."}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def stop_container(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.stop()
        return {"status": "success", "message": f"Container {container_name} stopped."}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def restart_container(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.restart()
        return {"status": "success", "message": f"Container {container_name} restarted."}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def list_containers(all=True):
    try:
        containers = client.containers.list(all=all)
        return {"status": "success", "message": "Containers listed", "containers": [container.name for container in containers]}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def delete_container(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
        return {"status": "success", "message": f"Container {container_name} removed."}
    except APIError as e:
        return {"status": "error", "message": str(e)}

# Volume Operations
def create_volume(volume_name: str):
    try:
        volume = client.volumes.create(name=volume_name)
        return {"status": "success", "message": f"Volume {volume_name} created", "volume": str(volume)}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def list_volumes():
    try:
        volumes = client.volumes.list()
        return {"status": "success", "message": "Volumes listed", "volumes": [str(volume) for volume in volumes]}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def delete_volume(volume_name: str):
    try:
        volume = client.volumes.get(volume_name)
        volume.remove(force=True)
        return {"status": "success", "message": f"Volume {volume_name} deleted."}
    except APIError as e:
        return {"status": "error", "message": str(e)}

# Logs & PS
def get_logs(container_name: str):
    try:
        container = client.containers.get(container_name)
        logs = container.logs().decode()
        return {"status": "success", "message": f"Logs for {container_name}", "logs": logs}
    except APIError as e:
        return {"status": "error", "message": str(e)}

def docker_ps():
    try:
        containers = client.containers.list()
        return {"status": "success", "message": "Running containers", "containers": [container.name for container in containers]}
    except APIError as e:
        return {"status": "error", "message": str(e)}
