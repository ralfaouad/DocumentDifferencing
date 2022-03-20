matrices = []
edit_scripts = []

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

def del_matrices(i, j, n, m):
    # i,j -> indexes of current element in the matrix
    # n, m -> # of rows and columns in the matrix
    for i in range(n*m):
        matrices.remove(index+1)


def get_matrix(i):
    return matrices[i]

def save_script(script):
    edit_scripts.append(script)

def get_script():
    return edit_scripts
