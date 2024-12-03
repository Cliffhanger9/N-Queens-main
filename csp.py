
import random
import time

class nQueensCSP:
    
    def __init__(self, n):
        # n-queens is represented by a 1D list where each index is the column and the value at that index/column is the row that contains the queen
        #e.g. [0,2,1]
        #at column 0 the queen is in row 0
        #at column 1 the queen is in row 2
        #at column 2 the queen is in row 1
        
        self.n = n
        
        # list to keep track of conflicts in each row
        self.row_conflicts = [0] * n     
        
        # list to keep track of conflicts in each right diagonal (top left to bottom right)
        # row-col will be the same number for each element that is in the same diagonal
        # the min number that row-col could be is 0 - (n-1) = -(n-1) and the max number is (n-1) - 0 = n-1
        # so the range is -(n-1) to n-1 which is 2*n-1 (the size of this list) 
        self.rdiag_conflicts = [0] * (2 * n - 1)
        
        # list to keep track of conflicts in each left diagonal (top right to bottom left)
        self.ldiag_conflicts = [0] * (2 * n - 1)
        self.variables = [random.randint(0, n - 1) for _ in range(n)]
        self.conflicted_queens = set()
       
        row = 0
        # for each column on the board, this updates and tracks how many queens are in conflict in every row, rdiag, and ldiag
        for col in range(n):
            self.variables[col] = row
            self.row_conflicts[row] += 1
            self.rdiag_conflicts[row - col + (n - 1)] += 1
            self.ldiag_conflicts[row + col] += 1
            
            # Track conflicts
            if self.conflicts(col) > 0:
                self.conflicted_queens.add(col)
            
            # Move to the next row with 2 over and 1 down
            row = (col * 2) % n
        
        # CONFLICT LISTS ARE ALL CORRECT 
        # print("row_conflicts list:", self.row_conflicts) 
        # print("rdiag_conflicts list:", self.rdiag_conflicts) 
        # print("ldiag_conflicts list:", self.ldiag_conflicts) 


        
    def conflicts(self, col):

        row = self.variables[col]
        rdiag_index = row - col + (self.n - 1)
        ldiag_index = row + col


        total_conflicts = (
            self.row_conflicts[row] - 1 +
            self.ldiag_conflicts[ldiag_index] - 1 +
            self.rdiag_conflicts[rdiag_index] - 1
        )
        
        return total_conflicts


    
    def update_conflicted_queens(self, col):
        self.conflicted_queens.clear()
        
        # Reassess conflicts for all queens
        for col in range(self.n):
            if self.conflicts(col) > 0:
                self.conflicted_queens.add(col)

        
        #print(f"Updated conflicted queens: {self.conflicted_queens}")

    def is_valid_solution(self):
        if self.conflicted_queens:
            return False
        else:
            return True
    
    
    def move_queen(self, col, new_row):
    

        # storing original row queen was in
        old_row = self.variables[col]
        rdiag_index = old_row - col + (self.n - 1)
        ldiag_index = old_row + col
        
        
        # subtracting one conflict from each category now that the queen is being moved
        self.row_conflicts[old_row] -= 1
        self.rdiag_conflicts[rdiag_index] -= 1
        self.ldiag_conflicts[ldiag_index] -= 1
    
    
        # move the queen to new_row 
        self.variables[col] = new_row
        rdiag_index = new_row - col + (self.n - 1)
        ldiag_index = new_row + col
        
        
        # adding conflict in the new position's categories
        self.row_conflicts[new_row] += 1
        self.rdiag_conflicts[rdiag_index] += 1
        self.ldiag_conflicts[ldiag_index] += 1
    

        #print(f"queen is now at {self.conflicted_queens[col]}")
        self.update_conflicted_queens(col)
    
def print_board(state):
    n = len(state)
    for row in range(n):
        row_string = ""
        for col in range(n):  
            if state[col] == row:
                row_string += "Q "
            else:
                row_string += ". "
        print(row_string.strip()) 
    
