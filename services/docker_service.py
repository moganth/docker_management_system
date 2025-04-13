import docker
from docker.errors import APIError
from fastapi.responses import JSONResponse

from config import DOCKER_REGISTRY

client = docker.from_env()

# Docker Login
def docker_login(username: str, password: str):
    try:
        return client.login(username=username, password=password, registry=DOCKER_REGISTRY)
    except APIError as e:
        return {"error": str(e)}

# Image Operations
def pull_image(image_name: str):
    result = client.images.pull(image_name)
    return JSONResponse(content={"status": "success", "image": str(result)})


def push_image(image_name: str):
    image = client.images.get(image_name)
    return client.images.push(image.tags[0])

def list_images():
    return client.images.list()

def delete_image(image_name: str):
    return client.images.remove(image=image_name, force=True)

# Container Operations
def run_container(image_name: str, container_name: str):
    return client.containers.run(image_name, name=container_name, detach=True)

def start_container(container_name: str):
    container = client.containers.get(container_name)
    return container.start()

def stop_container(container_name: str):
    container = client.containers.get(container_name)
    return container.stop()

def restart_container(container_name: str):
    container = client.containers.get(container_name)
    return container.restart()

def list_containers(all=True):
    return client.containers.list(all=all)

def delete_container(container_name: str):
    container = client.containers.get(container_name)
    return container.remove(force=True)

# Volume Operations
def create_volume(volume_name: str):
    return client.volumes.create(name=volume_name)

def list_volumes():
    return client.volumes.list()

def delete_volume(volume_name: str):
    volume = client.volumes.get(volume_name)
    return volume.remove(force=True)

# Logs & PS
def get_logs(container_name: str):
    container = client.containers.get(container_name)
    return container.logs().decode()

def docker_ps():
    return [c.name for c in client.containers.list()]
