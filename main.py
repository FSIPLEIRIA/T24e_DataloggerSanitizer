import sys
import numpy as np
import json

"""
Developed by carlostojal - may 2023
(autonomous driving department rules :))
"""

# parse the int bytes from an int array i.e. bit masking and shifting
def parseFromIntArray(array):
    n_bytes = len(array)
    out = 0
    for b in range(n_bytes):
        out |= array[b] << (n_bytes - b - 1) * 8
    return out

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
print(config)
print("Done!")

# load csv file to numpy matrix
print("Reading the data...", end='')
mat = np.loadtxt(sys.argv[1], delimiter=';', dtype=int)
print("Done!")

# slice the IDs based on the config
ids_vector = mat[0:config['n_ids'],0]

# remove the IDs column from the matrix
mat = mat[:,1:]

# iterate the matrix rows
curr_row = 0
while curr_row < mat.shape[0]:

    # iterate the IDs
    for id_index in range(config['n_ids']):

        # find the frame ID on configuration to parse bytes
        for frame_config in config['structure']:
            if int(frame_config['can_id'], 16) == int(ids_vector[id_index]):
                # iterate the variables on the configuration to get the matrix values
                cur_byte_index = 0
                for v in range(len(frame_config['vars'])):
                    # calculate the ending byte of this variable
                    ending_byte = cur_byte_index + frame_config['vars'][v]['length']

                    # convert the byte array to the integer value
                    int_val = parseFromIntArray(mat[curr_row][cur_byte_index:ending_byte])

                    # show the result
                    print(f"{frame_config['vars'][v]['name']}: {int_val}")

                    # the new starting byte index of the row is the last ending byte
                    cur_byte_index = ending_byte

        # change to the next matrix row
        curr_row += 1

    print()

    # change to the next timestep
    curr_row += config['n_ids_max'] - config['n_ids']
