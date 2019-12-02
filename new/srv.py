
import socket
import time,datetime
from Env import *
#============
import pygame, random, numpy as np
from snake_agent import agent
from pygame.locals import *
#===========init game ============
def on_grid_random():
	x = random.randint(3, 56)
	y = random.randint(3, 56)

	return (x * 10, y * 10)
def add_to_snake_tail():
		snake.append((0, 0))
def collision(c1, c2):
	return (c1[0] == c2[0]) and (c1[1] == c2[1])

def init_server():
    global host,port
    host = setting.HOST
    port = setting.PORT  # initiate port no above 1024

def init_game():
    # Macro definition for snake movement.
    global UP,RIGHT,DOWN,LEFT,screen,food_board
    global snake,snake_skin,snake_energy ,my_direction
    global clock,font,score,movement,game_over
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Snake With AI =)')

    # Board
    food_board = np.random.randint(50, size=(60, 60))

    snake = [on_grid_random()]

    snake_skin = pygame.Surface((10, 10))
    snake_skin.fill((255, 255, 255))  # White
    snake_energy = 3

    my_direction = LEFT

    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 18)
    score = 0
    movement = 0

    game_over = False

#===========
def server_program():
    # get the hostname

    server_socket = socket.socket()  # get instance

    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        #======
        # clock.tick(7)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        #=====
        data=str(datetime.datetime.now())

        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    init_server()
    init_game()
    host = socket.gethostname()
    port = setting.PORT  # initiate port no above 1024

    while True:
        server_program()
        print('User is Offline')