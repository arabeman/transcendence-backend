"""

Model in SQLModel is special: it defines a Python class AND a Database table at the same time.

"""
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

# Base class for all game entities
# This class represents the table 'hero' in your database
class Hero(SQLModel, table=True):
    """Represents a playable character in the game"""
    # primary_key=True means this is the unique ID for each row
    # field to add extra settings or metadata
    id: Optional[int] = Field(default=None, primary_key = True)
    nickname: str = Field(index=True) # search made faster
    role: str # e.g fruit or archetypes
    speed: float = Field(default=5.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class User(SQLModel, table=True):
    """Represents a human player's account"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: Optional[str] = Field(default=None, index=True)
    hashed_password: str # Store hashed for security
    
    # Game progression
    level: int = Field(default=1)
    xp: int = Field(default=0)
    
    # Metadata
    is_active: bool = Field(default=True)
    is_superuser:bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Weapon(SQLModel, table=True):
    """ Represents weapons/boomerang in the game"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    throw_speed: float
    special_ability: Optional[str] = None
    rarity: str = Field(default="common") # common, rare

class GameSession(SQLModel, table=True):
    """Tracks individual game matches"""
    id: Optional[int] = Field(default=None, primary_key=True)
    winner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    duration_seconds: int
    player_count: int
    map_name: str
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
class PlayerStats(SQLModel, table=True):
    """Stores player statistics across all games"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key = "user.id", unique=True)
    total_kills: int = Field(default=0)
    total_deaths: int = Field(default=0)
    total_wins: int = Field(default=0)
    total_games: int = Field(default=0)
    # I put it there in case we need it for more statistics
    favorite_weapon_id: Optional[int] = Field(default=None, foreign_key="weapon.id")
