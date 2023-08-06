from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import List, Dict

# example
# "name": "TEST",
# "sourceTableName": "TEST",
# "subtype": "Table",
# "outCols": [
#     {
#         "name": "C1"
#     },
#     {
#         "name": "C2"
#     }
# ],
# "shareRelation": [
# ]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DataObject:
    id: str
    name: str
    out_cols: List[Dict[str, str]]
    share_relation: List[str]
    source_table_name: str
    subtype: str
    author: str
    description: str
    created_on: str
    last_edited: str
