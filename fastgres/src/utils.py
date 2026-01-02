from heroes import HEROES

from typing import Iterable, Mapping, Any

def get_last_id(hero):
	return 1 if len(HEROES) == 0 else HEROES[-1].id

# def get_last_id(heroes: Iterable[Mapping[str, Any]]) -> int:
#     """Returns the maximum integer 'id' found; 0 if none present."""
#     ids = [h["id"] for h in heroes if "id" in h and isinstance(h["id"], int)]
#     return max(ids) if ids else 0

def get_last_id_from_store() -> int:
	return get_last_id(HEROES)
