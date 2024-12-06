# PythonMouse2020
# Copyright (C) 2023 David Fan
# Released under GPLv3

import numpy as np

UP = (0, 1)
DOWN = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)
STILL = (0, 0)


def build_coord(coord_x, coord_y, direction, animal):
	"""Build a 2D coordinate with direction and animal"""
	new_coord = {'x': coord_x, 'y': coord_y, \
	'direction': direction, 'animal': animal}
	return new_coord


def next_coord(coord):
	"""Return next coordinate from direction"""
	coord_x = coord['x'] + coord['direction'][0]
	coord_y = coord['y'] + coord['direction'][1]
	direction = coord['direction']
	animal = coord['animal']
	return build_coord(coord_x, coord_y, direction, animal)


def prev_coord(coord):
	"""Return previous coordinate from direction"""
	coord_x = coord['x'] - coord['direction'][0]
	coord_y = coord['y'] - coord['direction'][1]
	direction = coord['direction']
	animal = coord['animal']
	return build_coord(coord_x, coord_y, direction, animal)


def get_coord_tuple(coord):
	"""Return coordinate tuple"""
	return (coord['x'], coord['y'])


def get_coord_tuple_list(coord_list):
	"""Return coordinate tuple list"""
	return [get_coord_tuple(x) for x in coord_list]


def get_coord_indices(coord_tuple, coord_tuple_list):
	"""Return indices that have the same coordinate tuple"""
	return tuple([idx for idx, value in enumerate(coord_tuple_list) \
	if value == coord_tuple])


def check_is_still_moving(coord_list):
	"""Check if coordinates are still moving"""
	for coord in coord_list:
		if(coord['direction'] != STILL):
			return True
	return False


def check_in_coord_bounds(coord):
	"""Check if coordinate is outside the boundary"""
	if (coord['x'] >= 0 and coord['x'] < 10) \
	and (coord['y'] >= 0 and coord['y'] < 10):
		return True
	return False


def check_if_opposite(coord_a, coord_b):
	"""Check if two coordinates are next to each other \
	with opposite direction
	"""
	if(		coord_a['x']+coord_a['direction'][0] == coord_b['x']
		and coord_a['y']+coord_a['direction'][1] == coord_b['y']
		and coord_a['direction'][0] == -1*coord_b['direction'][0]
		and coord_a['direction'][1] == -1*coord_b['direction'][1]):
		return True
	return False


def check_if_right(coord_a, coord_next_to_a):
	"""Return true if coordinate is to the right"""
	if coord_a['x'] + 1 == coord_next_to_a['x'] \
	and coord_a['y'] == coord_next_to_a['y']:
		return True
	return False


def check_if_left(coord_a, coord_next_to_a):
	"""Return true if coordinate is to the left"""
	if coord_a['x'] == coord_next_to_a['x'] + 1 \
	and coord_a['y'] == coord_next_to_a['y']:
		return True
	return False


def check_if_above(coord_a, coord_next_to_a):
	"""Return true if coordinate is above"""
	if coord_a['x'] == coord_next_to_a['x'] \
	and coord_a['y'] + 1 == coord_next_to_a['y']:
		return True
	return False


def check_if_below(coord_a, coord_next_to_a):
	"""Return true if coordinate is above"""
	if coord_a['x'] == coord_next_to_a['x'] \
	and coord_a['y'] == coord_next_to_a['y'] + 1:
		return True
	return False


def find_opposite_indices(coord_list, n):
	"""In a list of coordinates return those indices
	where coordinates are opposite
	"""
	i = 0
	opposite_indices = []

	while(i < n):
		for coord in coord_list:
			if(check_if_opposite(coord,coord_list[i])):
				opposite_indices.append(i)
		i += 1

	return opposite_indices


def draw_board(board, victory_flag, level):
	"""Draw 10 by 10 board"""
	
	print(f"Level {level}")
	i = 9
	while(i>=0):
		line = str(i)
		for entry in board[i*10:(i+1)*10]:
			line = line + entry
		print(line)
		i = i - 1
	print(' 0123456789')

	if victory_flag == True:
		print("Congratulations!")

	print()


def setup_board(coord_list, hole_coord):
	"""Setup board from coordinate list"""
	board = []

	i=0
	j=0

	while(i<100):
		board.append('.')
		i = i + 1

	board[hole_coord[1]*10+hole_coord[0]] = 'O'

	for coord in coord_list:
		board[coord['y']*10+coord['x']] = coord['animal']

	return board


def input_digit_coordinate(axis):
	"""User inputs integer between 0-9 or quits \
	with text explaining the coordinate axis
	"""
	coord_flag = True

	while coord_flag:

		coord = input(f"Choose {axis}-coordinate from 0-9: ")
		try:
			if coord == 'q':
				exit()
			coord = int(coord)
		except ValueError:
			print("Type an integer.")
			continue

		if coord > 9 or coord < 0:
			print("Choose value within bounds.")
		else:
			coord_flag = False

	return coord


def get_level_num(levels):
	"""User inputs integer matching level array size or quits """
	level_flag = True

	while level_flag:
		level_num = input("Choose level: ")
		try:
			if level_num == 'q':
				exit()
			level_num = int(level_num)
		except ValueError:
			print("Type an integer.")
			continue

		if level_num < 0 or level_num >= len(levels):
			print("Not a level")
			continue

		level_flag = False

	return level_num


def place_pieces(start_coords, hole_coord, pieces, level_num):
	"""Loop that adds all pieces to board \
	checking whether space is occupied
	"""
	occupied_places = get_coord_tuple_list(start_coords)
	
	occupied_places.append(hole_coord)

	while pieces:

		letter_piece = pieces.pop()

		print(f"Select coordinates for {letter_piece}")

		place_occupied = True

		while place_occupied:

			piece_x_coord = input_digit_coordinate('x')

			piece_y_coord = input_digit_coordinate('y')

			piece_place = (piece_x_coord, piece_y_coord)

			if piece_place in occupied_places:

				print("This place is occupied.")

				continue

			else:

				place_occupied = False

		occupied_places.append(piece_place)

		piece = build_coord(piece_x_coord, piece_y_coord, STILL, letter_piece)

		start_coords.append(piece)

		board = setup_board(start_coords, hole_coord)
		draw_board(board, False, level_num)


def check_animal_relation(coord_a, coord_b):
	if(coord_a['animal'] == 'M' and coord_b['animal'] == 'C'):
		return True
	if(coord_a['animal'] == 'C' and coord_b['animal'] == 'D'):
		return True
	if(coord_a['animal'] == 'D' and coord_b['animal'] == 'B'):
		return True
	if(coord_a['animal'] == 'B' and coord_b['animal'] == 'L'):
		return True
	if(coord_a['animal'] == 'L' and coord_b['animal'] == 'E'):
		return True
	if(coord_a['animal'] == 'E' and coord_b['animal'] == 'M'):
		return True
	if(coord_a['animal'] == 'C' and coord_b['animal'] == 'P'):
		return True
	if(coord_a['animal'] == 'P' and coord_b['animal'] == 'L'):
		return True
	return False


def get_touching_array(coord, coord_list):
	"""Returns intermediary array that shows if 1
	or more animals are touching the coordinate
	and which directions
	"""

	i = 0

	touching_list_of_lists = []

	while(i<len(coord_list)):

		touching_list = []
		# Lists of size 4 [ R B L A ] where
		# R B L A are 1 or 0 and represent the direction

		if(check_if_right(coord,coord_list[i])\
		and check_animal_relation(coord,coord_list[i])):
			touching_list.append(1)
		else:
			touching_list.append(0)
		if(check_if_below(coord,coord_list[i])\
		and check_animal_relation(coord,coord_list[i])):
			touching_list.append(1)
		else:
			touching_list.append(0)
		if(check_if_left(coord,coord_list[i])\
		and check_animal_relation(coord,coord_list[i])):
			touching_list.append(1)
		else:
			touching_list.append(0)
		if(check_if_above(coord,coord_list[i])\
		and check_animal_relation(coord,coord_list[i])):
			touching_list.append(1)
		else:
			touching_list.append(0)

		i+=1
		touching_list_of_lists.append(touching_list)

	touching_array = np.array(touching_list_of_lists)
	touching_array = np.sum(touching_array, axis = 0)

	return touching_array


def get_direction_of_touching_array(array):
	"""Returns the logical direction from touching_array"""
	if np.sum(array) > 1:
		return STILL
	elif array[0] == 1:
		return LEFT
	elif array[1] == 1:
		return UP
	elif array[2] == 1:
		return RIGHT
	elif array[3] == 1:
		return DOWN
	else:
		return None


def set_directions(coord_list):
	t_arrays = [get_touching_array(x, coord_list) for x in coord_list]
	d_t_arrays = [get_direction_of_touching_array(x)
	for x in t_arrays]

	i = 0

	while(i<len(coord_list)):
		 if(d_t_arrays[i] == STILL):
		 	coord_list[i]['direction'] = STILL
		 elif(d_t_arrays[i] == UP):
		 	coord_list[i]['direction'] = UP
		 elif(d_t_arrays[i] == DOWN):
		 	coord_list[i]['direction'] = DOWN
		 elif(d_t_arrays[i] == RIGHT):
		 	coord_list[i]['direction'] = RIGHT
		 elif(d_t_arrays[i] == LEFT):
		 	coord_list[i]['direction'] = LEFT
		 else:
		 	pass
		 i += 1


class Level:
	"""Class with level variables that are copied"""
	def __init__(self, start_coords, hole_coord, pieces):
		self.start_coords = start_coords
		self.hole_coord = hole_coord
		self.pieces = pieces

	def copy_start_coords(self):

		return self.start_coords.copy()

	def copy_hole_coord(self):

		return self.hole_coord

	def copy_pieces(self):

		return self.pieces.copy()


# Levels

# Mouse is always at position 0.

level_00 = {'start_coords': [
	{'x': 5, 'y': 5, 'direction': STILL, 'animal': 'M'},
	{'x': 5, 'y': 6, 'direction': STILL, 'animal': 'C'}
	],
	'hole_coord': (0,0),
	'pieces': ['C']}

level_01 = {'start_coords': [
	{'x': 1, 'y': 0, 'direction': STILL, 'animal': 'M'},
	{'x': 1, 'y': 1, 'direction': STILL, 'animal': 'E'},
	{'x': 2, 'y': 1, 'direction': STILL, 'animal': 'L'},
	{'x': 2, 'y': 8, 'direction': STILL, 'animal': 'C'},
	{'x': 8, 'y': 2, 'direction': STILL, 'animal': 'P'}
	],
	'hole_coord': (0,0),
	'pieces': ['L']}

level_02 = {'start_coords': [
	{'x': 5, 'y': 1, 'direction': STILL, 'animal': 'M'},
	{'x': 5, 'y': 0, 'direction': STILL, 'animal': 'C'},
	{'x': 5, 'y': 2, 'direction': STILL, 'animal': 'E'},
	{'x': 5, 'y': 7, 'direction': STILL, 'animal': 'B'},
	{'x': 4, 'y': 7, 'direction': STILL, 'animal': 'B'},],
	'hole_coord': (5,6),
	'pieces': ['L']}

level_03 = {'start_coords': [
	{'x': 1, 'y': 1, 'direction': STILL, 'animal': 'M'},
	{'x': 0, 'y': 1, 'direction': STILL, 'animal': 'C'},
	{'x': 3, 'y': 0, 'direction': STILL, 'animal': 'C'},
	{'x': 1, 'y': 3, 'direction': STILL, 'animal': 'C'},
	{'x': 2, 'y': 5, 'direction': STILL, 'animal': 'D'},
	{'x': 0, 'y': 7, 'direction': STILL, 'animal': 'C'},
	{'x': 8, 'y': 3, 'direction': STILL, 'animal': 'C'},
	{'x': 5, 'y': 8, 'direction': STILL, 'animal': 'C'},
	{'x': 7, 'y': 9, 'direction': STILL, 'animal': 'C'}],
	'hole_coord': (9,9),
	'pieces': ['C']}

level_04 = {'start_coords': [
	{'x': 1, 'y': 1, 'direction': STILL, 'animal': 'M'},
	{'x': 2, 'y': 1, 'direction': STILL, 'animal': 'E'},
	{'x': 3, 'y': 2, 'direction': STILL, 'animal': 'L'},
	{'x': 4, 'y': 3, 'direction': STILL, 'animal': 'B'},
	{'x': 5, 'y': 4, 'direction': STILL, 'animal': 'D'},
	{'x': 4, 'y': 5, 'direction': STILL, 'animal': 'C'},
	{'x': 7, 'y': 5, 'direction': STILL, 'animal': 'C'},
	{'x': 8, 'y': 0, 'direction': STILL, 'animal': 'D'}],
	'hole_coord': (9,5),
	'pieces': ['B']}

level_05 = {'start_coords': [
	{'x': 4, 'y': 5, 'direction': STILL, 'animal': 'M'},
	{'x': 3, 'y': 4, 'direction': STILL, 'animal': 'C'},
	{'x': 3, 'y': 7, 'direction': STILL, 'animal': 'C'},
	{'x': 6, 'y': 7, 'direction': STILL, 'animal': 'C'},
	{'x': 5, 'y': 5, 'direction': STILL, 'animal': 'D'},
	{'x': 3, 'y': 6, 'direction': STILL, 'animal': 'D'},
	{'x': 7, 'y': 6, 'direction': STILL, 'animal': 'D'},
	{'x': 6, 'y': 9, 'direction': STILL, 'animal': 'D'},
	{'x': 7, 'y': 8, 'direction': STILL, 'animal': 'B'},
	{'x': 2, 'y': 9, 'direction': STILL, 'animal': 'B'}],
	'hole_coord': (4,0),
	'pieces': ['D']}

level_06 = {'start_coords': [
	{'x': 2, 'y': 2, 'direction': STILL, 'animal': 'M'},
	{'x': 1, 'y': 7, 'direction': STILL, 'animal': 'P'},
	{'x': 2, 'y': 8, 'direction': STILL, 'animal': 'P'}],
	'hole_coord': (7,7),
	'pieces': ['C','C']}

levels = []
levels.append(level_00)
levels.append(level_01)
levels.append(level_02)
levels.append(level_03)
levels.append(level_04)
levels.append(level_05)
levels.append(level_06)

# Game Text

print("PythonMouse 2020")

help_message = f"""
Goal: Get Mouse [M] into Hole [O] (Levels 0-{len(levels)-1})

The animals:
	[M]ouse
	[C]at
	[D]og
	[B]ear
	[L]ion
	[E]lephant
	[P]ython

Place animal piece at coordinate.

Animals will run away from another animal based on type.

M < C < D < B < L < E < M :: C < P < L

Press q to quit and b to break out of loop
"""

s = input("Press h for help or return to continue: ")

if(s == 'h'):
	print(help_message)
if(s == 'q'):
	exit()

# Reset loop

while(True):

	# Get level number from user

	level_num = get_level_num(levels)

	current_level = Level(levels[level_num]['start_coords'], \
	levels[level_num]['hole_coord'], levels[level_num]['pieces'])

	# Fill level variables

	start_coords = current_level.copy_start_coords()
	hole_coord = current_level.copy_hole_coord()
	pieces = current_level.copy_pieces()

	victory_flag = False

	# Initial position without pieces

	board = setup_board(start_coords, hole_coord)

	draw_board(board, victory_flag, level_num)

	# Place pieces

	# Each piece is placed checking whether the place is occupied.

	place_pieces(start_coords, hole_coord, pieces, level_num)

	# Setup variables

	next_len = start_len = len(start_coords)

	prev_coords = start_coords

	# Simulation

	# Loop ends if all animals are still or victory is met.

	still_flag = False  # Set in collision loop

	while True:

		if still_flag == True:
			break

		# Direction Setter

		set_directions(prev_coords)

		# Check motion

		if not check_is_still_moving(prev_coords):
			break

		# Victory condition

		if victory_flag == True:
			break

		# Next loop control

		s = input("Press return to continue: ")

		if(s == 'b'):
			break
		if(s == 'q'):
			exit()

		# Passing Collisions

		# Collisions where two pieces collide head-on with no space.

		opposite_indices = find_opposite_indices(prev_coords, start_len)

		# The direction is changed to 'STILL'.
		if any(opposite_indices):
			for index in opposite_indices:
				prev_coords[index]['direction'] = STILL

		# Collision loop

		# Variables:
		# 'next_coords' is the current frame that is calculated from \
		# 'prev_coords'.

		# 'prev_coords' is the last frame and it is modified \
		# when there is an animal out of bounds or collision in \
		# 'next_coords'

		while(True):

			next_coords = [next_coord(x) for x in prev_coords]

			if not check_is_still_moving(next_coords):
				still_flag = True

			flag = False

			# Deal with out of bounds animals

			for idx, coord in enumerate(next_coords):
				if not check_in_coord_bounds(coord):
					prev_coords[idx]['direction'] = STILL
					flag = True

			if flag == True:
				next_coords = None
				continue

			# For each animal in 'next_coords' determine \ 
			# if there are duplicates of the coordinate tuples.
			# Duplicates means two animals are in the same position, \
			# thus collision.

			coord_tuple_list = get_coord_tuple_list(next_coords)

			next_coord_indices = []  # Indices of all tuples

			for coord_tuple in coord_tuple_list:
				next_coord_indices.append(get_coord_indices(coord_tuple, coord_tuple_list))

			next_coord_indices = set(next_coord_indices) # All unique index positions

			next_len = len(next_coord_indices)

			if next_len < start_len:
				for partition in next_coord_indices:
					if len(partition) > 1:  # Duplicates
						for idx in partition:
							prev_coords[idx]['direction'] = STILL
				next_coords = None
				next_len = start_len
				continue
			else:
				if next_coords[0]['x'] == hole_coord[0] and \
				next_coords[0]['y'] == hole_coord[1]:
					del next_coords[0] # Delete mouse
					victory_flag = True

				board = setup_board(next_coords, hole_coord)
				draw_board(board, victory_flag, level_num)

			prev_coords = next_coords
			break

	if(input("Play again? (Press return to play again or q to quit): ") == 'q'):
		exit()
