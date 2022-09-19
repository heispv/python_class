import random

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # hala board ro besaz
        self.board = self.make_new_board()

        # adadi ke namayesh dade mishe ro mohasebe bokonim
        self.get_board_values()

        # Baraye inke biaim va khoone hayi ke baz shodan ro dashte bashim
        self.history = list()

    def get_board_values(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # in khoone bombe pas lazem nist ke value oon neshoon dade beshe
                    continue
                self.board[r][c] = self.calc_near_bombs(r, c)
    
    def calc_near_bombs(self, row, col):
        # bala chap: row-1, col-1
        # bala: row-1, col
        # bala rast: row-1, col+1
        # chap : row, col-1
        # khodesh: row, col
        # rast: row, col+1
        # pain chap: row+1, col-1
        # pain: row+1, col
        # pain rast: row+1, col+1
        total_near_bombs = 0
        for r in range(row-1, row+1 + 1):
            for c in range(col-1, col+1 + 1):
                if r == row and c == col:
                    # yani hamoon khoonas va lazem nist ke bebinim bomb hast toosh yana
                    continue
                if self.board[r][c] == '*':
                    # yani tooye oon khoone bomb hast, pas be bomb haye atraf yeki ezafe beshe
                    total_near_bombs += 1
        
        return total_near_bombs

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # mikhaim bomb haro be soorate random bezarim
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            # agar bomb gozashte boodim nemikhaim dobare bomb bezare pas bere iter e badi
            if board[row][col] == '*':
                continue
            
            # pas bomb bezarim
            board[row][col] = '*'
            bombs_planted += 1
        
        return board

def play(dim_size=10, num_bombs=10):
    # step 1 : sakhte board va gozashtane bomb ha
    # step 2 : be user board ro neshoon bedim va azash bekhaim yek jaro click bokone
    # step 3 : agar bomb bood user bakhte va agar bomb nabood be bazi edame bede
    # step 4 : bayad in karo enghad tekrar bokonim ta ya user bebaze ya inke bazi ro bebarim
    pass