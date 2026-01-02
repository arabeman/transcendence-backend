from database import create_db_and_tables
from crud import (
	create_hero, list_heroes, mutable_list_heroes,
	get_hero, update_hero, delete_hero,
	create_user, get_user, update_user,
	create_weapon, list_weapons, mutable_list_weapons,
	weapons_by_rarity, mutable_weapons_by_rarity,
	create_game_session, recent_games, create_or_update_stats,
	get_leaderboard,
)

def demo():
	print("Init DB...")
	create_db_and_tables()
	
 
	# ---------------------------------- Heroes --------------------------------- #
	print("\nCreate heroes")
	h1 = create_hero("Carrot", role="Veggie", speed=5.5)
	h2 = create_hero("Peach", role="Fruit", speed=4.5)
	
	assert h1.id is not None
	assert h2.id is not None
 
	print("\nUpdate Carrot Speed")
	upd = update_hero(h1.id, speed=5.8)
	assert upd is not None
	print(f"Updated: {upd.nickname} speed={upd.speed}")
 
	print("\nList heroes")
	for h in list_heroes():
		print(f"- {h.nickname} ({h.role}) speed={h.speed}")
	
 	# ---------------------------------- Users ---------------------------------- #
	
	print("\nCreate user")
	user1 = create_user("Uman", password="huhupwd123", email="uman@example.com")
	assert user1.id is not None
	print(f"user {user1} created with ID {user1.id}")
 
	fetched_user = get_user(user1.id)
	assert fetched_user is not None
	print(f"Fetched by ID: {fetched_user.username}")
 
	updated_user = update_user(user1.id, email="new_email@test.com", xp=100)
	assert updated_user is not None
	print(f"Updated User: XP={updated_user.xp}, Email={updated_user.email}")
 
	# --------------------------------- Weapons --------------------------------- #
	
	print("\nCreate weapons")
	create_weapon("Basic Boomerang", throw_speed=4.5)
	create_weapon("Fire Boomerang", throw_speed=6.5, special_ability="trailblazer", rarity="rare")
	create_weapon("Ice Boomerang", throw_speed=6.5, special_ability="frost-walker", rarity="rare")
	
	print("\nRare weapons")
	for i, w in enumerate(weapons_by_rarity("rare"), 1):
		print(f"{i}- {w}")
  
	# --------------------------------- Gameplay -------------------------------- #
		
	print("\nRecord a game session")
	game = create_game_session(winner_id=user1.id, duration_seconds=69, player_count=6, map_name="Kitchen")
	print("\nGame {game.id} recorded")
	
	print("Update stats for User")
	create_or_update_stats(user_id=user1.id, kills=5, deaths=2, wins=1)
	print("Stats updated")
 
	# -------------------------------- Leaderboad ------------------------------- #
	
	print("\n Leaderboard")
	lb = get_leaderboard()
	for rank, (user, stats) in enumerate(lb, 1):
		print(f"{rank}. {user.username} - Wins: {stats.total_wins}, Kills: {stats.total_kills}")

if __name__ == "__main__":
	demo()