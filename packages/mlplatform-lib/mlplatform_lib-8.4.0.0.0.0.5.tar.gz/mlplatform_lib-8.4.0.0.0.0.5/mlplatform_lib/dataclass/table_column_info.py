from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

# {
#     "name": "review",
#     "type": "VARCHAR",
#     "alias": "review",
#     "nullable": true,
#     "primaryKey": false,
#     "foreignKey": false,
#     "description": ""
# },


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TableColumnInfo:
    name: str
    type: str
    alias: str
    nullable: bool
    primary_key: bool
    foreign_key: bool
    description: str
