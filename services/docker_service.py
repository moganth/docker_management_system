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

def push_image(image_name: str):
    try:
        response = client.images.push(image_name)
        return f"Image '{image_name}' pushed to Docker Hub.\nResponse:\n{response}"
    except Exception as e:
        raise Exception(f"Push failed: {e}")


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
