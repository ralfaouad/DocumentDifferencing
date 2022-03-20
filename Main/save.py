matrices = []
edit_scripts = []

def save_matrix(matrix):
    matrices.append(matrix)

def delete_matrix():
    if(len(matrices) != 0):
        matrices.pop()

def get_matrices():
    toReturn = list(reversed(matrices))
    return toReturn

def get_matrix(i):
    return matrices[i]

def save_script(script):
    edit_scripts.append(script)

def get_script():
    return edit_scripts
