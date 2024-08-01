from dataclasses import dataclass, astuple
from typing import Optional

import pydantic
from loguru import logger


@dataclass
class Models:
    harlew_davidson: str = "Harley-Davidson"
    ducati: str = "Ducati"
    honda: str = "Honda"


@dataclass
class MotoConstructionTypes:
    child: str = "детский"
    custom: str = "кастом"
    classic: str = "классика"
    cross: str = "кроссовый"
    cruiser: str = "круизер"


@dataclass
class TactX:
    x_2: str = "двухтактный"
    x_4: str = "четырехтактный"


class PriceRange(pydantic.BaseModel):
    start_range: Optional[int] = None
    finish_range: Optional[int] = None

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


class EngineDisplacement(pydantic.BaseModel):
    start_range: Optional[int] = None
    finish_range: Optional[int] = None

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
    model: str | None = pydantic.Field(default=None, serialization_alias="Model")
    constuction_types: list[str] | None = pydantic.Field(default=None, serialization_alias="ConstructionTypes")
    engine_displacement: EngineDisplacement | None = pydantic.Field(serialization_alias="EngineDisplacement")
    tact_x: str | None

    @pydantic.field_validator("model")
    def is_correct_model(cls, model: str):
        if not model or model in astuple(Models()):
            return model
        else:
            logger.warning(f"Uncorrent moto model: {model}")
            return None

    @pydantic.field_validator("constuction_types")
    def is_correct_model(cls, user_constuction_types: list[str]):
        correct_construction_types = astuple(MotoConstructionTypes())
        correct_user_types = []
        for constuction_type in user_constuction_types:
            if constuction_type in correct_construction_types:
                correct_user_types.append(constuction_type)
        return correct_user_types if correct_user_types else None

    @pydantic.field_validator("tact_x")
    def is_correct_tact_x(cls, tact_x):
        return tact_x if tact_x in astuple(TactX()) else None


data = {
    "model": Models.honda,
    "constuction_types": [],
    "engine_displacement": EngineDisplacement.model_validate(obj={"start_range": 1, "finish_range": 99}),
    "tact_x": TactX.x_2,
}
moto_search = MotoSearchSettings.model_validate(obj=data)
res = moto_search.model_dump()
