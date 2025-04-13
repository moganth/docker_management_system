from fastapi import APIRouter
from services import docker_service as ds
from schemas.docker_schema import (
    ImageSchema, ContainerSchema, VolumeSchema, DockerLoginSchema
)

router = APIRouter()

# Docker Hub Login
@router.post("/login")
def login_to_docker(payload: DockerLoginSchema):
    return ds.docker_login(payload.username, payload.password)

# Image Endpoints
@router.post("/pull")
def pull_image(payload: ImageSchema):
    return ds.pull_image(payload.image_name)

@router.post("/push")
def push_image(payload: ImageSchema):
    return ds.push_image(payload.image_name)

@router.get("/images")
def get_images():
    return ds.list_images()

@router.delete("/images")
def remove_image(payload: ImageSchema):
    return ds.delete_image(payload.image_name)

# Container Endpoints
@router.post("/run")
def run_container(payload: ContainerSchema):
    return ds.run_container(payload.image_name, payload.container_name)

@router.post("/start")
def start_container(payload: ContainerSchema):
    return ds.start_container(payload.container_name)

@router.post("/stop")
def stop_container(payload: ContainerSchema):
    return ds.stop_container(payload.container_name)

@router.post("/restart")
def restart_container(payload: ContainerSchema):
    return ds.restart_container(payload.container_name)

@router.get("/containers")
def list_all_containers():
    return ds.list_containers()

@router.delete("/containers")
def remove_container(payload: ContainerSchema):
    return ds.delete_container(payload.container_name)

# Volume Endpoints
@router.post("/volumes")
def create_volume(payload: VolumeSchema):
    return ds.create_volume(payload.volume_name)

@router.get("/volumes")
def list_volumes():
    return ds.list_volumes()

@router.delete("/volumes")
def delete_volume(payload: VolumeSchema):
    return ds.delete_volume(payload.volume_name)

# Logs & Docker PS
@router.get("/logs/{container_name}")
def get_logs(container_name: str):
    return ds.get_logs(container_name)

@router.get("/ps")
def docker_ps():
    return ds.docker_ps()
