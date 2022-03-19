matrices = []
edit_scripts = []
def save_matrix(matrix):
    matrices.append(matrix)

def get_matrices():
    toReturn = list(reversed(matrices))
    return toReturn

def save_script(script):
    edit_scripts.append(script)

def get_script():
    toReturn = list(reversed(edit_scripts))
    return toReturn