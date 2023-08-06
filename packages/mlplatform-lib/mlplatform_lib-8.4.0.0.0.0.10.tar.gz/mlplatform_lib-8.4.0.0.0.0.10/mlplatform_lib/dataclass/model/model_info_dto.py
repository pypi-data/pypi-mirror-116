from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase
from mlplatform_lib.dataclass.model.type import ModelStatus


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ModelInfoDto:
    id: int = field(init=False, default = 0)
    type: str
    result: str
    finished_time: str = field(init=False)
    status: ModelStatus = field(init=False)
