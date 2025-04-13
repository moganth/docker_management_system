from pydantic import BaseModel

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
    image_name: str

