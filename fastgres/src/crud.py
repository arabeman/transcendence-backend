from typing import List, Optional, Sequence
from sqlmodel import Session, select, desc
from models import Hero, User, Weapon, GameSession, PlayerStats
from database import engine
import hashlib

def hash_password(password: str) -> str:
	"""Hashes a password using SHA-256 (simple version)."""
	return hashlib.sha256(password.encode()).hexdigest()

# ============================================================================ #
#                                     HERO                                     #
# ============================================================================ #

def create_hero(nickname: str, role: str, speed: float = 5.0) -> Hero:
	"""
	Creates a new hero in the database.
	Returns the created hero with its generated ID.
	"""
	existing_hero = get_hero_by_nickname(nickname)
	if existing_hero:
		return existing_hero
	hero = Hero(nickname = nickname, role=role, speed=speed)
	with Session(engine) as session:
		session.add(hero)		# Stage the hero for insertion
		session.commit()		# Execute the INSERT query
		session.refresh(hero)	# Get the ID that was auto-generated
		return hero

def list_heroes() -> Sequence[Hero]:
	"""Retrieves all heroes from the database."""
	with Session(engine) as session:
		return session.exec(select(Hero)).all()
	
def mutable_list_heroes() -> List[Hero]:
	"""Retrieves all heroes from the database in a list."""
	with Session(engine) as session:
		return list(session.exec(select(Hero)).all())

def get_hero(hero_id: int) -> Optional[Hero]:
	"""Finds a hero by their ID. Returns None if not found."""
	with Session(engine) as session:
		return session.get(Hero, hero_id) # or session.exec(select(Hero).where(Hero.id == hero_id)).first() <- iterator

def get_hero_by_nickname(nickname:str) ->Optional[Hero]:
	"""Finds a Hero by nickname."""
	with Session(engine) as session:
		statement = select(Hero).where(Hero.nickname == nickname)
		return session.exec(statement).first()

def update_hero(hero_id: int, **kwargs) -> Optional[Hero]:
	"""
	Updates a hero's attributes.
	"""
	with Session(engine) as session:
		hero = session.get(Hero, hero_id)
		if not hero:
			return None
		for key, value in kwargs.items():
			setattr(hero, key, value)
		session.add(hero)
		session.commit()
		session.refresh(hero)
		return hero

def delete_hero(hero_id: int) -> bool:
	"""Deletes a hero from the database. Returns True if successful."""
	with Session(engine) as session:
		hero = session.get(Hero, hero_id)
		if not hero:
			return False
		session.delete(hero)
		session.commit()
		return True


# ============================================================================ #
#                                     USER                                     #
# ============================================================================ #

def create_user(username:str, password:str, email: Optional[str] = None) -> User:
	existing_user = get_user_by_username(username)
	if existing_user:
		return existing_user
	
	hashed_pw = hash_password(password)
	user = User(username=username, hashed_password=hashed_pw, email=email)
	
	with Session(engine) as session:
		session.add(user)
		session.commit()
		session.refresh(user)
		return user
	
def get_user(user_id: int, **kwargs) -> Optional[User]:
	"""Finds a user by their ID."""
	with Session(engine) as session:
		return session.get(User, user_id)

def get_user_by_username(username:str) ->Optional[User]:
	"""Finds a user by their username."""
	with Session(engine) as session:
		statement = select(User).where(User.username == username)
		return session.exec(statement).first()
	
def update_user(user_id: int, **kwargs) -> Optional[User]:
	"""Update a user's attributes."""
	with Session(engine) as session:
		user = session.get(User, user_id)
		if not user:
			return None
		for key, value in kwargs.items():
			setattr(user, key, value)
		session.add(user)
		session.commit()
		session.refresh(user)
		return user

def delete_user(user_id: int) -> bool:
	"""Deletes a user from the database."""
	with Session(engine) as session:
		user = session.get(User, user_id)
		if not user:
			return False
		session.delete(user)
		session.commit()
		return True

# ============================================================================ #
#                                    WEAPON                                    #
# ============================================================================ #

def create_weapon(name: str, throw_speed: float, special_ability: Optional[str] = None, rarity: str = "common") -> Weapon:
	"""Creates a new weapon in the database."""
	weapon = Weapon(name=name, throw_speed=throw_speed, special_ability=special_ability, rarity=rarity)
	with Session(engine) as session:
		session.add(weapon)
		session.commit()
		session.refresh(weapon)
		return weapon

def list_weapons() -> Sequence[Weapon]:
	"""Retrieves all weapons."""
	with Session(engine) as session:
		return session.exec(select(Weapon)).all()
	
def mutable_list_weapons() -> List[Weapon]:
	"""Retrieves all weapons in a list."""
	with Session(engine) as session:
		return list(session.exec(select(Weapon)).all())

def weapons_by_rarity(rarity: str) -> Sequence[Weapon]:
	"""Finds all weapons of a specific rarity."""
	with Session(engine) as session:
		return session.exec(select(Weapon).where(Weapon.rarity == rarity)).all()
	
def mutable_weapons_by_rarity(rarity: str) -> List[Weapon]:
	with Session(engine) as session:
		return list(session.exec(select(Weapon).where(Weapon.rarity == rarity)).all())


# ============================================================================ #
#                                 GAME SESSION                                 #
# ============================================================================ #

def create_game_session(winner_id: int, duration_seconds: int, player_count: int, map_name: str) -> GameSession:
	"""Records a completed game session."""
	game = GameSession(winner_id=winner_id, duration_seconds=duration_seconds, player_count=player_count, map_name=map_name)
	with Session(engine) as session:
		session.add(game)
		session.commit()
		session.refresh(game)
		return game
	
def recent_games(limit: int = 10) -> Sequence[GameSession]:
	"""Gets the 10 most recent game sessions."""
	with Session(engine) as session:
		return session.exec(select(GameSession).order_by(desc(GameSession.started_at)).limit(limit)).all()


# ============================================================================ #
#                                 PLAYER STATS                                 #
# ============================================================================ #

def create_or_update_stats(user_id: int, kills: int = 0, deaths: int = 0, wins: int = 0, games: int = 1 ) -> PlayerStats:
	"""Creates or updates player statisctics."""
	with Session(engine) as session:
		stats = session.exec(select(PlayerStats).where(PlayerStats.user_id == user_id)).first() # <- iterable
		
		if stats:
			stats.total_kills += kills
			stats.total_deaths += deaths
			stats.total_wins += wins
			stats.total_games += games
		else:
			stats = PlayerStats(
				user_id=user_id,
				total_kills=kills,
	   			total_deaths=deaths,
		  		total_wins=wins,
				total_games=games
			 )

		session.add(stats)
		session.commit() # execute ISNERT or UPDATE query
		session.refresh(stats) # update the Python object with the latest state. 
		return stats

""" 
SELECT hero.*, playerstats.*
FROM hero
JOIN playerstats ON hero.id = playerstats.hero_id
ORDER BY playerstats.total_wins DESC
LIMIT 10;
"""

def get_leaderboard(limit: int = 10):
	"""
	Gets top 10 players by wins.
	Returns list of (Hero, PlayerStats) tuples
	"""
	with Session(engine) as session:
		statement = (
			select(User, PlayerStats)
			.join(PlayerStats)  # auto-generates ON User.id = playerstats.user_id
			.order_by(desc(PlayerStats.total_wins))
			.limit(limit)
		)
		# statement = (
		#    select(User, PlayerStats)
		# 	.where(User.id == PlayerStats.user_id)
		# 	.order_by(desc(PlayerStats.total_wins))
		# 	.limit(limit)
	 	# )
		return session.exec(statement).all()
