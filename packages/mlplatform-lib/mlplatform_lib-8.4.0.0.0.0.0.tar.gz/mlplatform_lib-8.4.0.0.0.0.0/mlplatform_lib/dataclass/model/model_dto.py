from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from mlplatform_lib.dataclass.experiment.type import ExperimentType
from mlplatform_lib.dataclass.model.type import ModelStatus


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ModelDto:
    id: int
    train_id: int
    name: int
    experiment_type: ExperimentType
    description: str
    model_path: str
    status: ModelStatus
