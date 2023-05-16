import sys
import numpy as np
import json

# check for command line arguments
if len(sys.argv) == 1:
    print("Insufficient arguments provided!")
    print(f"Usage: python {sys.argv[0]} [filename.csv]")
    sys.exit(-1)

# load configuration file
print("Reading CAN configuration...", end='')
f = open("can_config.json", "r")
config = json.loads(f.read())
f.close()
print("Done!")

# load csv file to numpy matrix
print("Loading the data...", end='')
mat = np.loadtxt(sys.argv[1], delimiter=';')
# print(mat)
print("Done!")

# slice the IDs based on the config
ids_vector = mat[0:config['n_ids'],0]
print(ids_vector)

# iterate the matrix rows
curr_row = 0
while curr_row < mat.shape[0]:
    curr_timestep = curr_row % config['n_ids_max']

    curr_row += 1