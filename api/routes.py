import docker
from fastapi import HTTPException
from fastapi import APIRouter
from services import docker_service as ds
from schemas.docker_schema import DockerImageSchema, DockerLoginSchema, BuildImagePayload, PushImagePayload

client = docker.from_env()
router = APIRouter()


# Docker Hub Login
@router.post("/login")
def login_to_docker(payload: DockerLoginSchema):
    return ds.docker_login(payload.username, payload.password)


@router.post("/docker/build")
def build_image(payload: BuildImagePayload):
    try:
        build_response = ds.build_image(
            dockerfile_path=payload.dockerfile_path,
            image_name=payload.image_name,
            dockerfile_name=payload.dockerfile_name
        )
        return {"message": build_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
