import random
from Agent import IntelligentAgent

class Environment:
    def __init__(self, w=5, h=5) -> None:
        self.w = w
        self.h = h
        self.origin = (1,1)
        self.destination = (w, h)
        self.walls = []
        self.generate_walls()
        self.agent_loc = (1,1)


        self.agent = IntelligentAgent(self.origin)

    def generate_walls(self) -> None:
        ratio = 0.2
        area = self.w * self.h

        num_of_walls = int(ratio * area)

        for _ in range(num_of_walls):
            while True:
                new_loc = (random.randint(1,self.w), random.randint(1,self.h))

                if (not new_loc in self.walls) and new_loc != self.destination and new_loc != self.origin:
                    self.walls.append(new_loc)
                    break
        
        for i in range(self.w + 2):
            self.walls.append((i,0))
            self.walls.append((i, self.h + 1))
        
        for i in range(self.h + 2):
            self.walls.append((0 ,i))
            self.walls.append((self.w + 1 ,i))

    def print_board(self) -> None:
        for y in range(self.h + 2):
            for x in range(self.w + 2):
                if (x, y) in self.walls:
                    if x == self.w + 1:
                        print("X")
                    else:
                        print("X", end="")
                elif (x, y) == self.agent_loc:
                    if x == self.w + 1:
                        print("@")
                    else:
                        print("@", end="")
                else:
                    print("#", end="")
        print()

    def update_state(self, action:str) -> None:
        if action == "up": self.agent_loc = (self.agent_loc[0], self.agent_loc[1] - 1)
        if action == "down": self.agent_loc = (self.agent_loc[0], self.agent_loc[1] + 1)
        if action == "right": self.agent_loc = (self.agent_loc[0] + 1, self.agent_loc[1])
        if action == "left": self.agent_loc = (self.agent_loc[0] - 1, self.agent_loc[1])
    
    def bumped(self) -> bool:
        return self.agent_loc in self.walls
    
    def undo_action(self, action:str) -> None:
        if action == "up": self.agent_loc = (self.agent_loc[0], self.agent_loc[1] + 1)
        if action == "down": self.agent_loc = (self.agent_loc[0], self.agent_loc[1] - 1)
        if action == "right": self.agent_loc = (self.agent_loc[0] - 1, self.agent_loc[1])
        if action == "left": self.agent_loc = (self.agent_loc[0] + 1, self.agent_loc[1])

    def train(self, num_of_games=10) -> None:
        for _ in range(num_of_games):
            self.agent_loc = (1,1)
            

            steps = 0
            reward = 0

            while self.agent_loc != self.destination:
                self.agent.percieve_new_state(self.agent_loc, reward)

                steps += 1
                action = self.agent.do_action()
                self.update_state(action)
                
                if self.bumped():
                    reward = -5 
                    self.undo_action(action)
                else:
                    reward = 0

                
            
            
            self.agent.percieve_new_state(self.agent_loc, 10)


        self.print_board()
        print("Finished at ", self.agent_loc)
        print("STEPS: ",steps)
        print(self.agent.Qs)
            
                
    def test(self):
        path = []

        self.agent.exploitation = 1

        self.agent_loc = (1,1)
            

        count = 0
        reward = 0

        while self.agent_loc != self.destination:
            path.append(self.agent_loc)
            self.agent.percieve_new_state(self.agent_loc, reward)

            count += 1
            action = self.agent.do_action()
            self.update_state(action)
            
            if self.bumped():
                reward = -5 
                self.undo_action(action)
            else:
                reward = 0

            
        
        
        self.agent.percieve_new_state(self.agent_loc, 10)

        self.print_board()
        print("Finished at ", self.agent_loc)
        print("Path: ", path)
        print("STEPS: ",count)


