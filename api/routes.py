from fastapi import APIRouter
from services import docker_service as ds
from schemas.docker_schema import DockerImageSchema, DockerLoginSchema

router = APIRouter()


# Docker Hub Login
@router.post("/login")
def login_to_docker(payload: DockerLoginSchema):
    return ds.docker_login(payload.username, payload.password)


# Build Image and Push to Docker Hub
@router.post("/build_and_push")
def build_and_push_image(payload: DockerImageSchema):
    # Step 1: Build the image from the Dockerfile
    build_response = ds.build_image(dockerfile_path="path_to_your_dockerfile", image_name=payload.image_name)

    # Step 2: Push the image to Docker Hub
    if "error" not in build_response:
        push_response = ds.push_image(payload.image_name, payload.repository_name)
        return push_response

    return build_response


# Image Endpoints
@router.post("/pull")
def pull_image(payload: DockerImageSchema):
    return ds.pull_image(payload.image_name)


@router.get("/images")
def get_images():
    return ds.list_images()


@router.delete("/images")
def remove_image(payload: DockerImageSchema):
    return ds.delete_image(payload.image_name)


# Logs & Docker PS
@router.get("/logs/{container_name}")
def get_logs(container_name: str):
    return ds.get_logs(container_name)


@router.get("/ps")
def docker_ps():
    return ds.docker_ps()
