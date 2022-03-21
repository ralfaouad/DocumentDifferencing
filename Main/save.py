matrices = []
edit_scripts = []

def print_matrix(matrix):
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            print(matrix[r][c], end = "\t"*3)
        print()

def save_matrix(matrix):
    matrices.append(matrix)

def delete_matrix():
    if(len(matrices) != 0):
        matrices.pop()

def get_matrices():
    # toReturn = list(reversed(matrices))
    # toReturn = list(reversed(matrices))

    # return toReturn
    return matrices

def get_matrix():
    return matrices.pop()
