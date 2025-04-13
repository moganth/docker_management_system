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
