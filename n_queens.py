from csp import nQueensCSP
from csp import print_board
import random
import time

def select_conflicted_queen(csp):
    return random.choice(list(csp.conflicted_queens))

def find_better_position(csp, col):
    
    n = csp.n
    current_row = csp.variables[col]
    min_conflicts = csp.conflicts(col)
    best_rows = [current_row]
    
    for row in range(n):
        if row == current_row:
            continue
        csp.variables[col] = row
        conflicts = csp.conflicts(col)
        if conflicts < min_conflicts:
            min_conflicts = conflicts
            best_rows = [row]
        elif conflicts == min_conflicts:
            best_rows.append(row)

    csp.variables[col] = current_row
    return random.choice(best_rows)

def min_conflicts(csp, max_steps, debug=False):
    for step in range(max_steps):
        if csp.is_valid_solution():
            if debug:
                print(f"Solution found in {step} steps")
            return csp.variables

        col = select_conflicted_queen(csp)
        new_row = find_better_position(csp, col)
        csp.move_queen(col, new_row)

        if debug and step % 1000 == 0:
            print(f"Step {step}: {len(csp.conflicted_queens)} queens in conflict")

    print("Restart due to no progress.")
    return min_conflicts(nQueensCSP(len(csp.variables)), max_steps, debug=False)


def main():

    n = 10000
    max_steps = n * 10
    start_time = time.time()
    # creates instance of CSP with a certain nxn board
    csp = nQueensCSP(n)

    # print all queens's positions on board
    print("starting positions: ", csp.variables)
    
    # print("queens in conflict in col 1: ", csp.conflicts(0)) 
    # print("queens in conflict in col 2: ", csp.conflicts(1)) 
    # print("queens in conflict in col 3: ", csp.conflicts(2)) 
    # print("queens in conflict in col 4: ", csp.conflicts(3)) 
    
    # call min_conflicts to solve the CSP
    solution = min_conflicts(csp, max_steps, debug=True)
    
    end_time = time.time()
    # print the queens's positions after board was solved
    if solution:
        print(solution)

    # print_board(csp.variables)
    
    # should be nothing - set()
    print(f"Final conflicted queens: {csp.conflicted_queens}")

    
    # print("queens in conflict in col 1: ", csp.conflicts(0)) 
    # print("queens in conflict in col 2: ", csp.conflicts(1)) 
    # print("queens in conflict in col 3: ", csp.conflicts(2)) 
    # print("queens in conflict in col 4: ", csp.conflicts(3)) 

    print("solution check: ", csp.is_valid_solution())
    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
