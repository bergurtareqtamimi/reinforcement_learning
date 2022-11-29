import random



class IntelligentAgent:
    def __init__(self, loc: tuple) -> None:
        self.current_loc = loc
        self.Qs : dict[list[tuple]] = dict() # dict[(2,3):[("up", 0),("down", 0),("left", 0),("right", 0)]
        self.previous_state = None
        self.previous_action = None
        self.learning_rate = 0.5
        self.discount_factor = 0.9
        self.exploitation = 0.6
    
    def get_legal_actions(self) -> list[str]:
        return ["up", "down", "right", "left"]

    def do_action(self) -> str:
        picked_action = self.pick_action()
        self.previous_action = picked_action

        return picked_action
    
    def pick_action(self) -> str:
        seed = random.uniform(0,1)

        if seed <= self.exploitation:
            # pick the current best action
            top_act_val = ("None", -100000)
            for action_value in self.Qs[self.current_loc]:
                if action_value[1] > top_act_val[1]:
                    top_act_val = action_value
            return top_act_val[0]
        else:
            # try random action
            return self.Qs[self.current_loc][random.randint(0, len(self.Qs[self.current_loc]) - 1)]


    def percieve_new_state(self, new_state : tuple, reward : int) -> None:
        self.previous_state = self.current_loc

        self.current_loc = new_state

        self.check_if_stored(new_state)

        # update previous state value
        self.update_state_value(reward)
        


    def update_state_value(self, reward) -> None:
        for action_value in self.Qs[self.previous_state]:
            if action_value[0] == self.previous_action:
                temp_action_value = action_value
                self.Qs[self.previous_state].append((temp_action_value[0], self.update_q(reward, self.q_value(self.previous_state, self.previous_action), self.max_q(self.current_loc), self.discount_factor, self.learning_rate)))
                self.Qs[self.previous_state].remove(temp_action_value)



    def check_if_stored(self, state) -> None:
        if state not in self.Qs:
            self.Qs[state] = [(action, 0) for action in self.get_legal_actions()]

    
    def max_q(self, state) -> float:
        max_val = -1000000
        for action_value in self.Qs[state]:
            if action_value[1] > max_val:
                max_val = action_value[1]
        return max_val
    
    def q_value(self, state, action) -> float:
        for action_value in self.Qs[state]:
            if action_value[0] == action:
                return action_value[1]

    def update_q(self, reward, q1, max_q2, discount, learning_rate) -> float:   
        return q1 + learning_rate * (reward + discount * max_q2 - q1)
