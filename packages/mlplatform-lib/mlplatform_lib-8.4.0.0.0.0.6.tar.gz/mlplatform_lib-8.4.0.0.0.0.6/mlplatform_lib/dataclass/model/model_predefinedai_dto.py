from typing import Dict, Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from mlplatform_lib.dataclass.model import ModelDto


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ModelPredefinedaiDto(ModelDto):
    algorithm: str
    metric: str
    metric_result: str
