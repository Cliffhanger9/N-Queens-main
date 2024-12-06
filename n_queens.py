import copy
from csp import nQueensCSP
import random
import time
import numpy as np
import matplotlib.pyplot as plt
# picks a random conflicted queen from the conflicted_queens set
def select_conflicted_queen(csp):
    return random.choice(list(csp.conflicted_queens))

# finds a position for a queen with the least conflicts
def find_better_position(csp, col):
    n = csp.n
    current_row = csp.variables[col]
    min_conflicts = csp.conflicts(col)
    best_rows = [current_row]
    
    for row in range(n):
        # don't evaluate the queen's current row
        if row == current_row:
            continue
        
        csp.variables[col] = row
        conflicts = csp.conflicts(col)
        # check whether the new position's conflicts are less than the minimum number of conflicts 
        if conflicts < min_conflicts:
            min_conflicts = conflicts
            # if yes, clear the current best_rows list and add the lowest conflict row
            best_rows = [row]
        elif conflicts == min_conflicts:
            # if they're the same, then append it to the existing list 
            best_rows.append(row)

    # if it's worse, than keep the queen in its original row
    csp.variables[col] = current_row
    # pick random choice from the best_rows to maintain variability
    return random.choice(best_rows)

# find the solution to the n-queens problem
def min_conflicts(csp, max_steps):
    for step in range(max_steps):
        if csp.is_valid_solution():
            print(f"Solution found in {step} steps")
            csp.conflicted_queens.clear()
            return csp.variables

        # select a random conflicted queen
        col = select_conflicted_queen(csp)
        # find a better position for that queen
        new_row = find_better_position(csp, col)
        # move the queen to that row
        csp.move_queen(col, new_row)

        # every 1000 steps, print a line that indicates how many queens are still in conflict
        if step % 1000 == 0:
            print(f"Step {step}: {len(csp.conflicted_queens)} queens in conflict")

    # if min_conflicts does not solve the problem within max_steps, it restarts
    print("Restart due to no progress.")
    return min_conflicts(nQueensCSP(len(csp.variables)), max_steps)

# prints solution in a board style
def print_board(state, file=None):
    n = len(state)
    for row in range(n):
        row_string = ""
        for col in range(n):  
            if state[col] == row:
                row_string += "Q "
            else:
                row_string += ". "
        if file:
            file.write(row_string.strip() + "\n") 
        else:
            print(row_string.strip())

def plot_placement_heatmap(csp, n, grid_size):
    #grid_size determines how many sub-grids
    #e.g. grid_size = 50 then heat map has 2500 sub-grids
    # num of sub grids = grid_size^2
    

    #section size determines how many rows and columns each sub-grid covers
    #e.g. 10k//50 = 200 so each grid covers 200 rows and columns
    section_size = n // grid_size
    heatmap = np.zeros((grid_size, grid_size))
    
    # Mark queen placements
    for col in range(n):
        row = csp.variables[col]
        x = int(col / section_size)  
        y = int(row / section_size) 
        heatmap[x, y] += 1  #count how many queens in subgrid
    
    

    plt.figure(figsize=(20, 20))
    plt.imshow(heatmap, cmap="Blues", interpolation="nearest", aspect="auto", vmax=heatmap.max())
    plt.colorbar(label="Queen Placements per sub-grid containing 200 rows and columns")
    plt.title(f"Queen Placement Heatmap for n = {n}")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    

    plt.show()
            
def main():

    queens = input("Please input the number of queens for the n-queens problem. (Make sure the number is not 2 or non-numeric).")
    while queens == "2" or queens.isnumeric() != True:
        queens = input("Please input the number of queens for the n-queens problem. (Make sure the number is not 2 or non-numeric).")
    
    # n = number of queens
    n = int(queens)
    max_steps = n * 100
    start_time = time.time()
    
    # creates instance of CSP with a certain nxn board
    csp = nQueensCSP(n)
    csp_initial_config = copy.deepcopy(csp)
    
    # call min_conflicts to solve the CSP
    solution = min_conflicts(csp, max_steps)
    
    end_time = time.time()
    plot_placement_heatmap(csp, n,grid_size=10)

    # write the relevant solution information to ouput.txt
    with open("output.txt", "w") as output_file:
        if n <= 100:
            output_file.write(f"initial board configuration:\n")
            print_board(csp_initial_config.variables, file = output_file)
        if solution:
            output_file.write(f"Solution to the {n}-queens problem found:\n")
            output_file.write(f"{solution}\n\n")
        
        # only print the board if the n is under 500, any bigger and the board becomes too large and unreadable
        if len(solution) < 1000:
            output_file.write("Final board configuration:\n")
            print_board(csp.variables, file=output_file)
    
        output_file.write("\nFinal conflicted queens: " + str(csp.conflicted_queens) + "\n")
        output_file.write("Solution check: " + str(csp.is_valid_solution()) + "\n")
        output_file.write(f"Execution time: {end_time - start_time:.2f} seconds\n")
    
if __name__ == "__main__":
    main()
