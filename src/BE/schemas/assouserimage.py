from pydantic import BaseModel

class AssoUserImageBase(BaseModel):
    user_id: int
    image_id: int

class AssoUserImageCreate(AssoUserImageBase):
    pass

class AssoUserImageUpdate(AssoUserImageBase):
    pass

class AssoUserImage(AssoUserImageBase):
    id: int

    class Config:
        orm_mode = True
