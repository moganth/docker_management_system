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


# Build Image
def build_image(dockerfile_path: str, image_name: str):
    try:
        image, build_logs = client.images.build(path=dockerfile_path, tag=image_name)
        return {"status": "success", "image_id": str(image.id), "message": "Image built successfully"}
    except APIError as e:
        return {"error": str(e)}


# Push Image to Docker Hub
def push_image(image_name: str, repository_name: str):
    try:
        # Tag the image with the provided Docker Hub repository
        tagged_image = client.images.get(image_name)
        tagged_image.tag(repository_name, tag="latest")

        # Push the image to Docker Hub
        push_response = client.images.push(repository_name, tag="latest")
        return {"status": "success", "message": "Image pushed to Docker Hub", "response": push_response}
    except APIError as e:
        return {"error": str(e)}


# Pull Image
def pull_image(image_name: str):
    try:
        result = client.images.pull(image_name)
        return JSONResponse(content={"status": "success", "image": str(result)})
    except APIError as e:
        return {"error": str(e)}


# List Images
def list_images():
    return client.images.list()


# Delete Image
def delete_image(image_name: str):
    try:
        client.images.remove(image_name, force=True)
        return {"status": "success", "message": f"Image {image_name} removed"}
    except APIError as e:
        return {"error": str(e)}
