import sys

def get_relative_direction(current_facing, new_direction):
    # Directions mapped to integers
    directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']

    # Get indices of current facing and new direction
    current_index = directions.index(current_facing)
    new_index = directions.index(new_direction)

    # Calculate the difference in direction (clockwise)
    diff = (new_index - current_index) % 4

    # Based on the difference, return the first person move
    if diff == 0:
        return "MOVE FORWARD"
    elif diff == 1:
        return "MOVE RIGHT"
    elif diff == 2:
        return "MOVE BACKWARD"
    elif diff == 3:
        return "MOVE LEFT"


def process_directions(starting_facing, directions):
    current_facing = starting_facing
    results = []

    for direction in directions:
        first_person_move = get_relative_direction(current_facing, direction)
        results.append(first_person_move)
        current_facing = direction  # Update the current facing to the new direction

    return results

def read_file(file):
	dir = []
	f = open(file, "r")
	line = f.readline()
	while True:
		line = line[:-1]
		if not line:
			break
		dir.append(line)
		line = f.readline()
	return dir

def write_file(instructions):
	f = open("Instructions.txt", "w")
	for instr in instructions:
		f.write(instr + '\n')
	f.close()


# Example usage
starting_facing = 'RIGHT'  # Initial facing direction
#directions = ['RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'LEFT', 'DOWN', 'RIGHT', 'UP']  # List of top-down directions

if len(sys.argv) != 2:
	print("Invalid argument format: GetDirections.py -[FILE_NAME]\n")
	exit(1)

directions = read_file(sys.argv[1][1:])

first_person_directions = process_directions(starting_facing, directions)
#for move in first_person_directions:
#    print(move)
write_file(first_person_directions)
