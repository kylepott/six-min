# client.py
import socket
import pickle
import pandas as pd
import time
import numpy as np
import random
from io import StringIO

def shuffle_and_deal():
    full_deck = [i for i in np.arange(1, 105)]
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
    #print("all hands", list_of_hands)
    #print("remaining deck", remaining_deck)
    game_board = pd.DataFrame(np.array(the_board).reshape(4, 1))
    #print("game board\n", game_board)

    cards_in_play_this_round = {}
    pd.to_pickle(cards_in_play_this_round, ".cards_in_play_this_round.pkl")
    pd.to_pickle(game_board, ".board.pkl")
    pd.to_pickle(list_of_hands, ".list_of_hands.pkl")



port = 8138
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

# initialize dealing
dealt = False
pd.to_pickle(dealt,".dealt.pkl")

players.update({data_int:player_name})
pd.to_pickle(players,".players.pkl")
players = pd.read_pickle(".players.pkl")
#print(players.values())
scoreboard = pd.read_pickle(".scoreboard.pkl")
score_tracker = 0
scoreboard.update({player_name:0})
pd.to_pickle(scoreboard,".scoreboard.pkl")
current_score = 0


scoreboard = pd.read_pickle(".scoreboard.pkl")
sorted_scoreboard = sorted(scoreboard.items(), key=lambda x: x[1])
highest_score = sorted_scoreboard[-1]
highest_score_redux = highest_score[1:2]
highest_score_redux_2 = str(highest_score_redux)
highest_score_redux_2 = highest_score_redux_2.replace("(","").replace(",","").replace(")","")

# get a new game board and hands from the server.
times_through = 0
dealt = False
while int(highest_score_redux_2) < 66:
    if times_through > 0:
        # this simulates player one being the dealer.
        # only one person should shuffle and deal and the other players should read in the pickle
        # or the random function causes everyone to have a random hand which results in repating numbers
        # as well as a random game board, different for each player which stops the game.
        if int(data_int) == 1:
            shuffle_and_deal()
            print("Let's shuffle up and deal another round!")
            dealer_is_done = True
            pd.to_pickle(dealer_is_done,".dealt.pkl")

        else:
            print("Let's shuffle up and deal another round!")
            while not dealt:
                time.sleep(6)
                dealt = pd.read_pickle(".dealt.pkl")

    # print the game board
    print("GAME BOARD:\n")
    unpickled_df = pd.read_pickle(".board.pkl")
    deck = unpickled_df.to_string(index=False, header=False)
    #print(deck,"\n")
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

    row_1_print = row_1.copy()
    row_2_print = row_2.copy()
    row_3_print = row_3.copy()
    row_4_print = row_4.copy()

    b = {k: scoring_dict[k] for k in scoring_dict.keys() & set(row_1_print)}
    c = {k: scoring_dict[k] for k in scoring_dict.keys() & set(row_2_print)}
    d = {k: scoring_dict[k] for k in scoring_dict.keys() & set(row_3_print)}
    e = {k: scoring_dict[k] for k in scoring_dict.keys() & set(row_4_print)}

    matching_points_card_row_1 = list(b.keys())
    matching_points_card_row_2 = list(c.keys())
    matching_points_card_row_3 = list(d.keys())
    matching_points_card_row_4 = list(e.keys())

    matching_points_bulls_row_1 = list(b.values())
    matching_points_bulls_row_2 = list(c.values())
    matching_points_bulls_row_3 = list(d.values())
    matching_points_bulls_row_4 = list(e.values())

    j = 0
    if len(matching_points_card_row_1) == 0:
        row_1_print = row_1.copy()
    else:
        for j in range(len(matching_points_card_row_1)):
            list_index = row_1_print.index(matching_points_card_row_1[j])
            replacer = str(matching_points_bulls_row_1[j])
            replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace("5","*****").replace("2", "**")
            row_1_print[list_index] = (str(matching_points_card_row_1[j]) + ":" + str(replacer2))
        j += 1
    row_1_print = str(row_1_print).replace("'", "").replace(":", " ")
    print(row_1_print)

    if len(matching_points_card_row_2) == 0:
        row_2_print = row_2.copy()
    else:
        for j in range(len(matching_points_card_row_2)):
            list_index = row_2_print.index(matching_points_card_row_2[j])
            replacer = str(matching_points_bulls_row_2[j])
            replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace("5",
                                                                                                              "*****").replace(
                "2", "**")
            row_2_print[list_index] = (str(matching_points_card_row_2[j]) + ":" + str(replacer2))
        j += 1
    row_2_print = str(row_2_print).replace("'", "").replace(":", " ")
    print(row_2_print)

    if len(matching_points_card_row_3) == 0:
        row_3_print = row_3.copy()
    else:
        for j in range(len(matching_points_card_row_3)):
            list_index = row_3_print.index(matching_points_card_row_3[j])
            replacer = str(matching_points_bulls_row_3[j])
            replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace("5",
                                                                                                              "*****").replace(
                "2", "**")
            row_3_print[list_index] = (str(matching_points_card_row_3[j]) + ":" + str(replacer2))
            j += 1
    row_3_print = str(row_3_print).replace("'", "").replace(":", " ")
    print(row_3_print)

    if len(matching_points_card_row_4) == 0:
        row_4_print = row_4.copy()
    else:
        for j in range(len(matching_points_card_row_4)):
            list_index = row_4_print.index(matching_points_card_row_4[j])
            replacer = str(matching_points_bulls_row_4[j])
            replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace("5",
                                                                                                              "*****").replace(
                "2", "**")
            row_4_print[list_index] = (str(matching_points_card_row_4[j]) + ":" + str(replacer2))
        j += 1
    row_4_print = str(row_4_print).replace("'", "").replace(":", " ")
    print(row_4_print)

    #print(row_1)
    #print(row_2)
    #print(row_3)
    #print(row_4)

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
            # I may need to pull the line below out and put it right abouve the print(pretty_hand_for_print) statement
            pretty_hand_for_print = str(player_hand_with_points).replace("'", "").replace(":", " ")
        j += 1
    print(pretty_hand_for_print, "\n")

    play = True
    round = 0
    while round < 10:

        scoreboard=pd.read_pickle(".scoreboard.pkl")
        #print("players",players_name)
        row_cleaner = -1
        pd.to_pickle(row_cleaner,".row_cleaner.pkl")

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
            # we currently have a mied tuple of (int, str) which is causing sorting issues - so we sort, convert to ints and re-sort
            sorted_cards = [tuple(int(ele) for ele in sub) for sub in sorted_cards]
            sorted_cards.sort(key=lambda x: x[1])
            #print("type", type(sorted_cards))
            #print(sorted_cards)
            i = 0
            for i in range(len(sorted_cards)):
                #time.sleep(2)
                spliter = list(sorted_cards[i])
                spliter = str(spliter).split(",")
                the_card = (spliter[1].replace("]", "").strip())
                the_player = (spliter[0]).replace("[", "").strip()
                players_name = list(players.values())
                #print("players_name",players_name)
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
                # loop list is looping for each player - we need to move higher up to see the order of players
                # loop list determines where to place each card.  We need to figure out the order of which card is being
                # played and we also need to make all hands wait while a row is selected if card is lower.
                #print("loop_list",loop_list)
                larger_than_any_row = any(p >= 0 for p in loop_list)
                # print(larger_than_any_row)
                # print(n)

                # I think we need a pickle here that all the clients read in to know that someone has a decision to make
                # and then re-read the game board???
                if larger_than_any_row:
                    n = min(i for i in loop_list if i > 0)
                    if loop_list.index(n) == 0:
                        if len(row_1) == 5:
                            # need to add up the score
                            score_tracker = 0
                            current_score = 0
                            row_1_score = row_1_print.split(",")
                            score_loop = 0
                            for score_loop in range(len(row_1_score)):
                                score_string = str(row_1_score[score_loop])
                                if score_string.count("*") == 0:
                                    score_tracker += 1
                                else:
                                    score_tracker += score_string.count("*")
                                score_loop += 1
                            print("Oh no, " + str(players_name[int(the_player) - 1]) + "! - You got Deep Sixed on row 1. For " + str(score_tracker) + " points.")
                            if players_name[int(the_player) - 1] == player_name:
                                scoreboard = pd.read_pickle(".scoreboard.pkl")
                                current_score = scoreboard.get(players_name[int(the_player) - 1])
                                current_score = int(current_score) + int(score_tracker)
                                scoreboard.update({players_name[int(the_player) - 1]: current_score})
                                pd.to_pickle(scoreboard, ".scoreboard.pkl")

                            row_1 = []
                        row_1.append(int(card))
                    elif loop_list.index(n) == 1:
                        if len(row_2) == 5:
                            # need to add up the score
                            score_tracker = 0
                            current_score = 0
                            row_2_score = row_2_print.split(",")
                            score_loop = 0
                            for score_loop in range(len(row_2_score)):
                                score_string = str(row_2_score[score_loop])
                                if score_string.count("*") == 0:
                                    score_tracker += 1
                                else:
                                    score_tracker += score_string.count("*")
                                score_loop += 1
                            print("Oh no, " + str(players_name[int(the_player) - 1]) + "! - You got Deep Sixed on row 2. For " + str(score_tracker) + " points.")
                            if players_name[int(the_player) - 1] == player_name:
                                scoreboard = pd.read_pickle(".scoreboard.pkl")
                                current_score = scoreboard.get(players_name[int(the_player) - 1])
                                current_score = int(current_score) + int(score_tracker)
                                scoreboard.update({players_name[int(the_player) - 1]: current_score})
                                pd.to_pickle(scoreboard, ".scoreboard.pkl")
                            row_2 = []
                        row_2.append(int(card))
                    elif loop_list.index(n) == 2:
                        if len(row_3) == 5:
                            # need to add up the score
                            score_tracker = 0
                            current_score = 0
                            row_3_score = row_3_print.split(",")
                            score_loop = 0
                            for score_loop in range(len(row_3_score)):
                                score_string = str(row_3_score[score_loop])
                                if score_string.count("*") == 0:
                                    score_tracker += 1
                                else:
                                    score_tracker += score_string.count("*")
                                score_loop += 1
                            print("Oh no, " + str(players_name[
                                int(the_player) - 1]) + "! - You got Deep Sixed on row 3. For " + str(score_tracker) + " points.")
                            if players_name[int(the_player) - 1] == player_name:
                                scoreboard = pd.read_pickle(".scoreboard.pkl")
                                current_score = scoreboard.get(players_name[int(the_player) - 1])
                                current_score = int(current_score) + int(score_tracker)
                                scoreboard.update({players_name[int(the_player) - 1]: current_score})
                                pd.to_pickle(scoreboard, ".scoreboard.pkl")
                            row_3 = []
                        row_3.append(int(card))
                    else:
                        if len(row_4) == 5:
                            # need to add up the score
                            score_tracker = 0
                            current_score = 0
                            row_4_score = row_4_print.split(",")
                            score_loop = 0
                            for score_loop in range(len(row_4_score)):
                                score_string = str(row_4_score[score_loop])
                                if score_string.count("*") == 0:
                                    score_tracker += 1
                                else:
                                    score_tracker += score_string.count("*")
                                score_loop += 1
                            print("Oh no, " + players_name[
                                int(the_player) - 1] + "! - You got Deep Sixed on row 4. For " + str(score_tracker) + " points.")
                            if players_name[int(the_player) - 1] == player_name:
                                scoreboard = pd.read_pickle(".scoreboard.pkl")
                                current_score = scoreboard.get(players_name[int(the_player) - 1])
                                current_score = int(current_score) + int(score_tracker)
                                scoreboard.update({players_name[int(the_player) - 1]: current_score})
                                pd.to_pickle(scoreboard, ".scoreboard.pkl")
                            row_4 = []
                        row_4.append(int(card))
                else:
                    # so only the player with the lower card gets to choose.
                    if players_name[int(the_player) - 1] == player_name:
                        row_cleaner = input("Oh no! Your card is less than every row! Which row are you going to take? ")
                        #print("row_cleaner",row_cleaner)
                        pd.to_pickle(row_cleaner,".row_cleaner.pkl")
                        #pickle the row cleaner
                        # should I put a pickle here that gives the value of row_cleaner
                        # then all players loop waiting for the other player to pick their card
                        # so if read pickle and row_cleaner <> -1 then go on otherwise wait time.sleep(2)
                        # then reset the pickle back to -1?

                    # all players will get this logic
                    # unpickle the row_cleaner
                    row_cleaner = pd.read_pickle(".row_cleaner.pkl")
                    ready_to_go = False
                    if int(row_cleaner) == -1:
                        print(players_name[int(the_player) - 1] + " has a lower card than the board.  Waiting for them to choose their row to take.")
                        while not ready_to_go:
                            time.sleep(1)
                            row_cleaner = pd.read_pickle(".row_cleaner.pkl")
                            #print(row_cleaner)
                            if row_cleaner != -1:
                                ready_to_go = True
                            else:
                                row_cleaner = pd.read_pickle(".row_cleaner.pkl")
                                #print(row_cleaner)
                        # read the pickle again and if it is still -1 kepe looping
                        # print(player_name has a lower card than the board, waiting for player_name to choose their row
                    if int(row_cleaner) == 1:
                        score_tracker = 0
                        current_score = 0
                        row_1_score = row_1_print.split(",")
                        score_loop = 0
                        for score_loop in range(len(row_1_score)):
                            score_string = str(row_1_score[score_loop])
                            if score_string.count("*") == 0:
                                score_tracker += 1
                            else:
                                score_tracker += score_string.count("*")
                            score_loop += 1
                        print("Oh no, " + str(players_name[int(the_player) - 1]) + "'s card is less than every row. " +
                                str(players_name[int(the_player) - 1]) + " took row number " + str(row_cleaner) +
                                ". " + str(players_name[int(the_player) - 1]) + " took " + str(score_tracker) + " points.")
                        # why is this coming back as none?
                        # only record this score if it is my score!!
                        if players_name[int(the_player) - 1] == player_name:
                            scoreboard = pd.read_pickle(".scoreboard.pkl")
                            current_score = scoreboard.get(players_name[int(the_player) - 1])
                            current_score = int(current_score) + int(score_tracker)
                            scoreboard.update({players_name[int(the_player) - 1]: current_score})
                            pd.to_pickle(scoreboard, ".scoreboard.pkl")

                        row_1 = []
                        row_1.append(int(card))
                    elif int(row_cleaner) == 2:
                        row_2_score = row_2_print.split(",")
                        score_tracker = 0
                        current_score = 0
                        score_loop = 0
                        for score_loop in range(len(row_2_score)):
                            score_string = str(row_2_score[score_loop])
                            if score_string.count("*") == 0:
                                score_tracker += 1
                            else:
                                score_tracker += score_string.count("*")
                            score_loop += 1
                        print("Oh no, " + str(players_name[int(the_player) - 1]) + "'s card is less than every row. " +
                              str(players_name[int(the_player) - 1]) + " took row number " + str(row_cleaner) +
                              ". " + str(players_name[int(the_player) - 1]) + " took " + str(score_tracker) + " points.")
                        if players_name[int(the_player) - 1] == player_name:
                            scoreboard = pd.read_pickle(".scoreboard.pkl")
                            current_score = scoreboard.get(players_name[int(the_player) - 1])
                            current_score = int(current_score) + int(score_tracker)
                            scoreboard.update({players_name[int(the_player) - 1]: current_score})
                            pd.to_pickle(scoreboard, ".scoreboard.pkl")

                        row_2 = []
                        row_2.append(int(card))

                    elif int(row_cleaner) == 3:
                        row_3_score = row_3_print.split(",")
                        score_tracker = 0
                        current_score = 0
                        score_loop = 0
                        for score_loop in range(len(row_3_score)):
                            score_string = str(row_3_score[score_loop])
                            if score_string.count("*") == 0:
                                score_tracker += 1
                            else:
                                score_tracker += score_string.count("*")
                            score_loop += 1
                        print("Oh no, " + str(players_name[int(the_player) - 1]) + "'s card is less than every row. " +
                              str(players_name[int(the_player) - 1]) + " took row number " + str(row_cleaner) +
                              ". " + str(players_name[int(the_player) - 1]) + " took " + str(score_tracker) + " points.")

                        if players_name[int(the_player) - 1] == player_name:
                            scoreboard = pd.read_pickle(".scoreboard.pkl")
                            current_score = scoreboard.get(players_name[int(the_player) - 1])
                            current_score = int(current_score) + int(score_tracker)
                            scoreboard.update({players_name[int(the_player) - 1]: current_score})
                            pd.to_pickle(scoreboard, ".scoreboard.pkl")
                        row_3 = []
                        row_3.append(int(card))
                        #print(scoreboard)
                    elif int(row_cleaner) == 4:
                        row_4_score = row_4_print.split(",")
                        score_tracker = 0
                        current_score = 0
                        score_loop = 0
                        for score_loop in range(len(row_4_score)):
                            score_string = str(row_4_score[score_loop])
                            if score_string.count("*") == 0:
                                score_tracker += 1
                            else:
                                score_tracker += score_string.count("*")
                            score_loop += 1
                        print("Oh no, " + str(players_name[int(the_player) - 1]) + "'s card is less than every row. " +
                              str(players_name[int(the_player) - 1]) + " took row number " + str(row_cleaner) +
                              ". " + str(players_name[int(the_player) - 1]) + " took " + str(score_tracker) + " points.")
                        if players_name[int(the_player) - 1] == player_name:
                            scoreboard = pd.read_pickle(".scoreboard.pkl")
                            current_score = scoreboard.get(players_name[int(the_player) - 1])
                            current_score = int(current_score) + int(score_tracker)
                            scoreboard.update({players_name[int(the_player) - 1]: current_score})
                            pd.to_pickle(scoreboard, ".scoreboard.pkl")
                        row_4 = []
                        row_4.append(int(card))

                row_1_print = row_1.copy()
                row_2_print = row_2.copy()
                row_3_print = row_3.copy()
                row_4_print = row_4.copy()

                b = {k: scoring_dict[k] for k in scoring_dict.keys() & set(row_1_print)}
                c = {k: scoring_dict[k] for k in scoring_dict.keys() & set(row_2_print)}
                d = {k: scoring_dict[k] for k in scoring_dict.keys() & set(row_3_print)}
                e = {k: scoring_dict[k] for k in scoring_dict.keys() & set(row_4_print)}

                matching_points_card_row_1 = list(b.keys())
                matching_points_card_row_2 = list(c.keys())
                matching_points_card_row_3 = list(d.keys())
                matching_points_card_row_4 = list(e.keys())

                matching_points_bulls_row_1 = list(b.values())
                matching_points_bulls_row_2 = list(c.values())
                matching_points_bulls_row_3 = list(d.values())
                matching_points_bulls_row_4 = list(e.values())

                j = 0
                if len(matching_points_card_row_1) == 0:
                    row_1_print = row_1.copy()
                else:
                    for j in range(len(matching_points_card_row_1)):
                        list_index = row_1_print.index(matching_points_card_row_1[j])
                        replacer = str(matching_points_bulls_row_1[j])
                        replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace(
                            "5", "*****").replace("2", "**")
                        row_1_print[list_index] = (str(matching_points_card_row_1[j]) + ":" + str(replacer2))
                    j += 1
                row_1_print = str(row_1_print).replace("'", "").replace(":", " ")
                print(row_1_print)

                if len(matching_points_card_row_2) == 0:
                    row_2_print = row_2.copy()
                else:
                    for j in range(len(matching_points_card_row_2)):
                        list_index = row_2_print.index(matching_points_card_row_2[j])
                        replacer = str(matching_points_bulls_row_2[j])
                        replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace(
                            "5",
                            "*****").replace(
                            "2", "**")
                        row_2_print[list_index] = (str(matching_points_card_row_2[j]) + ":" + str(replacer2))
                    j += 1
                row_2_print = str(row_2_print).replace("'", "").replace(":", " ")
                print(row_2_print)

                if len(matching_points_card_row_3) == 0:
                    row_3_print = row_3.copy()
                else:
                    for j in range(len(matching_points_card_row_3)):
                        list_index = row_3_print.index(matching_points_card_row_3[j])
                        replacer = str(matching_points_bulls_row_3[j])
                        replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace(
                            "5",
                            "*****").replace(
                            "2", "**")
                        row_3_print[list_index] = (str(matching_points_card_row_3[j]) + ":" + str(replacer2))
                        j += 1
                row_3_print = str(row_3_print).replace("'", "").replace(":", " ")
                print(row_3_print)

                if len(matching_points_card_row_4) == 0:
                    row_4_print = row_4.copy()
                else:
                    for j in range(len(matching_points_card_row_4)):
                        list_index = row_4_print.index(matching_points_card_row_4[j])
                        replacer = str(matching_points_bulls_row_4[j])
                        replacer2 = replacer.replace("3", "***").replace("8", "********").replace("7", "*******").replace(
                            "5",
                            "*****").replace(
                            "2", "**")
                        row_4_print[list_index] = (str(matching_points_card_row_4[j]) + ":" + str(replacer2))
                    j += 1
                row_4_print = str(row_4_print).replace("'", "").replace(":", " ")
                print(row_4_print, "\n")

                #print(row_1)
                #print(row_2)
                #print(row_3)
                #print(row_4)


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

        scorez = pd.read_pickle(".scoreboard.pkl")
        sorted_scorez = sorted(scorez.items(), key=lambda x: x[1])
        for i in range(len(sorted_scorez)):
            rep, rep2 = "",""
            rep = str(sorted_scorez[i])
            rep2 = rep.replace("'","").replace("(","").replace(")","").replace(",",":")
            print(rep2)
            i+=1
        pd.to_pickle(scorez,".scoreboard.pkl")
        print("\n")

    scorez2 = pd.read_pickle(".scoreboard.pkl")
    sorted_scorez2 = sorted(scorez2.items(), key=lambda x: x[1])
    highest_score = sorted_scorez2[-1]
    highest_score_redux = highest_score[1:2]
    highest_score_redux_2 = str(highest_score_redux)
    highest_score_redux_2 = highest_score_redux_2.replace("(", "").replace(",", "").replace(")", "")

    times_through += 1


print("Game over, thanks for playing.")
s.close()
