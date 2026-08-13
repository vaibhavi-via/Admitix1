from __future__ import annotations
import uuid
from pydantic import BaseModel, ConfigDict, Field
from core.enums import PreferenceStatus
class ApplicationPreferenceBase(BaseModel):
    preference_no: int = Field(..., gt=0)
    status: PreferenceStatus = PreferenceStatus.PENDING
class ApplicationPreferenceCreate(ApplicationPreferenceBase):
    application_id: uuid.UUID
    course_id: uuid.UUID
class ApplicationPreferenceUpdate(BaseModel):
    preference_no: int | None = Field(None, gt=0)
    status: PreferenceStatus | None = None
class ApplicationPreferenceRead(ApplicationPreferenceBase):
    model_config = ConfigDict(from_attributes=True)
    preference_id: uuid.UUID
    application_id: uuid.UUID
    course_id: uuid.UUID
