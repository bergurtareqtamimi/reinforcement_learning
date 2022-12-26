import math, copy, random



class Node:
    def __init__(self, board=[["","","","","","",""], ["","","","","","",""], ["","","","","","",""], ["","","","","","",""], ["","","","","","",""], ["","","","","","",""]], turn="🔵") -> None:
        self.parent: Node = None
        self.turn = turn
        self.board = board
        self.number_of_moves = self.calculate_number_of_moves()
        self.childs: list[Node] = []
        self.win = 0
        self.sim = 0
        self.last_move = -1
        self.rows = 6
        self.cols = 7
    
    def calculate_number_of_moves(self) -> int:
        moves = 0
        for i in self.board:
            for j in i:
                if j != "":
                    moves += 1
        return moves


    def get_legal_moves(self) -> list[int]:
        moves: list[int] = []
        for column in range(7):
            if self.is_space_available(column):
                moves.append(column)
        return moves

    def is_space_available(self, column: int) -> bool:
        if self.board[0][column] == "": return True
        return False
    
    def generate_new_board(self, move:int, piece: str) -> list[list[str]]:
        board = copy.deepcopy(self.board)
        for current_row in range(5, -1, -1):
            if board[current_row][move] == "":
                board[current_row][move] = piece
                return board


    def next_turn(self) -> str:
        if self.turn == "🔵":
            return "🔴"
        return "🔵"
    
    def check_for_winner(self, chip) -> bool:
        ### Check horizontal spaces
        for y in range(self.rows):
            for x in range(self.cols - 3):
                if self.board[y][x] == chip and self.board[y][x+1] == chip and self.board[y][x+2] == chip and self.board[y][x+3] == chip:
                    #print("\nGame over", chip, "wins! Thank you for playing :)")
                    return True

        ### Check vertical spaces
        for y in range(self.rows-3):
            for x in range(self.cols):
                if self.board[y][x] == chip and self.board[y+1][x] == chip and self.board[y+2][x] == chip and self.board[y+3][x] == chip:
                    #print("\nGame over", chip, "wins! Thank you for playing :)")
                    return True

        ### Check upper right to bottom left diagonal spaces
        for x in range(self.rows - 3):
            for y in range(3, self.cols):
                if self.board[x][y] == chip and self.board[x+1][y-1] == chip and self.board[x+2][y-2] == chip and self.board[x+3][y-3] == chip:
                    #print("\nGame over", chip, "wins! Thank you for playing :)")
                    return True

        ### Check upper left to bottom right diagonal spaces
        for x in range(self.rows - 3):
            for y in range(self.cols - 3):
                if self.board[x][y] == chip and self.board[x+1][y+1] == chip and self.board[x+2][y+2] == chip and self.board[x+3][y+3] == chip:
                    #print("\nGame over", chip, "wins! Thank you for playing :)")
                    return True
        return False

    def check_for_draw(self) -> bool:
        return self.number_of_moves == self.rows * self.cols
    
    def is_terminal(self) -> bool:
        if self.check_for_winner("🔵"): return True
        if self.check_for_winner("🔴"): return True
        if self.check_for_draw(): return True
        return False
    
    def is_leaf(self) -> bool:
        return self.childs == []
    
    def evaluation(self) -> float:
        if self.sim == 0: return float("inf")
        return self.win/self.sim + math.sqrt(2) * math.sqrt(self.parent.sim/self.sim)



class monte_carlo_tree_search:
    def __init__(self, board=None, turn=None) -> None:
        self.parent = Node(board, turn)
    
    def run(self, iterations:int):
        for _ in range(iterations):
            current_node = self.parent
            
            # SELECTION
            while not current_node.is_leaf(): 
                current_node = self.select_child(current_node)
            
            # EXPAND node when it is a leaf note(generate each child)
            actions = current_node.get_legal_moves()
            
            # create each child
            for action in actions:
                child = Node()
                child.parent = current_node
                child.turn = current_node.next_turn()
                child.board = current_node.generate_new_board(action, current_node.turn)
                child.number_of_moves += current_node.number_of_moves + 1
                child.last_move = action

                current_node.childs.append(child)

            # SIMULATE game from one of the child nodes
            current_node = current_node.childs[random.randint(0, len(current_node.childs)-1)]
            result = self.simulate(current_node)

            # BACKPROBAGATION
            self.backprobagation(current_node, result)

    def backprobagation(self, node:Node, result):
        node.win += result
        node.sim += 1

        if node.parent == None:
            return
        self.backprobagation(node.parent, result)

    def select_child(self, node: Node) -> Node:
        max_node = [-1, Node()]
        for child in node.childs:
            if child.evaluation() > max_node[0]:
                max_node[0] = child.evaluation()
                max_node[1] = child
        return max_node[1]

    def simulate(self, node: Node) -> int:
        if node.check_for_winner(self.parent.turn): return 1
        if node.check_for_winner(self.parent.next_turn()): return 0
        if node.check_for_draw(): return 0
        

        actions = node.get_legal_moves()
        action = actions[random.randint(0, len(actions)-1)]

        new_node = Node()
        node.next_turn()
        new_node.turn = node.next_turn()
        new_node.board = node.generate_new_board(action, node.turn)
        new_node.number_of_moves = node.number_of_moves + 1
        return self.simulate(new_node)

    def pick_move(self) -> int:
        best_node = [-1, Node()]
        for child in self.parent.childs:
            win_rate = child.win / child.sim
            if win_rate > best_node[0]:
                best_node = [win_rate, child]

        return best_node[1].last_move


mcts = monte_carlo_tree_search(
   [["","","","","","",""], 
    ["","","","","","",""], 
    ["","","","","","",""], 
    ["","","🔴","","","",""], 
    ["","🔵","🔴","🔴","🔵","",""], 
    ["🔴","🔵","🔵","🔵","🔴","",""]], 
    "🔵")

mcts.run(10000)
print(mcts.pick_move())












