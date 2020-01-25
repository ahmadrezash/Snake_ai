import socket
import time
from snake_agent import agent, Snake
from Env import *
import json


def client_program():
	host = socket.gethostname()  # as both code is running on same pc
	port = setting.PORT  # initiate port no above 1024

	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server
	data = {
			'action': 'Hi'
	}
	message = 'Start testing...'
	i = 0
	while True:
		# client_socket.send(message.encode())  # send message
		# client_socket.send(bytes(json.dumps(data), 'utf-8'))
		client_socket.send(bytes(json.dumps(data), 'utf-8'))
		print(f'{i}-th level')
		i += 1
		print('sending...')
		print('waiting...')
		data = client_socket.recv(10000).decode("utf-8")  # receive response
		print('recieved...')
		print(data)
		data = json.loads(json.loads(data))
		# data = json.loads((dict))
		# print(type(json.loads(data)))
		print(data['action'])  # show in terminal
		message = 'time?'
		data_bk = data
		if data['action'] == ActionItem.Next:
			dir = agent(board=data['board'],
			            snake=data['snake'],
			            snake_energy=data['snake_energy'],
			            score=data['score'],
			            )
			print(f'dir is {dir}')
		data = {
				'action': ActionItem.Next,
				'next': int(dir)
		}
	# conn.send(bytes(json.dumps(a), 'utf-8'))

	# message = input(" -> ")  # again take input

	client_socket.close()  # close the connection


if __name__ == '__main__':
	client_program()
