from random import randint					#Allows us to place food randomly
from sense_hat import SenseHat				#Library that controls the Sense Hat
from time import sleep						#Allows us to pause our program




#This is called a class.  It is like a blueprint for creating objects.
#The following link provides a detailed but advanced explanation of classes in python:
# https://www.python-course.eu/python3_object_oriented_programming.php
class snakeGame():
	
	#All of the following def statements are called methods.  They are very similar
	#	to functions except they are called inside classes and the first argument is
	#	always 'self'
	
	#The __init__ method is called as soon as a snake instance is created. (This is
	#	accomplished by snake = snake(difficulty=diff) on line 175.)
	def __init__(self, bg_color = (0,0,0), snake_color = (255,255,255), \
		food_color = (0,255,0), difficulty = 'easy'):
		
		#We used keyword parameters to define this method.  That means we can call it
		#	with only the parameters we want to change.  The others will be automatically
		#	set to the default values above.
	
		self.bg_color = bg_color			#Background color
		self.snake_color = snake_color		#Snake color
		self.food_color = food_color		#Food color
	
		self.difficulty = difficulty		#Difficulty setting
	
		#The following are called dictionaries.  We use them to change speed setting
		#	and score multiplier according to difficulty.
		self.speed = {'easy': 0.5,'medium': 0.3, 'hard': 0.1}
		self.multiplier = {'easy': 0.5, 'medium': 1, 'hard': 2}
	
	#Method to initialize game.  This doesn't run until we call 'snake.startGame()'	
	def startGame(self):
		sense.clear(self.bg_color)			#Sets background to bg_color
		self.direction = 'up'				#Snake starts moving up
		self.length = 3						#Initial snake length
		self.tail = [(4,4),(4,5),(4,6)]		#Starting position  
		
		#Draws snake
		for pixel in self.tail:
			sense.set_pixel(pixel[0],pixel[1],self.snake_color)
		
		self.createFood()					#This method places food randomly					
		self.score = 0						#Initializes score to zero
      
		#The following listens for joystick presses and calls move method.
		#If move returns True, keep playing.  If it returns false, game ends.
		playing = True
		while playing:
			#Adjusts speed according to difficulty
			sleep(self.speed[self.difficulty])
			for event in sense.stick.get_events():
				self._handle_event(event)
			playing = self.move()
		
		del self
    

	#This method is called during the "while playing" loop above.  It's sole purpose
	#	is to call the functions that change the snake's direction.
	def _handle_event(self, event):
		if event.direction == 'up':
			self.up()
		elif event.direction == 'down':
			self.down()
		elif event.direction == 'left':
			self.left()
		elif event.direction == 'right':
			self.right()
    

	#This method places food in a random location.  It creates a random integer for
	#	x and y and checks if that location is inside the snake using .checkCollision
	#	method.  If there is a collision, it generates a new x and y.
	def createFood(self):
		badFood = True
		while badFood:
			x = randint(0,7)				#'x' and 'y' don't have 'self.' infront of them.
			y = randint(0,7)				#	Thus, they are local to this method only. 
			badFood = self.checkCollision(x,y)
		self.food = [x,y]
		sense.set_pixel(x,y,self.food_color)



	#This method checks if the snake has hit a wall or itself.  Also used in createFood()
	def checkCollision(self, x, y):
		if x > 7 or x < 0 or y > 7 or y < 0:
			return True
		else:
			for segment in self.tail:
				if segment[0] == x and segment[1] == y:
					return True  
			return False
     

	#This method is used by move.  It adds a segment to the front of the snake and
	#	deletes a segment from the end of a snake using .pop().  If the snake just ate
	#	its length would increase by one and the last segment would not be deleted.
	def addSegment(self, x, y):
		sense.set_pixel(x,y,self.snake_color)
		self.tail.insert(0, (x, y))
		
		if len(self.tail) > self.length:
			lastSegment = self.tail[-1]
			sense.set_pixel(lastSegment[0],lastSegment[1], self.bg_color)
			self.tail.pop()
      


	#This method is responsible for snake movement.  It creates a new segment depending
	#	on the snake.direction attribute.  If the new segment passes .checkCollision
	#	it calls .addSegment.  If there is a collision, endgame procedure occurs.
	def move(self):
		newSegment = [self.tail[0][0], self.tail[0][1]]
		if self.direction == 'up':
			newSegment[1] -= 1
		elif self.direction == 'down':
			newSegment[1] += 1
		elif self.direction == 'left':
			newSegment[0] -= 1
		elif self.direction == 'right':
			newSegment[0] += 1
          
		if self.checkCollision(newSegment[0],newSegment[1]):
			snakehead = self.tail[0]
			for flashHead in range(0,5):
				sense.set_pixel(snakehead[0],snakehead[1], self.snake_color)
				sleep(0.2)
				sense.set_pixel(snakehead[0], snakehead[1], 255, 0, 0)
				sleep(0.2)
			sense.show_message("GAME OVER", scroll_speed = 0.05)
			sense.show_message("Score = " + str(self.score), scroll_speed = 0.05)
			return False
			
		else:
			self.addSegment(newSegment[0], newSegment[1])
		
			#Checks if snake just ate.  If so, length and score are increased and
			#	new food is created.
			if newSegment[0] == self.food[0] and newSegment[1] == self.food[1]:
				self.length += 1
				self.score += 10 * self.multiplier[self.difficulty]
				self.createFood()
			
			return True
 


	#These functions ensure the snake does not flip directions.  They are called
	#	by ._handle_event.
	def up(self):
		if self.direction != 'down':
			self.direction = 'up'
	
	def down(self):
		if self.direction != 'up':
			self.direction = 'down'
		
	def left(self):
		if self.direction != 'right':
			self.direction = 'left'
		
	def right(self):
		if self.direction != 'left':
			self.direction = 'right'
		
#The if statement just ensures that senseHat snake.py is the main module running,
#	not an imported module.  This is unnecessary here, but it is a very common 
#	convention.  For further information, see the following Stack Overflow post:
#	https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
	sense = SenseHat()						#This creates an instance of SenseHat()
											#	called sense


	diff = None								#Difficulty to be set by main script
	
	running = True							#Allows the following while loop to exit
											#	by setting running to False
											
	#Prompts user for difficulty setting.  If user inputs something besides up, right,
	#	or down, asks user if script should quit.  After setting difficulty, begins 
	#	game with difficulty settings.
	while running:
		sense.show_message("PRESS UP FOR HARD, RIGHT FOR MEDIUM, DOWN FOR EASY", scroll_speed = 0.05)
		event = sense.stick.wait_for_event(emptybuffer=True)
		if event.direction == 'up':
			diff = 'hard'
		elif event.direction == 'right':
			diff = 'medium'
		elif event.direction == 'down':
			diff = 'easy'
		else:
			sense.show_message("WOULD YOU LIKE TO EXIT? PRESS UP FOR yes, DOWN FOR NO.", scroll_speed = 0.05)
			event = sense.stick.wait_for_event(emptybuffer=True)
			if event.direction == 'up':
				running = False
				break
			else:
				continue
	
		sense.show_message("Difficulty: " + diff.upper(), scroll_speed = 0.05)
		sense.show_message("PRESS JOY TO BEGIN", scroll_speed = 0.05)
		event = sense.stick.wait_for_event(emptybuffer=True)
		if event.action == 'pressed':
			snake = snakeGame(difficulty = diff)
			snake.startGame()
		
	
	
	

	
	
	
	
	