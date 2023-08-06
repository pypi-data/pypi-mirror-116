from typing import Dict, Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from mlplatform_lib.dataclass.model import ModelDto
from mlplatform_lib.dataclass.experiment.type import ExperimentType
from mlplatform_lib.dataclass.model.type import ModelStatus


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ModelPredefinedaiDto(ModelDto):
    algorithm: str
    metric: str
    metric_result: str

