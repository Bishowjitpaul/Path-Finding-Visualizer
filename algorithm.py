import queue
import math

#Mỗi ô trên board coi như là 1 node
class Node():

	def __init__(self, parent = None, position = None):
		self.parent = parent
		self.position = position

		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self, node):
		return self.position == node.position
		
	def __hash__(self):
		return hash(self.position)
	def __lt__(self, other): 
		if(self.f < other.f): 
			return True
		else: 
			return False

def create_child_node(maze, node):

	children = []
	
	for new_position in [(1, -1), (-1, 1), (-1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0),]:

		# Get child node position
		node_position = (node.position[0] + new_position[0], node.position[1] + new_position[1])

		# Make sure within range
		if node_position[0] <= (len(maze) - 1) and node_position[0] >= 0 and node_position[1] <= (len(maze[len(maze)-1]) -1) and node_position[1] >= 0:

			# Make sure walkable
			if maze[node_position[0]][node_position[1]] == 1:
				continue
			
			# Xét trường hợp tạo ô chéo thì không được vượt qua corner
			if new_position	== (1, -1):
				if node.position[1] >= 1 and node.position[0] < (len(maze) - 1) and maze[node.position[0]][node.position[1] - 1] == 1 and maze[node.position[0] + 1][node.position[1]] == 1:
					continue
			elif new_position == (-1, 1):
				if node.position[1] < (len(maze[len(maze)-1]) -1) and node.position[0] >= 1 and maze[node.position[0]][node.position[1] + 1] == 1 and maze[node.position[0] - 1][node.position[1]] == 1:
					continue
			elif new_position == (-1, -1):
				if node.position[1] >= 1 and node.position[0] >= 1 and maze[node.position[0]][node.position[1] - 1] == 1 and maze[node.position[0] - 1][node.position[1]] == 1:
					continue
					
			else:
				if node.position[1] + 1 <= (len(maze[len(maze)-1]) -1) and node.position[0] + 1 <= (len(maze) - 1) and maze[node.position[0]][node.position[1] + 1] == 1 and maze[node.position[0] + 1][node.position[1]] == 1:
					continue
								
			#Khúc trên sẽ cải tiến sau chứ nhìn ghê quá
			
			# Create new node
			new_node = Node(node, node_position)
			
			# Tính khoảng cách g
			#if new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
			if new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
				new_node.g = node.g + 1
			else:
				new_node.g = node.g + math.sqrt(2)
			
			
			
			children.append(new_node)
		
	return children
	
def get_path(node):
	path = []
	current = node
	while current is not None:
		path.append(current.position)
		current = current.parent

	return path[::-1] # Return reversed path	
	
	

def astar(maze, start, end, hType='Mahattan'):

	# Create start and end node
	start_node = Node(None, start)
	start_node.g = start_node.h = start_node.f = 0
	end_node = Node(None, end)
	end_node.g = end_node.h = end_node.f = 0

	# Initialize open and closed list
	open_list = []
	closed_list = set()
	traversal = []	#List thể hiện thứ tự duyệt, dùng cho visualizer


	# Add the start node
	open_list.append(start_node)

	# Loop until the end
	while len(open_list) > 0:

		# Get the current node
		current_node = open_list[0]
		index_min = 0
		
		# By finding node with smallest f
		for i in range(len(open_list)):
			if open_list[i].f < current_node.f:
				current_node = open_list[i]
				index_min = i

		# Pop current off open list, add to closed list
		open_list.pop(index_min)
		closed_list.add(current_node)
		

		# Found the goal
		if current_node == end_node:
			return traversal, get_path(current_node)
		
		#Create children node
		children = create_child_node(maze, current_node)
		

		# Loop through children
		for child in children:
		
			
			
			#Check if child is in the closed list
			if child in closed_list:
					continue
			
			#Calculate h
			if hType == 'Mahattan':
				child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
			else:
				child.h = math.sqrt((child.position[0] - end_node.position[0]) ** 2 + (child.position[1] - end_node.position[1]) ** 2)
			
			
			#Calculate f
			child.f = child.g + child.h
			
			
			#If child is already in the open list, replace it with smaller g node
			appear = False
			for open_node in open_list:
				if child == open_node:
					appear = True
					if child.g < open_node.g:
						open_node.g = child.g
						open_node.h = child.h
						open_node.f = child.f
						open_node.position = child.position
						open_node.parent = child.parent
						#NOTE: Khúc này không hiểu sao gán thẳng không được mà phải gán như vầy mới được
						
					break
			#Else
			if appear == False:		
				# Add the child to the open list
				open_list.append(child)
				
				if child.position != start_node.position and child.position != end_node.position:		
					traversal.append(child.position)
			
			
	#Open list empty but exit loop mean no path
	return traversal, -1

def bfs(maze, start, end):
	
	# Create start and end node
	start_node = Node(None, start)
	start_node.g = 0
	end_node = Node(None, end)
	end_node.g = 0
	
	#Queue for open node
	queue = []
	queue.append(start_node)
	
	#Visited set
	visited = set()
	visited.add(start_node)
	
	traversal = []
	
	while len(queue) > 0:
	
		#Pop node off queue
		current_node = queue[0]
		queue.pop(0)	#Queue is FIFO, so pop first node

		
		#If end
		if current_node.position == end:
			return traversal, get_path(current_node)
				
		
		#Create children node
		children = create_child_node(maze, current_node)
		
		for child in children:

			#Check if child is visited
			if child not in visited:
			
				visited.add(child)
				queue.append(child)
				
				if child.position != start_node.position and child.position != end_node.position:		
					traversal.append(child.position)
		
		
	
	return traversal, -1


#Dijkstra
def ucs(maze, start, end):
	
	start_node = Node(None, start)
	start_node.g = start_node.h = start_node.f = 0
	end_node = Node(None, end)
	end_node.g = end_node.h = end_node.f = 0
	
	
	q = []
	visited = set()

	# Add the start node
	q.append(start_node)
	traversal = []
	
	# Loop until the end
	while len(q) > 0:
		#Find smallest g node
		current_node = q[0]
		min_index = 0
		for i in range(len(q)):
			if q[i].g < current_node.g:
				current_node = q[i]
				min_index = i
			
		visited.add(current_node)
		q.pop(min_index)
		
		
		# Found the goal
		if current_node == end_node:
			
			return traversal, get_path(current_node)

		#Create children node
		children = create_child_node(maze, current_node)

		# Loop through children
		for child in children:
			
			if child in visited:
				continue
		
			#If child is already in the open list, replace with smaller g node
			appear = False
			for node in q:
				if child == node:
					appear = True
					if child.g < node.g:
						node.g = child.g
						node.parent = child.parent
						node.position = child.position
					break
			#Else append		
			if appear == False:
				q.append(child)
				if child.position != start_node.position and child.position != end_node.position:		
					traversal.append(child.position)

	
	#Open list empty but exit loop mean no path
	return traversal, -1
	
def dfs(maze, start, end):
	visited = set()
	
	# Create start and end node
	start_node = Node(None, start)
	end_node = Node(None, end)
	
	#Stack for open node
	stack = []
	stack.append(start_node)
	
	traversal = []
	
	while len(stack) > 0:
		
		# Get the current node
		current_node = stack[-1]

		# Pop current off open list
		stack.pop(-1)	#Stack is LIFP, so pop the last one
		
		#Chỗ này nhìn thì có vẻ không cần nhưng xóa đi thì lỗi
		if current_node not in visited:
			visited.add(current_node)
		
		
		#If end
		if current_node.position == end:
			return traversal, get_path(current_node)
				
		
		#Create children node
		children = create_child_node(maze, current_node)
		
		for child in children:
		
			if child not in visited:		
				stack.append(child)
				
				if child.position != start_node.position and child.position != end_node.position:		
					traversal.append(child.position)				
	
	return traversal, -1
	