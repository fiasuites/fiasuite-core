from pydantic import BaseModel, Field, constr


class APIKey(BaseModel):
    id: str
    value: constr(max_length=20, min_length=20) = Field(None, title="The value of the api key.")
    

