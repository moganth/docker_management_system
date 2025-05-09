import docker
from fastapi import HTTPException
from fastapi import APIRouter
from services import docker_service as ds
from schemas.docker_schema import DockerImageSchema, DockerLoginSchema, BuildImagePayload, PushImagePayload, PullImagePayload, ContainerRunRequest, VolumeSchema, BuildRequest
from services.docker_service import build_image_from_repo

client = docker.from_env()
router = APIRouter()

@router.post("/login")
def login_to_docker(payload: DockerLoginSchema):
    return ds.docker_login(payload.username, payload.password)

# Build Docker image from a GitHub repository
@router.post("/docker/build from github repo")
def build_image(request: BuildRequest):
    github_url = request.github_url
    image_name = request.image_name
    repo_name = request.repo_name
    return build_image_from_repo(github_url, image_name, repo_name)

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
        push_response = ds.push_image(
            local_image_name=payload.local_image_name,
            repository_name=payload.repository_name,
            username=payload.username,
            password=payload.password
        )
        return {"message": push_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pull")
def pull_image(payload: PullImagePayload):
    try:
        return ds.pull_image(payload.image_name, payload.repository_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images")
def list_all_images():
    return ds.list_images()

@router.delete("/images")
def remove_image(image_name: str):
    return ds.delete_image(image_name)

# Container Endpoints
@router.post("/container/run")
def run_container(payload: ContainerRunRequest):
    try:
        return ds.run_container(payload.image_name, payload.container_name, payload.ports, payload.environment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/container/stop")
def stop_container(payload: ContainerRunRequest):
    try:
        return ds.stop_container(payload.container_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/container/start")
def start_container(payload: ContainerRunRequest):
    try:
        return ds.start_container(payload.container_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/container/restart")
def restart_container(payload: ContainerRunRequest):
    try:
        return ds.restart_container(payload.container_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/container/remove")
def remove_container(payload: ContainerRunRequest):
    try:
        return ds.remove_container(payload.container_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs/{container_name}")
def get_logs(container_name: str):
    return ds.get_logs(container_name)

@router.get("/ps")
def docker_ps():
    return ds.docker_ps()

@router.post("/volume/create")
def create_docker_volume(payload: VolumeSchema):
    return ds.create_volume(payload.volume_name)

@router.get("/volumes")
def list_docker_volumes():
    return ds.list_volumes()

@router.delete("/volume/delete")
def delete_docker_volume(volume_name: str):
    return ds.delete_volume(volume_name)
