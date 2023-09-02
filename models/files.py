from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from typing import Optional


class File(BaseModel):
    document_id: str = Field(alias="DocumentId")
    brain_id: str = Field(alias="BrainId")
    user_id:str = Field(alias="UserId")
    file_name: str = Field(alias="source")
    document_vector_status: Optional[bool] = Field(
        default=True, alias="DocumentVectorStatus"
    )
    document_vector_creation_date: Optional[str] = Field(
        default=str(datetime.now()), alias="DocumentVectorCreationDate"
    )

    class Config:
        allow_population_by_field_name = True
