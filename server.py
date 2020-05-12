# server.py
import socket
import time
import random
import pandas as pd
import numpy as np
import pickle

def shuffle_and_deal():
    full_deck = [i for i in np.arange(1, 112)]
    player1_hand = []
    player2_hand = []
    player3_hand = []
    player4_hand = []
    player5_hand = []
    player6_hand = []
    player7_hand = []
    player8_hand = []
    player9_hand = []
    player10_hand = []
    the_board = []
    i = 1
    # deal to players
    while i <= 10:
        card = full_deck.pop(random.randrange(len(full_deck)))
        player1_hand.append(card)

        card = full_deck.pop(random.randrange(len(full_deck)))
        player2_hand.append(card)

        card = full_deck.pop(random.randrange(len(full_deck)))
        player3_hand.append(card)

        card = full_deck.pop(random.randrange(len(full_deck)))
        player4_hand.append(card)

        card = full_deck.pop(random.randrange(len(full_deck)))
        player5_hand.append(card)

        card = full_deck.pop(random.randrange(len(full_deck)))
        player6_hand.append(card)

        card = full_deck.pop(random.randrange(len(full_deck)))
        player7_hand.append(card)

        card = full_deck.pop(random.randrange(len(full_deck)))
        player8_hand.append(card)

        card = full_deck.pop(random.randrange(len(full_deck)))
        player9_hand.append(card)

        card = full_deck.pop(random.randrange(len(full_deck)))
        player10_hand.append(card)
        i += 1

    remaining_deck = full_deck
    # deal the board
    i = 1
    while i <= 4:
        card = remaining_deck.pop(random.randrange(len(remaining_deck)))
        the_board.append(card)
        i += 1
    list_of_hands = {1: player1_hand, 2: player2_hand, 3: player3_hand, 4: player4_hand, 5:player5_hand,6: player6_hand, 7: player7_hand, 8:player8_hand, 9:player9_hand, 10:player10_hand}
    print("all hands", list_of_hands)
    print("remaining deck", remaining_deck)
    game_board = pd.DataFrame(np.array(the_board).reshape(4, 1))
    print("game board\n", game_board)

    cards_in_play_this_round = {}
    pd.to_pickle(cards_in_play_this_round, ".cards_in_play_this_round.pkl")
    pd.to_pickle(game_board, ".board.pkl")
    pd.to_pickle(list_of_hands, ".list_of_hands.pkl")

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 8139
# bind to the port
serversocket.bind((host, port))

# queue up to 10 requests
serversocket.listen(10)
number_of_connections = 0
shuffle_and_deal()
players = {}
pd.to_pickle(players, ".players.pkl")

scoreboard = {}
pd.to_pickle(scoreboard, ".scoreboard.pkl")
print("Let's get it!")
while True:
    #try:
    # establish a connection
    clientsocket,addr = serversocket.accept()

    number_of_connections += 1
    print("Got a connection from", str(addr[1]))
    print("We have this many players:", number_of_connections)
    data_string = pickle.dumps(number_of_connections)
    clientsocket.send(data_string)
    clientsocket.close()

    # Starting the first round

    #except:
        #clientsocket.close()
        #print("Closing...bye")
