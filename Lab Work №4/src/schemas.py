from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict


class Role(str, Enum):
    CONTRACTOR = "Подрядчик"
    SUPERVISOR = "Представитель УСК"
    MANAGER = "Руководитель УСК"


class SUserAdd(BaseModel):
    login: str
    password: str
    name: str
    role: Role


class SUser(SUserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SConstructionObjectAdd(BaseModel):
    address: str
    type: str | None = None


class SConstructionObject(SConstructionObjectAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SConstructionObjectId(BaseModel):
    id: int


class Status(str, Enum):
    open = "Открыто"
    atWork = "В работе"
    close = "Закрыто"


class SViolationAdd(BaseModel):
    description: str
    location: str
    date: date
    resolution_status: Status
    contractor_id: int
    supervisor_id: int
    construction_object_id: int
    violation_classifier: str


class SViolation(SViolationAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SViolationUpdateStatus(BaseModel):
    id: int
    new_status: Status
