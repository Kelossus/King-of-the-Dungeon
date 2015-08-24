# window
window = {
    'width': 1280,
    'height': 720,
    'caption': "King of the Dungeon",
    "fullscreen": False,
    'resizable': True
}

window_original = (1920, 1080)

# static positioning
monster_pos = (650, 750)
gold_pos = ((200, 700), (1100, 700))
gold_scale = 1.5

# minions

soldiers = { # ((attack, defense), corpse cost, weapon cost)
	"goblin": 			([1, 1], 1, 0),
	"hobgoblin": 		([2, 2], 1, 1),
	"orc": 				([2, 4], 2, 2), # they have a 50% chance to attack twice, if they kill in the first attack they take no damage
	"madgnome": 		([2, 1], 1, 2), # spawn madgnome_count when bought
	"necromancer": 		([0, 1], 0, 0) # costs gold
}

farmers = { # (cost, success rate, gathred gold, gathered corpses, gathered weapons)
	"miner": 			(1, 0.05, 5, 0, 0),
	"gatherer": 		(1, 0.04, 1, 5, 1)
}

spawn_place = {
	"goblin": 			(220, 350),
	"hobgoblin": 		(1200, 200),
	"orc": 				(100, 225), 
	"madgnome": 		(960, 220),
	"necromancer": 		(1080, 350),
	"gatherer":			(350, 210),
	"miner":			(950, 420)
}

minion_move_to = {
	"goblin": 			(0, -360),
	"hobgoblin": 		(0, -200),
	"orc": 				(0, -220), 
	"madgnome": 		(0, -225),
	"necromancer": 		(0, -340),
	"gatherer":			(0, -220),
	"miner":			(320, 0)
}

minion_move_time = 3

orc_berserk_chance = 0.5

madgnome_count = 3

necromancer_gold_cost = 10
necromancer_revival_chance = 0.05

# treasure hunters

hunters = { # (attack, defense)
		"vagabound":    (1, 1),  
	    "militia":      (1, 2),  
		"looter":	    (2, 1),  
		"defender":	    (1, 5),  
		"agressor":	    (3, 2),  
		"champion":	    (7, 7)   
}

waves = { # (vagabound, militia, looter, defender, agressor, champion)

	"vagabound": (5,6,4,2,1,1,1,30),
    "militia":   (1,3,5,5,3,3,3,0),
    "looter":    (0,2,2,3,5,4,4,0),
    "agressor":  (0,0,3,2,3,5,5,0),
    "defender":  (0,0,0,1,2,2,2,0),
    "champion":  (0,0,0,0,0,0,1,2),

}

# misc
start_gold = 50
start_corpses = 2
start_weapons = 0
gold_objective = 100

update_delay = 2

house_scale = 6
minion_scale =1.5

col_radious = 20

building_cool_down = 0.75