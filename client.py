import socket
import threading
import pygame
import sys



WIDTH, HEIGHT = 700, 600
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fourplay")

font = pygame.font.sysFont("monospace", 40)

def draw_board(board):
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, (0,0,WIDTH,SQUARESIZE))

    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(7):
        for r in range(6):
            if board[r][c] == 'R':
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 'Y':
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# Client setup
HOST = '192.168.1.100'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

board = [[' ' for _ in range(7)] for _ in range(6)]
my_turn = False
symbol = ''
winner = False

def receive_messages():
    global my_turn, symbol, winner, color
    while True:
        try:
            #receive message from server
            message = client.recv(1024).decode()
            if message -- 'R' or message == 'Y':
                symbol =message
                color = 'Red' if symbol =='R' else 'Yellow'
                my_turn = (symbol =='R')
                if my_turn:
                    display_message("It is your turn ("+ color + ")")
                else:
                    display_message("Waiting for opponent turn")
            else:
                if message.startswith('WIN:'):
                    player_symbol, col = message[4:].split(':')
                    col = int(col)
                    for row in range(5, -1, -1):
                        if board[row][col] == ' ':
                            board[row][col] = player_symbol
                            break
                    winner = True
                    if player_symbol == symbol:
                        display_message("You win!")
                    else:
                        display_message("You lose!")
                    pygame.quit()
                    sys.exit()
                player_symbol, col = message.split(':')
                col = int(col)
                for row in range(5, -1, -1):
                    if board[row][col] == ' ':
                        board[row][col] = player_symbol
                        break
                draw_board(board)
                if player_symbol != symbol:
                    my_turn = True
                    display_message("It is your turn ("+ color +")")
                else:
                    display_message("Waiting for opponent turn")
        except Exception as e:
            print(f"Error: {e}")
            client.close()
            break

def send_move(col):
    client.sendall(f'{col}'.encode())

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

draw_board(board)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            posx = event.pos[0]
            if symbol == 'R':
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

       pygame
