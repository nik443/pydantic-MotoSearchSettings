import pydantic
from loguru import logger


class EngineDisplacement(pydantic.BaseModel):
    start_range: int
    finish_range: int

    @pydantic.field_validator("start_range", "finish_range")
    def is_positive_start_and_finis_range(cls, point_range: int):
        if point_range < 0:
            logger.warning(f"Point of range: {point_range} less than zero, return 0")
            return 0
        return point_range

    @pydantic.model_validator(mode="after")
    def start_less_finish_range(self, values):
        if self.start_range > self.finish_range:
            logger.warning(f"Point start range biggest then finish, error")
            self.start_range = 0
        return self


class MotoSearchSettings(pydantic.BaseModel):
    model: str = pydantic.Field(serialization_alias="Model")
    constuction_type: list[str] = pydantic.Field(serialization_alias="ConstructionTypes")
    engine_displacement: EngineDisplacement = pydantic.Field(serialization_alias="EngineDisplacement")


data = {
    "start_range": 1,
    "finish_range": -10,
}
enginge_displacement = EngineDisplacement.model_validate(obj=data)
res = enginge_displacement.model_dump()

a = 1
