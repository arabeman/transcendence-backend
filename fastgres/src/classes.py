from typing import List, Optional
#constr constraint for string
from pydantic import BaseModel, Field, constr 
class Hero:
	id: int
	nickname: str
	fullname: str
	occupation: List[str]
	powers: List[str]
	hobby: List[str]
	type: str
	rank: int
	def __init__(self, id, nickname, fullname,\
				occupation, powers, hobby, type, rank):
		self.id = id
		self.nickname = nickname
		self.fullname = fullname
		self.occupation = occupation
		self.powers = powers
		self.hobby = hobby
		self.type = type
		self.rank = rank

class HeroValidation(BaseModel):
	id: Optional[int] = Field(default=None, ge=0, description="ID is optional on creation")
	nickname: str = Field(min_length = 3)
	fullname: str = Field(min_length = 3)
	occupation: List[constr(min_length = 3)]
	powers: List[constr(min_length = 3)]
	hobby: List[constr(min_length = 3)]
	type: str = Field(min_length = 3)
	rank: int = Field(ge=1, le=100)
	model_config = {
		"json_schema_extra": {
			"example" : {
				"id": 42, # can be omitted
				"nick_name": "Percy",
                "full_name": "Percival Fredrickstein Von Musel Klossowski de Rolo III",
                "occupation": ["Aristocrat", "Ruler of Whitestone", "Member of Vox Machina"],
                "powers": ["Gunsmanship", "Craftsmanship", "Strength", "Speed"],
                "hobby": ["Designing and building new weapons like 'Bad News'", "Building weapons and gadgets"],
                "type": "Tragic Aristocrat",
                "rank": 63
			}
		}
	}