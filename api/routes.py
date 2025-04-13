from http.client import HTTPException

from fastapi import APIRouter
from services import docker_service as ds
from schemas.docker_schema import DockerImageSchema, DockerLoginSchema, BuildImagePayload, PushImagePayload

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

@router.post("/docker/push")
def push_image(payload: PushImagePayload):
    try:
        push_response = ds.push_image(payload.image_name)
        return {"message": push_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
