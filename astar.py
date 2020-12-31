import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# We create a class for each square on the grid, and we name it Spot
class Spot:
        #the Spot will include its (x,y) coordinate, row, column, and other important info
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

        # returns the position of the spot on the grid
	def get_pos(self):
		return self.row, self.col

        # checks if the Spot is of the colour black, as this means it is a wall
	def is_barrier(self):
		return self.color == BLACK

        # resets a spot on the board, making its colour white again
	def reset(self):
		self.color = WHITE

        # sets the colour for the start point on the grid, which is orange
	def make_start(self):
		self.color = ORANGE

        # sets the colour for the searching path on the grid, which is blue
	def make_closed(self):
		self.color = BLUE
		
        # sets the colour for the open spots on the grid while we are searching, which are a darker blue colour
	def make_open(self):
		self.color = (0,0,150)

        # sets the colour for a wall on the grid, which is the colour black
	def make_barrier(self):
		self.color = BLACK

        # sets the colour for the end point on the grid, which is orange
	def make_end(self):
		self.color = ORANGE

        # sets the colour for the final path of the grid
	def make_path(self):
		self.color = YELLOW

        # makes a draw function for the stuff we want to draw on the grid
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

        # updates the list of neighbours near that spot on the grid
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Neighbour below the spot
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Neighbour above the spot
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Neighbour to the right of the spot
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Neighbour to the left of the spot
			self.neighbors.append(grid[self.row][self.col - 1])

# function for the distance between 2 points
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# function to draw the path from the start spot to the end spot
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

# the A-star algorithm that we use to actually search for the path to the end spot
def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
                
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] 
		open_set_hash.remove(current)

		if current == end: # if the current spot is the end spot, then construct the path from there
			reconstruct_path(came_from, end, draw)
			end.make_end() # make the current spot actually the end spot
			return True # return true to signal that the algorithm is over

		for neighbor in current.neighbors: # then we loop through the neighbours for all the spots
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
					
		draw() # draw the path to the end spot as it is being rendered

		if current != start:
			current.make_closed()

	return False

# function to initialize each spot in the 2-D array of the grid
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)
	return grid

# function to draw the actual lines on the grid
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# function to draw each spot on the grid
def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

# function that returns the row, col position on the spot that is clicked
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

# actual main endless loop so the program runs forever
def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width) #continously draws each spot on the grid
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #if we quit the program, end the loop
				run = False

			if pygame.mouse.get_pressed()[0]: #if we left click, then we want to be able to draw on the grid
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end: #if we haven't put down any walls, then our first click will give us the start spot
					start = spot
					start.make_start()

				elif not end and spot != start: #if we've already put down our start spot, we will then put down our end spot with the next click
					end = spot
					end.make_end()

				elif spot != end and spot != start: #otherwise, we just draw walls whenever we click
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #if we right click, then we want to erase the walls on the grid
				pos = pygame.mouse.get_pos() 
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start: #if we erase the starting spot, we set start = None
					start = None
				elif spot == end: #if we erase the ending spot, we set end = None
					end = None

			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_SPACE and start and end: #if we hit space, we start the algorithm
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid) #for each row/col in the grid, we update it

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) #run the algorithm

				if event.key == pygame.K_c: #if we hit the C key, we clear the board
					start = None
					end = None
					grid = make_grid(ROWS, width)
					
	pygame.quit()

main(WIN, WIDTH) #run the main function
