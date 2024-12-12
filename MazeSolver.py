import heapq
import copy
import sys

path = []

def solve_maze(matrix):
	# Find the start and end points of the maze
	start_x = 0
	start_y = 0
	for i in range(len(matrix)):
		if matrix[i][start_x] == 0:
			start_y = i
			break
	end_x = len(matrix[0]) - 1
	end_y = 0
	for i in range(len(matrix)):
		if matrix[i][end_x] == 0:
			end_y = i
			break

	# Initialize the priority queue and came_from dictionary
	queue = [(0, start_x, start_y)] # (distance, x, y)
	came_from = {(start_x, start_y): None}

	# Perform A* search
	while queue:
		distance, x, y = heapq.heappop(queue)
		if x < 0 or x >= len(matrix[0]) or y < 0 or y >= len(matrix) or matrix[y][x] != 0:
			continue
		if x == end_x and y == end_y:
			current = (x, y)
			while current is not None:
				x, y = current
				path.append((x, y))
				current = came_from.get(current)
			return
		matrix[y][x] = distance
		for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			nx, ny = x + dx, y + dy
			if (nx, ny) not in came_from:
				came_from[(nx, ny)] = (x, y)
				heapq.heappush(queue, (distance + abs(end_x - nx) + abs(end_y - ny), nx, ny))

def read_maze(file):
	f = open(file, "r")
	lines = f.readlines()
	temp = []
	for line in lines:
		temp.append(list(map(int, line.translate(str.maketrans('', '', '\n[],')).split())))
	return temp

def write_directions(directions):
	f = open("Directions.txt", "w")
	for dir in directions:
		f.write(dir + '\n')
	f.close()

if len(sys.argv) != 2:
	print("Invalid argument format: MazeSolver.py -[FILE_NAME]\nThe -[FILE_NAME] argument requires a text file containing a labyrinth in matrix form.")
	exit(1)
M = read_maze(sys.argv[1][1:])
N = copy.deepcopy(M)

solve_maze(M)

a, b = -1, -1
directions = []
while path:
	x, y = path.pop()
	N[y][x] = 2
	if a != -1 and b != -1:
		if a - x < 0:
			directions.append("RIGHT")
		elif a - x > 0:
			directions.append("LEFT")
		else:
			if b - y < 0:
				directions.append("DOWN")
			else:
				directions.append("UP")
	a, b = x, y

write_directions(directions)

for dir in directions:
	print(dir)

"""
M = [[1, 1, 1, 1, 1, 1, 1],
     [0, 0, 0, 0, 0, 0, 1],
     [1, 1, 1, 0, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 1, 1]]

print(path)
"""
