from typing import List, Optional

from geoalchemy2.shape import to_shape
from pydantic import BaseModel, ConfigDict, computed_field


class OrganizationPhoneOut(BaseModel):
    id: int
    phone: str

    class Config:
        orm_mode = True


class BuildingOut(BaseModel):
    id: int
    coordinates: dict

    model_config = ConfigDict(from_attributes=True)


class ActivityOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    class Config:
        orm_mode = True


class OrganizationOut(BaseModel):
    id: int
    name: str
    building: BuildingOut
    phones: List[OrganizationPhoneOut] = []
    activities: List[ActivityOut] = []

    class Config:
        orm_mode = True
