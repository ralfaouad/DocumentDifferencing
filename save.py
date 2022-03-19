matrices = []
def save_matrix(matrix):
    matrices.append(matrix)

def get_matrices():
    toReturn = list(reversed(matrices))
    return toReturn