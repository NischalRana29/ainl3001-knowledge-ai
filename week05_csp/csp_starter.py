"""
AINL3001 — Knowledge-Driven AI
Week 5 — Constraint Satisfaction Problems
BSP 2026

Australian map colouring: six regions and three colours.

Tasks
-----
0. Examine an invalid assignment.
1. Understand variables, domains and constraints.
2. Implement constraint checking.
3. Implement backtracking with simple variable selection.
4. Compare backtracking with brute force.
5. Improve variable selection using MRV.

Work in this starter file and commit your progress to your own fork.
"""

# --------------------------------------------------
# TASK 0 — MANUAL EXPLORATION
# --------------------------------------------------

example_assignment = {
    "WA": "Red",
    "NT": "Red",
    "SA": "Green",
    "Q": "Blue",
    "NSW": "Red",
    "V": "Green",
}

print("Manual CSP Exploration")
print(example_assignment)
print("\nQuestions:")
print("1. Is this assignment valid?")
print("2. Which neighbouring pairs violate a constraint?")
print("3. How could you correct the assignment?")
print("4. Why is it useful to detect violations early?")

# --------------------------------------------------
# TASK 1 — CSP REPRESENTATION
# --------------------------------------------------

# Each variable is an Australian region.
variables = ["WA", "NT", "SA", "Q", "NSW", "V"]

# Each region may use one of these three colours.
domains = {
    variable: ["Red", "Green", "Blue"]
    for variable in variables
}

# Each pair of neighbouring regions must have different colours.
constraints = [
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("Q", "NSW"),
    ("NSW", "V"),
]

# --------------------------------------------------
# TASK 2 — CONSTRAINT CHECKING
# --------------------------------------------------

def is_valid_assignment(assignment):
    for region1, region2 in constraints:
        if region1 in assignment and region2 in assignment:
            if assignment[region1] == assignment[region2]:
                return False
    return True


# --------------------------------------------------
# TASK 3 AND TASK 5 — VARIABLE SELECTION
# --------------------------------------------------

def select_unassigned_variable(assignment):
    """Task 3: simple selection."""
    for variable in variables:
        if variable not in assignment:
            return variable
    return None

def select_unassigned_variable(assignment):
    """Task 5: MRV"""
    best_variable = None
    fewest_legal_colours = float("inf")
    
    for variable in variables:
        if variable in assignment:
            continue
        
        legal_colours = 0
        for colour in domains[variable]:
            assignment[variable] = colour
            if is_valid_assignment(assignment):
                legal_colours += 1
            del assignment[variable]
            
        if legal_colours < fewest_legal_colours:
            fewest_legal_colours = legal_colours
            best_variable = variable
            
    return best_variable

# --------------------------------------------------
# TASK 3 — BACKTRACKING SEARCH
# --------------------------------------------------

def backtracking_search(assignment):
    """Return a complete valid assignment, or None if none exists."""
    if len(assignment) == len(variables):
        return assignment.copy()
    
    variable = select_unassigned_variable(assignment)
    
    for colour in domains[variable]:
        assignment[variable] = colour
        
        if is_valid_assignment(assignment):
            result = backtracking_search(assignment)
            if result is not None:
                return result
        
        del assignment[variable]

    return None


# --------------------------------------------------
# TASK 4 — BRUTE FORCE COMPARISON
# --------------------------------------------------

# Six regions with three possible colours each give 3 ** 6 = 729
# complete assignments. Why can backtracking avoid checking all 729?

# Once WA and NT are both Red, it never explores the 3^4 = 81 completions
# beneth that choice. Brute force would generate and check all 729.

# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("WEEK 5 — CONSTRAINT SATISFACTION PROBLEMS")
    print("=" * 50)

    print("\nVariables:", variables)
    print("Domains:", domains)
    print("Constraints:", constraints)

    print("\nExample assignment valid?")
    print(is_valid_assignment(example_assignment))  # Expected: False

    partial_assignment = {"WA": "Red", "NT": "Green"}
    print("\nPartial assignment valid?")
    print(is_valid_assignment(partial_assignment))  # Expected: True

    print("\nSearching for a solution...")
    solution = backtracking_search({})
    print("Solution:", solution)

    if solution is not None:
        print("\nSolution valid?", is_valid_assignment(solution))
        print("\nColour assignment:")
        for region in variables:
            print(f"{region:4} -> {solution[region]}")
    else:
        print("No solution yet. Complete the TODO sections.")

    print("\nPossible complete assignments:", 3 ** len(variables))
    print("\nReflection:")
    print("1. What causes backtracking?")
    print("2. Why can backtracking be faster than brute force?")
    print("3. Why might MRV reduce search?")
    print("4. How could this model represent timetabling?")