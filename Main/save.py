matrices = []
edit_scripts = []
def save_matrix(matrix):
    matrices.append(matrix)

def get_matrices():
    toReturn = list(reversed(matrices))
    return toReturn

def get_matrix(i):
    return matrices[i]
