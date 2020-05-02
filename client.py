# client.py
import socket
import pickle
import pandas as pd
import time
from io import StringIO

port = 8013
player_name = input("Howdy! Enter your name: ")

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get local machine name
host = socket.gethostname()
#player_name = host
print("Hi, " + player_name + "! Let's shuffle up and deal. \n")


# connection to hostname on the port.
s.connect((host, port))

# Receive no more than 1024 bytes
data = s.recv(4096*8)
data_int = pickle.loads(data)
#data_int = pickle.load(data_string)
# print the player's number and store their info
print("You're player:", data_int)
players = pd.read_pickle(".players.pkl")

players.update({data_int:player_name})
pd.to_pickle(players,".players.pkl")
players = pd.read_pickle(".players.pkl")
#print(players.values())


# print the game board
print("GAME BOARD:\n")
unpickled_df = pd.read_pickle(".board.pkl")
deck = unpickled_df.to_string(index=False, header=False)
print(deck,"\n")


# print your hand
list_of_hands = pd.read_pickle(".list_of_hands.pkl")
player_hand = list_of_hands[int(data_int)]
player_hand.sort()
print("YOUR HAND:\n ")
print(player_hand, "\n")

play = True
j = 0
while j < 10:
    #round 1
    j += 1
    round_1_card = input("Round " + str(j) +": Which card do you want to play? ")
    # remove the card from the player_hand (pop?)
    #re-read the pickle
    for i in range(len(player_hand)-1):
        if round_1_card == player_hand[i]:
            player_hand.pop(i)

    player_hand.remove(int(round_1_card))

    list_of_hands.update({int(data_int):player_hand})
    pd.to_pickle(list_of_hands,".list_of_hands.pkl")
    cards_in_play_this_round = pd.read_pickle(".cards_in_play_this_round.pkl")
    cards_in_play_this_round.update({int(data_int):round_1_card})
    pd.to_pickle(cards_in_play_this_round, ".cards_in_play_this_round.pkl")
    #we will need to clean this out, too.
    # if all players done = true
    all_players_gone = False
    old_slow_players = ""

    #we need to read in the pickle to get latest
    while not all_players_gone:
        #read the pickles to get latest values - this is not working
        cards_in_play_this_round = pd.read_pickle(".cards_in_play_this_round.pkl")
        players = pd.read_pickle(".players.pkl")
        #DEBUG print(cards_in_play_this_round.values())
        if list(cards_in_play_this_round.keys()) != list(players.keys()):
            # read in the names of the players done and minus them from the players list
            value = {k: players[k] for k in set(players) - set(cards_in_play_this_round)}
            slow_players = str(value.values())
            #if new slow_players == old slow players then don't show the message over and over again
            if old_slow_players != slow_players:
                print("Waiting for " + str(slow_players.replace("'", "").replace("(", "")).replace("[", "").replace(
                    "dict_values", "").replace(",", " and").replace("]", "").replace(")", "") + " to finish their move.")
            old_slow_players = slow_players
        else:
            all_players_gone = True

         #read the cards_in_play and update the_board

    board_updated = False
    while not board_updated:
        sorted_cards = sorted(cards_in_play_this_round.items(), key=lambda cards_in_play_this_round: cards_in_play_this_round[1])
        for i in range(len(sorted_cards) - 1):
            print(players.values()[sorted_cards.keys()[i]] + "played a " + sorted_cards.values()[i])
            # then we would add the cards to the game board, but first let's confirm numerical looping
            time.sleep(2)
            i += 1
        board_updated = True


        #print(cards_in_play_this_round)
    #create a list of all cards sorted from all players then add them to the matrix
    #
    #server needs to create a dictonary of cards played that round, sort them by value,
    #then work one by one adding them to the matrix, if any of them are in the 5th index
    #or sixth real position we need to total up the points, add tem to another dictionary
    #from the server then clean everything out and head to round 2, repeat to ten.
    #re-read the pickle


    #if we have any collisions then we will need to send to the server for centralized processing
    print("\nYOUR NEW HAND: ", player_hand, "\n")

print("Game over, thanks for playing.")
s.close()
