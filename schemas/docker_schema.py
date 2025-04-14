from pydantic import BaseModel
from typing import Optional, Dict

class ImageSchema(BaseModel):
    image_name: str

class ContainerSchema(BaseModel):
    image_name: str
    container_name: str

class VolumeSchema(BaseModel):
    volume_name: str

class DockerLoginSchema(BaseModel):
    username: str
    password: str

class DockerImageSchema(BaseModel):
    image_name: str
    repository_name: str  # Docker Hub repository name (e.g., username/repository)

class BuildImagePayload(BaseModel):
    image_name: str
    dockerfile_path: str
    dockerfile_name: str = "Dockerfile"

class PushImagePayload(BaseModel):
    local_image_name: str  # local name like 'image1'
    repository_name: str   # target like 'moganthkumar/moganth'
    username: str
    password: str

class PullImagePayload(BaseModel):
    image_name: str
    repository_name: str

class ContainerOperationPayload(BaseModel):
    image_name: str
    container_name: str
    ports: Optional[Dict[str, str]] = None  # Example: {"80": "8080"}
    environment: Optional[Dict[str, str]] = None  # Example: {"ENV_VAR": "value"}

