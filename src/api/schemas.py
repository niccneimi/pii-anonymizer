from pydantic import BaseModel

class AnonymizeRequest(BaseModel):
    text: str
    mode: str

class AnonymizeResponse(BaseModel):
    anonymized_text: str