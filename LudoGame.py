# Author: Ryan Canete
# GitHub username: rcanete26
# Date: 7/31/2022 Finished:8/10/2022
# Description: Is  representation of the Ludo game, that is playable.

# constants
player_state = ["Won", "Finished", "Still Playing"]


class LudoGame:
    """Represents a Ludo Game"""
    def __init__(self):
        """Initializes an empty dictionary that will hold all the players that are currently playing the game.
        Uses the player position as the key, and the value as the player object"""
        self.current_players = {}

    def play_game(self, player_list, turns_list):
        """Takes two parameters the player list(who will be playing) and the turns list(dice rolls for players)
        This method uses several other methods to play the Game of Ludo with the information given."""
        token_position_list = []
        winner = []
        for players in player_list:
            new_player = Player(players)
            self.current_players[players] = new_player
        for turns in turns_list:
            players = turns[0]
            steps = turns[1]
            if self.current_players[players].get_token_q_position() == "E" \
                    and self.current_players[players].get_token_q_position() == "E":
                if len(winner) == 0:
                    self.get_player_by_position(players).set_player_current_state(player_state[0])
                    winner.append(players)
                if len(winner) > 0:
                    self.get_player_by_position(players).set_player_current_state(player_state[1])
            self.movement_algo(self.get_player_by_position(players), steps)
        for player in self.current_players:
            token_position_list.append(self.current_players[player].get_token_p_position())
            token_position_list.append(self.current_players[player].get_token_q_position())
        return token_position_list

    def get_player_by_position(self, player_position):
        """Returns the player object, from a string."""
        if player_position not in self.current_players:
            return "Player not found!"
        else:
            return self.current_players[player_position]

    def move_token_stack(self, player_object, number_of_steps, key):
        """Is a special move method that handles all things when moving a stacked token."""
        if key == "E":
            player_object.increment_step_count_p(number_of_steps)
            player_object.increment_step_count_q(number_of_steps)
            player_object.set_token_p_position(key)
            player_object.set_token_q_position(key)
        if key == "H":
            player_object.increment_step_count_p(-(player_object.get_token_p_step_count()) + -1)
            player_object.increment_step_count_q(-(player_object.get_token_q_step_count()) + -1)
            player_object.set_token_p_position(key)
            player_object.set_token_q_position(key)
        else:
            while player_object.get_token_p_step_count() + number_of_steps > 57:
                current_value = player_object.get_token_p_step_count() + number_of_steps
                temp_value = current_value - 57
                actual_value = 57 - temp_value
                player_object.set_token_p_step_count(actual_value)
                player_object.set_token_q_step_count(actual_value)
                player_object.set_token_p_position(player_object.get_space_name(player_object.get_token_p_step_count()))
                player_object.set_token_q_position(player_object.get_space_name(player_object.get_token_p_step_count()))
                return
            player_object.increment_step_count_p(number_of_steps)
            player_object.increment_step_count_q(number_of_steps)
            player_object.set_token_p_position(player_object.get_space_name(player_object.get_token_p_step_count()))
            player_object.set_token_q_position(player_object.get_space_name(player_object.get_token_q_step_count()))

    def move_token(self, player_object, token_name, number_of_steps):
        """Will preform updating the token information and moving the token on the board, will get the token name
        parameter from the movement algo, which will determine what token will do."""

        if token_name == "Token P Ready":
            player_object.increment_step_count_p(1)

        if token_name == "Token Q Ready":
            player_object.increment_step_count_q(1)

        if token_name == "Token P Win":
            if player_object.get_token_p_step_count == player_object.get_token_q_step_count:
                return self.move_token_stack(player_object, number_of_steps, "E")
            player_object.increment_step_count_p(number_of_steps)
            player_object.set_token_p_position("E")

        if token_name == "Token Q Win":
            if player_object.get_token_p_step_count == player_object.get_token_q_step_count:
                return self.move_token_stack(player_object, number_of_steps, "E")
            player_object.increment_step_count_q(number_of_steps)
            player_object.set_token_q_position("E")

        if token_name == "Token P Kick":
            player_object.increment_step_count_p(number_of_steps)
            player_object.set_token_p_position(player_object.get_space_name(player_object.get_token_p_step_count()))
            for player in self.current_players:
                if player_object.get_position() != self.current_players[player].get_position():
                    token_p_new_space = player_object.get_space_name(player_object.get_token_p_step_count())
                    if self.current_players[player].get_token_p_position != "H" and "R" and "E":
                        if token_p_new_space == self.current_players[player].get_token_p_position() \
                                and self.current_players[player].get_token_q_position():
                            return self.move_token_stack(self.current_players[player], 0, "H")
                        if token_p_new_space == self.current_players[player].get_token_p_position():
                            self.current_players[player].increment_step_count_p(-(player_object.get_token_p_step_count()) + -1)
                            self.current_players[player].set_token_q_position("H")
                    if self.current_players[player].get_token_q_position != "H" and "R" and "E":
                        if token_p_new_space == self.current_players[player].get_token_q_position():
                            self.current_players[player].increment_step_count_q(-(player_object.get_token_q_step_count()) + -1)
                            self.current_players[player].set_token_q_position("H")

        if token_name == "Token Q Kick":
            player_object.increment_step_count_q(number_of_steps)
            player_object.set_token_q_position(player_object.get_space_name(player_object.get_token_q_step_count()))
            for player in self.current_players:
                if player_object.get_position() != self.current_players[player].get_position():
                    token_q_new_space = player_object.get_space_name(player_object.get_token_q_step_count())
                    if self.current_players[player].get_token_p_position != "H" and "R" and "E":
                        if token_q_new_space == self.current_players[player].get_token_p_position() \
                                and self.current_players[player].get_token_q_position():
                            return self.move_token_stack(self.current_players[player], 0, "H")
                        if token_q_new_space == self.current_players[player].get_token_p_position():
                            self.current_players[player].increment_step_count_p(-(player_object.get_token_p_step_count()) + -1)
                            self.current_players[player].set_token_q_position("H")
                    if self.current_players[player].get_token_q_position != "H" and "R" and "E":
                        if token_q_new_space == self.current_players[player].get_token_q_position():
                            self.current_players[player].increment_step_count_q(-(player_object.get_token_q_step_count()) + -1)
                            self.current_players[player].set_token_q_position("H")

        if token_name == "Token P Move":
            if player_object.get_token_p_step_count == player_object.get_token_q_step_count:
                if player_object.get_token_p_position() != "R" and player_object.get_token_q_position() != "R":
                    return self.move_token_stack(player_object, number_of_steps, "")
            while player_object.get_token_p_step_count() + number_of_steps > 57:
                current_value = player_object.get_token_p_step_count() + number_of_steps
                temp_value = current_value - 57
                actual_value = 57 - temp_value
                player_object.set_token_p_step_count(actual_value)
                player_object.set_token_p_position(player_object.get_space_name(player_object.get_token_p_step_count()))
                return
            player_object.increment_step_count_p(number_of_steps)
            player_object.set_token_p_position(player_object.get_space_name(player_object.get_token_p_step_count()))

        if token_name == "Token Q Move":
            if player_object.get_token_p_step_count == player_object.get_token_q_step_count:
                if player_object.get_token_p_position() != "R" and player_object.get_token_q_position() != "R":
                    return self.move_token_stack(player_object, number_of_steps, "")
            while player_object.get_token_q_step_count() + number_of_steps > 57:
                current_value = player_object.get_token_q_step_count() + number_of_steps
                temp_value = current_value - 57
                actual_value = 57 - temp_value
                player_object.set_token_q_step_count(actual_value)
                player_object.set_token_q_position(player_object.get_space_name(player_object.get_token_q_step_count()))
                return
            player_object.increment_step_count_q(number_of_steps)
            player_object.set_token_q_position(player_object.get_space_name(player_object.get_token_q_step_count()))
        return

    def movement_algo(self, player_object, number_of_steps):
        """Will have a player object and the number of steps, and will determine what action player will take,
        as well as which token to move."""

        if player_object.get_completed() == True:
            return

        if number_of_steps == 6 and player_object.get_token_p_position() == "H":
            player_object.set_token_p_position("R")
            return self.move_token(player_object, "Token P Ready", number_of_steps)

        if number_of_steps == 6 and player_object.get_token_q_position() == "H":
            player_object.set_token_q_position("R")
            return self.move_token(player_object, "Token Q Ready", number_of_steps)

        if number_of_steps + player_object.get_token_p_step_count() == 57:
            return self.move_token(player_object, "Token P Win", number_of_steps)

        if number_of_steps + player_object.get_token_q_step_count() == 57:
            return self.move_token(player_object, "Token Q Win", number_of_steps)

        for player in self.current_players:
            if player_object.get_position() != self.current_players[player].get_position():
                token_p_new_space = player_object.get_space_name(player_object.get_token_p_step_count() + number_of_steps)
                token_q_new_space = player_object.get_space_name(player_object.get_token_q_step_count() + number_of_steps)
                if self.current_players[player].get_token_p_position != "H" and "R" and "E":
                    if token_p_new_space == self.current_players[player].get_token_p_position():
                        return self.move_token(player_object, "Token P Kick", number_of_steps)
                    if token_q_new_space == self.current_players[player].get_token_p_position():
                        return self.move_token(player_object, "Token Q Kick", number_of_steps)
                if self.current_players[player].get_token_q_position != "H" and "R" and "E":
                    if token_q_new_space == self.current_players[player].get_token_q_position():
                        return self.move_token(player_object, "Token Q Kick", number_of_steps)
                    if token_p_new_space == self.current_players[player].get_token_q_position():
                        return self.move_token(player_object, "Token P Kick", number_of_steps)

        if player_object.get_token_p_position() != "H":
            if player_object.get_token_p_step_count() == player_object.get_token_q_step_count():
                if player_object.get_token_p_step_count() != 0:
                    return self.move_token_stack(player_object, number_of_steps, "")
                else:
                    return self.move_token(player_object, "Token P Move", number_of_steps)
            if player_object.get_token_p_step_count() < player_object.get_token_q_step_count():
                return self.move_token(player_object, "Token P Move", number_of_steps)
        elif player_object.get_token_q_position() != "H":
            return self.move_token(player_object, "Token Q Move", number_of_steps)

        if player_object.get_token_q_position() != "H":
            if player_object.get_token_q_step_count() == player_object.get_token_p_step_count():
                if player_object.get_token_p_step_count() != 0:
                    return self.move_token_stack(player_object, number_of_steps, "")
            if player_object.get_token_q_step_count() < player_object.get_token_p_step_count():
                return self.move_token(player_object, "Token Q Move", number_of_steps)

        elif player_object.get_token_p_position() != "H":
            return self.move_token(player_object, "Token P Move", number_of_steps)


class Player:
    def __init__(self, position):
        """Initializes a player, has several data members need to play the game. Also has unique data members
        based on the player being initialized."""
        self.position = position
        if position == "A":
            self.start = 1
            self.end = 50
        if position == "B":
            self.start = 15
            self.end = 8
        if position == "C":
            self.start = 29
            self.end = 22
        if position == "D":
            self.start = 43
            self.end = 36
        self.current_position_token_p = "H"
        self.current_position_token_q = "H"
        self.current_state = player_state[2]
        self.total_steps_token_p = -1
        self.total_steps_token_q = -1

    def get_completed(self):
        """Tells you if player is finished with the game or not. Returns True or False"""
        if self.current_state == player_state[0]:
            return True
        if self.current_state == player_state[1]:
            return True
        if self.current_state == player_state[2]:
            return False

    def set_token_p_step_count(self, steps):
        """Sets token p total steps"""
        self.total_steps_token_p = steps

    def set_token_q_step_count(self, steps):
        """Sets token q total steps"""
        self.total_steps_token_q = steps

    def set_player_current_state(self, state):
        """Sets the players current state, won, finished, or still playing"""
        self.current_state = state

    def get_player_current_state(self):
        return self.current_state

    def get_token_p_step_count(self):
        """returns the total player step count, but cannot exceed 57"""
        return self.total_steps_token_p

    def get_token_q_step_count(self):
        """return token q current total step count, but cannot exceed 57"""
        return self.total_steps_token_q

    def get_space_name(self, number_of_steps):
        """As a parameter takes the number of steps and returns the position of a token with that number of steps."""
        if number_of_steps == -1:
            return "H"
        if number_of_steps == 0:
            return "R"
        if number_of_steps == 57:
            return "E"
        if number_of_steps > 50:
            return f"{self.position}{number_of_steps - 50}"
        if self.position == "A":
            return str(number_of_steps)
        else:
            current_space = self.start + number_of_steps
            if current_space > 56:
                new_space = current_space - 56
                return str(new_space - 1)
            else:
                return str(current_space - 1)

    def set_token_p_position(self, position):
        """Sets the token p new position"""
        self.current_position_token_p = position

    def set_token_q_position(self, position):
        """Sets the token q new position"""
        self.current_position_token_q = position

    def get_token_p_position(self):
        """returns the position of token p"""
        return self.current_position_token_p

    def get_token_q_position(self):
        """returns the position of token q"""
        return self.current_position_token_q

    def get_position(self):
        """Returns the players position A, B, C, or D"""
        return self.position

    def increment_step_count_p(self, number_of_steps):
        """Increments the step count of p by adding the number of steps passed to it."""
        self.total_steps_token_p += number_of_steps

    def increment_step_count_q(self, number_of_steps):
        """Increments the step count of q by adding the number of steps passed to it."""
        self.total_steps_token_q += number_of_steps
