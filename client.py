# client.py
import socket
import pickle
import pandas as pd
import time
from io import StringIO

port = 8084
player_name = input("Howdy! Enter your name: ")

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get local machine name
host = socket.gethostname()
#player_name = host
print("Hi, " + player_name + "! Let's shuffle up and deal. \n")

#all the cards that have special scoring; if no match to the key, then program assumes it is one.
#let's start by showing the players their cards with the bulls heads in their hand
scoring_dict = {11:5,22:5,33:5,44:5,66:5,77:5,88:5,99:5,55:7,10:3,20:3,30:3,40:3,50:3,60:3,70:3,80:3,90:3,100:3,5:2,15:2,25:2,35:2,45:2,65:2,75:2,85:2,95:2}

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
# initialize the game board
row_1, row_2, row_3, row_4 = [], [], [], []
the_board = unpickled_df.values.tolist()
j = the_board[0]
j = str(j)
j = j.replace("[", "").replace("]", "")
k = the_board[1]
k = str(k)
k = k.replace("[", "").replace("]", "")
l = the_board[2]
l = str(l)
l = l.replace("[", "").replace("]", "")
q = the_board[3]
q = str(q)
q = q.replace("[", "").replace("]", "")
row_1.append(int(j))
row_2.append(int(k))
row_3.append(int(l))
row_4.append(int(q))

# print your hand
list_of_hands = pd.read_pickle(".list_of_hands.pkl")
player_hand = list_of_hands[int(data_int)]
player_hand.sort()
print("YOUR HAND:\n ")

player_hand_with_points = player_hand.copy()
n = {k: scoring_dict[k] for k in scoring_dict.keys() & set(player_hand)}

matching_points_card = (list(n.keys()))
matching_points_bulls = list(n.values())

j = 0
if len(matching_points_card) == 0:
    pretty_hand_for_print = player_hand.copy()
else:
    for j in range(len(matching_points_card)):
        player_hand_with_points.remove(matching_points_card[j])
        replacer = str(matching_points_bulls[j])
        replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace("5","*****").replace("2", "**")
        player_hand_with_points.append(str(matching_points_card[j]) + ":" + str(replacer2))
        pretty_hand_for_print = str(player_hand_with_points).replace("'", "").replace(":", " ")
    j += 1
print(pretty_hand_for_print, "\n")

play = True
round = 0
while round < 10:
    #round 1
    round += 1
    round_1_card = input("Round " + str(round) +": Which card do you want to play? ")
    # remove the card from the player_hand (pop)
    #re-read the pickle
    for i in range(len(player_hand)):
        if round_1_card == player_hand[i]:
            player_hand.pop(i)
            player_hand_with_points = player_hand.copy()

    player_hand.remove(int(round_1_card))
    player_hand_with_points = player_hand.copy()

    list_of_hands.update({int(data_int):player_hand})
    pd.to_pickle(list_of_hands,".list_of_hands.pkl")
    cards_in_play_this_round = pd.read_pickle(".cards_in_play_this_round.pkl")
    cards_in_play_this_round.update({int(data_int):round_1_card})
    i_went = True
    pd.to_pickle(cards_in_play_this_round, ".cards_in_play_this_round.pkl")
    time.sleep(1)
    #we will need to clean this out, too.
    # if all players done = true
    all_players_gone = False
    old_slow_players = ""

    #we need to read in the pickle to get latest
    while not all_players_gone:
        if i_went:
            time.sleep(2)
            #read the pickles to get latest values - this is not working
            cards_in_play_this_round = pd.read_pickle(".cards_in_play_this_round.pkl")
            players = pd.read_pickle(".players.pkl")
            #DEBUG print(cards_in_play_this_round.values())
            if list(cards_in_play_this_round.keys()) != list(players.keys()):
                # read in the names of the players done and minus them from the players list
                value = {k: players[k] for k in set(players) - set(cards_in_play_this_round)}
                slow_players = str(value.values())
                # I think this may have to be a global check - not just for one player - so pickle and unpickle all players_gone??
                if slow_players == "dict_values([])":
                    all_players_gone = True

                else:
                        #if new slow_players == old slow players then don't show the message over and over again
                        # we need the dict_values portion for when the slow players array is empty then we know
                        # it is time to move on.
                    if old_slow_players != slow_players:
                        print("Waiting for " + str(slow_players.replace("'", "").replace("(", "")).replace("[", "").replace(
                            "dict_values", "").replace(",", " and").replace("]", "").replace(")", "") + " to finish their move.")
                    old_slow_players = slow_players
            else:
                all_players_gone = True




    board_updated = False
    while not board_updated:




        sorted_cards = sorted(cards_in_play_this_round.items(), key=lambda cards_in_play_this_round: cards_in_play_this_round[1])


        #print(row_1)
        #print(row_2)
        #print(row_3)
        #print(row_4)

        row_cleaner = ""
        i = 0
        for i in range(len(sorted_cards)):
            time.sleep(2)
            spliter = list(sorted_cards[i])
            spliter = str(spliter).split(",")
            the_card = (spliter[1].replace("]", "").strip())
            the_player = (spliter[0]).replace("[", "").strip()
            players_name = list(players.values())
            print(players_name[int(the_player)-1] + " played: " + str(the_card).replace("'", "") + ".")
            #time.sleep(2)
            #print(type(the_card))
            card = the_card.replace("'","").replace('"', "")

            loop_list = []

            length_of_the_row_1 = len(row_1)
            length_of_the_row_2 = len(row_2)
            length_of_the_row_3 = len(row_3)
            length_of_the_row_4 = len(row_4)

            j = row_1[length_of_the_row_1 - 1]
            j = str(j)
            j = j.replace("[", "").replace("]", "")

            k = row_2[length_of_the_row_2 - 1]
            k = str(k)
            k = k.replace("[", "").replace("]", "")

            l = row_3[length_of_the_row_3 - 1]
            l = str(l)
            l = l.replace("[", "").replace("]", "")

            q = row_4[length_of_the_row_4 - 1]
            q = str(q)
            q = q.replace("[", "").replace("]", "")

            loop_list.append((int(card) - int(j)))
            loop_list.append((int(card) - int(k)))
            loop_list.append((int(card) - int(l)))
            loop_list.append((int(card) - int(q)))

            larger_than_any_row = any(p >= 0 for p in loop_list)
            # print(larger_than_any_row)
            # print(n)

            if larger_than_any_row:
                n = min(i for i in loop_list if i > 0)
                if loop_list.index(n) == 0:
                    if len(row_1) == 5:
                        row_1 = []
                        print("Oh no, " + players_name[
                            int(the_player) - 1] + "! - You got Deep Sixed on row 1. For 35 points.")
                        # need to add up the score
                    row_1.append(int(card))
                elif loop_list.index(n) == 1:
                    if len(row_2) == 5:
                        row_2 = []
                        print("Oh no, " + players_name[
                            int(the_player) - 1] + "! - You got Deep Sixed on row 2. For 35 points.")
                    row_2.append(int(card))
                elif loop_list.index(n) == 2:
                    if len(row_3) == 5:
                        row_3 = []
                        print("Oh no, " + players_name[
                            int(the_player) - 1] + "! - You got Deep Sixed on row 3. For 35 points.")
                    row_3.append(int(card))
                else:
                    if len(row_4) == 5:
                        row_4 = []
                        print("Oh no, " + players_name[
                            int(the_player) - 1] + "! - You got Deep Sixed on row 4. For 35 points.")
                    row_4.append(int(card))
            else:
                # so only the player with the lower card gets to choose.
                if players_name[int(the_player) - 1] == player_name:
                    row_cleaner = input("Oh no! Your card is less than every row! Which row are you going to take? ")
                if int(row_cleaner) == 1:
                    print("Oh no, " + players_name[int(the_player) - 1] + "'s card is less than every row. " +
                          players_name[int(the_player) - 1] + " took row number " + str(
                        row_cleaner) + ". He took 35 points.")
                    row_1 = []
                    row_1.append(int(card))
                elif int(row_cleaner) == 2:
                    print("Oh no, " + players_name[int(the_player) - 1] + "'s card is less than every row. " +
                          players_name[int(the_player) - 1] + " took row number " + str(
                        row_cleaner) + ". He took 35 points.")
                    row_2 = []
                    row_2.append(int(card))

                elif int(row_cleaner) == 3:
                    print("Oh no, " + players_name[int(the_player) - 1] + "'s card is less than every row. " +
                          players_name[int(the_player) - 1] + " took row number " + str(
                        row_cleaner) + ". He took 35 points.")
                    row_3 = []
                    row_3.append(int(card))

                elif int(row_cleaner) == 4:
                    print("Oh no, " + players_name[int(the_player) - 1] + "'s card is less than every row. " +
                          players_name[int(the_player) - 1] + " took row number " + str(
                        row_cleaner) + ". He took 35 points.")
                    row_4 = []
                    row_4.append(int(card))

            print(row_1)
            print(row_2)
            print(row_3)
            print(row_4)


            i += 1
            # then we would add the cards to the game board, but first let's confirm numerical looping
            time.sleep(2)

        board_updated = True

        if all_players_gone == True:
            #we need to zero some things out for the next round
            cards_in_play_this_round = {}
            pd.to_pickle(cards_in_play_this_round, ".cards_in_play_this_round.pkl")
            #print(".")




    #if we have any collisions then we will need to send to the server for centralized processing

    player_hand_with_points = player_hand.copy()
    n = {k: scoring_dict[k] for k in scoring_dict.keys() & set(player_hand)}

    matching_points_card = (list(n.keys()))
    matching_points_bulls = list(n.values())

    j = 0

    if len(matching_points_card) == 0:
        pretty_hand_for_print = player_hand.copy()
    else:
        for j in range(len(matching_points_card)):
            player_hand_with_points.remove(matching_points_card[j])
            replacer = str(matching_points_bulls[j])
            replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace("5","*****").replace("2", "**")
            player_hand_with_points.append(str(matching_points_card[j]) + ":" + str(replacer2))
            pretty_hand_for_print = str(player_hand_with_points).replace("'", "").replace(":", " ")
        j += 1
    print("\nYOUR HAND: ", pretty_hand_for_print, "\n")

print("Game over, thanks for playing.")
s.close()
