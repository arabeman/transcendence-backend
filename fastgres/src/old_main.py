from fastapi import FastAPI, HTTPException, Query, Path, Body, status
from typing import Optional, List, Dict, Any # stict type argument
from heroes import HEROES
from classes import HeroValidation, Hero
from utils import get_last_id_from_store
from starlette import status

app = FastAPI()

# NOTE CRUD operations:
# CREATE(post) READ(get) UPDATE(put) DELETE(delete)
# Rest

#defining route and enpoints
""" 
Route: The URL path that users/clients access (e.g., /, /users, /posts/123)
Endpoint: The combination of a route + HTTP method (e.g., GET /users, POST /users)

http://localhost:8000/heroes/search?type=Wizard&min_rank=50
									└─────────────────────┘
										 Query parameters
"""

# ============================================================================ #
#                                  GET - READ                                  #
# ============================================================================ #

@app.get("/") # Route: "/", Method: GET
#by default async so we can ommit it
def read_root():
	return {"message": "Hello, World!"}

# ---------------------------------------------------------------------------- #

@app.get("/heroes", status_code=status.HTTP_200_OK) # Route: "/heroes", Method: GET
def get_heroes():
	return HEROES

# ---------------------------------------------------------------------------- #

@app.get("/heroes/type", status_code=status.HTTP_200_OK)
#min length returns a 422 Unprocessable Entity if query empty =>HTTPException
def get_all_heroes_by_type(hero_type: str = Query(min_length=1)):
	return [h for h in HEROES if hero_type.casefold() in h.type.casefold()]

# ---------------------------------------------------------------------------- #

@app.get("/heroes/rank", status_code=status.HTTP_200_OK)
def get_all_heroes_by_rank(hero_rank: int = Query(ge=1, le=100)): #must be greater of equal than 1
	return [h for h in HEROES if h.rank >= hero_rank]

# ---------------------------------------------------------------------------- #
# Optional must be initialised
@app.get("/heroes/search", status_code=status.HTTP_200_OK)
def search_heroes(
	type: Optional[str] = Query(None), 
	min_rank: Optional[int] = Query(None),
	max_rank: Optional[int] = Query(None),
	occupation: Optional[str] = Query(None),
):
	results = []
	for h in HEROES:
		if type and type.casefold() not in h.type.casefold():
			continue
		if min_rank is not None and h.rank < min_rank:
			continue
		if max_rank is not None and h.rank > max_rank:
			continue
		if occupation:
			# Check if occupation query is a substring of ANY of the hero's occupations
			hero_occupations = [occ.casefold() for occ in h.occupation]
			if not any(occupation.casefold() in occ for occ in hero_occupations):
				continue
		results.append(h)
	return results

# ---------------------------------------------------------------------------- #

@app.get("/hero/id/{hero_id}", status_code=status.HTTP_200_OK)
def get_hero_by_id(hero_id: int = Path(ge=1, le= 100, title="Id of the hero to get")):#Path parameter is {hero_id}
	for h in HEROES:
		if h.id == hero_id:
			return h
	raise HTTPException(status_code=404, detail="Hero not found")

# ---------------------------------------------------------------------------- #

@app.get("/hero/nick/{nickname}", status_code=status.HTTP_200_OK)
def get_hero_by_nickname(nickname: str=Path(min_length=1, max_length=300, title="Nickname of the hero to get")):
	for h in HEROES:
		hero_nickname = h.nickname
		if hero_nickname and nickname.casefold() in hero_nickname.casefold():
			return h
	raise HTTPException(status_code=404, detail="Hero not found")


# ============================================================================ #
#                                 POST - CREATE                                #
# ============================================================================ #

""" 
	model_dump(): previously called dict() -> transforming model instance into a plain dict
	of its field/values
	hero_body.model_dump gives a dict {"id": 11, "nickname": "X", "fullname": "...", ...}
	** takes a mapping and expands each key/value into a keyword argument
	print(type(hero_body))
"""
@app.post("/hero/create", status_code=status.HTTP_201_CREATED)
def create_hero(hero_body: HeroValidation = Body()):
	new_hero = Hero(**hero_body.model_dump()) 
	new_hero.id = get_last_id_from_store() + 1
	print(type(new_hero))
	HEROES.append(new_hero)
	return new_hero


# ============================================================================ #
#                                 UPDATE - PUT                                 #
# ============================================================================ #

@app.put("/hero/update", status_code=status.HTTP_204_NO_CONTENT)
def update_hero(hero_body: HeroValidation = Body()):
	for i in range(len(HEROES)):
		if HEROES[i].id == hero_body.id:
			HEROES[i] = Hero(**hero_body.model_dump())
			return HEROES[i]
	raise HTTPException(status_code = 404, detail="Hero not found")

# ============================================================================ #
#                                    DELETE                                    #
# ============================================================================ #

@app.delete("/hero/delete/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int = Path(ge=1, le= 100, title="Id of the hero to delete")):
	for i, h in enumerate(HEROES):
		if h.id == hero_id:
			HEROES.pop(i)
			return {"message": "Hero Deleted"}
	raise HTTPException(status_code=404, detail="Hero not found")
