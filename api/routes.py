from fastapi import APIRouter, Form
from services import docker_service as ds
from schemas.docker_schema import DockerLoginSchema, ImageSchema, ContainerSchema, VolumeSchema

router = APIRouter()

# Docker Hub Login
@router.post("/login")
def login_to_docker(payload: DockerLoginSchema):
    return ds.docker_login(payload.username, payload.password)

# Docker Logout
@router.post("/logout")
def logout_from_docker():
    return ds.docker_logout()

# Image Operations
@router.post("/build")
def build_image(image_name: str = Form(...)):
    return ds.build_image(image_name)

@router.post("/push")
def push_image(image_name: str = Form(...)):
    return ds.push_image(image_name)

@router.post("/pull")
def pull_image(image_name: str = Form(...)):
    return ds.pull_image(image_name)

@router.get("/images")
def get_images():
    return ds.list_images()

@router.delete("/images")
def remove_image(image_name: str = Form(...)):
    return ds.delete_image(image_name)

# Container Operations
@router.post("/run")
def run_container(image_name: str = Form(...), container_name: str = Form(...)):
    return ds.run_container(image_name, container_name)

@router.post("/start")
def start_container(container_name: str = Form(...)):
    return ds.start_container(container_name)

@router.post("/stop")
def stop_container(container_name: str = Form(...)):
    return ds.stop_container(container_name)

@router.post("/restart")
def restart_container(container_name: str = Form(...)):
    return ds.restart_container(container_name)

@router.get("/containers")
def list_all_containers():
    return ds.list_containers()

@router.delete("/containers")
def remove_container(container_name: str = Form(...)):
    return ds.delete_container(container_name)

# Volume Operations
@router.post("/volumes")
def create_volume(volume_name: str = Form(...)):
    return ds.create_volume(volume_name)

@router.get("/volumes")
def list_volumes():
    return ds.list_volumes()

@router.delete("/volumes")
def delete_volume(volume_name: str = Form(...)):
    return ds.delete_volume(volume_name)

# Logs & PS
@router.get("/logs/{container_name}")
def get_logs(container_name: str):
    return ds.get_logs(container_name)

@router.get("/ps")
def docker_ps():
    return ds.docker_ps()
