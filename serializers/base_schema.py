from pydantic import BaseModel, PositiveInt, NonNegativeInt


class ModelSchema(BaseModel):
    id: PositiveInt

    class Config:
        orm_mode = True


class CreateModelSchema(BaseModel):
    pass


class UpdateModelSchema(BaseModel):
    id: PositiveInt | None


class GetModelSchema(BaseModel):
    id: PositiveInt


class GetModelsByQuerySchema(BaseModel):
    limit: PositiveInt | None
    offset: NonNegativeInt | None


class DeleteModelSchema(BaseModel):
    id: PositiveInt
