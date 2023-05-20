import sys
import numpy as np
import json
import threading
import os

"""
Developed by carlostojal - may 2023
(autonomous driving department rules :))
(the autonomous software is more optimized than this, trust me)
"""

# parse the int bytes from an int array i.e. bit masking and shifting
def parseFromIntArray(array):
    n_bytes = len(array)
    out = 0
    for b in range(n_bytes):
        out |= array[b] << (n_bytes - b - 1) * 8
    return out

def loadFile(path, separator):
    # open the file
    with open(path, "r") as f:
        data = f.read()

    # line breaks differ from Linux to Windows (\n vs \r\n), so the splitting is different
    lines = data.split(os.linesep)

    # remove the first line: header line
    lines.pop(0)

    # print(lines)

    out = list()

    for l in lines:
        # split each line by ";"
        l = l.split(separator)
        # create a list to the new line
        new_line = list()
        # convert to int
        for c in l:
            try:
                c = int(c)
            except ValueError:
                c = 0
            new_line.append(c)
        out.append(new_line)

    # convert to a numpy matrix
    # mat = np.matrix(out)
    mat = np.array(out)

    return mat

def file_processing_routine(full_path):
    """
    PROCESS EACH FILE OF THE DIRECTORY
    """
    # load csv file to numpy matrix
    print("Reading the input file...", end='')
    mat = loadFile(os.path.join(sys.argv[1], file), ';')
    print("Done!")

    # slice the IDs based on the config
    # ids_vector = mat[0:can_struct['n_ids'], 0]
    ids_vector = list()
    for struct in can_struct['structure']:
        ids_vector.append(int(struct['can_id'], 16))

    # remove the IDs column from the matrix
    # mat = mat[:,1:]

    print("Parsing the data...", end='')
    # iterate the matrix rows
    curr_row = 0
    while curr_row < mat.shape[0]:

        # find the frame configuration to the ID of the matrix
        for frame_config in can_struct['structure']:
            if int(frame_config['can_id'], 16) == mat[curr_row][0]:
                # iterate the variables on the configuration to get the matrix values
                cur_byte_index = 1
                for v in range(len(frame_config['vars'])):
                    # calculate the ending byte of this variable
                    ending_byte = cur_byte_index + frame_config['vars'][v]['length']

                    # convert the byte array to the integer value
                    int_val = parseFromIntArray(mat[curr_row][cur_byte_index:ending_byte])
                    frame_config['vars'][v]['values'].append(int_val)

                    # the new starting byte index of the row is the last ending byte
                    cur_byte_index = ending_byte

        # change to the next matrix row
        curr_row += 1

    print("Done!")

    # print(can_struct)

    s_out = ""
    # print the frame IDs header
    for frame in can_struct['structure']:
        s_out += frame['can_id']
        for i in range(len(frame['vars'])):
            s_out += ";"
    s_out += "\n"

    # print the var names
    for frame in can_struct['structure']:
        for var in frame['vars']:
            s_out += var['name']
            s_out += ";"
    s_out += "\n"

    # print the data
    for row_num in range(int(mat.shape[0] / can_struct['n_ids_max'])):
        for frame in can_struct['structure']:
            for var in frame['vars']:
                if row_num <= len(var['values']) - 1:
                    s_out += str(var['values'][row_num])
                s_out += ";"
        s_out += "\n"

    # write the output csv to file
    f_out = open(os.path.join(sys.argv[2], file), "w")
    f_out.write(s_out)
    f_out.close()

# check for command line arguments
if len(sys.argv) < 3:
    print("Insufficient arguments provided!")
    print(f"Usage: python {sys.argv[0]} [in_dir] [out_dir]")
    sys.exit(-1)

# load configuration file
print("Reading CAN configuration...", end='')
f = open("can_config.json", "r")
can_struct = json.loads(f.read())
f.close()
# print(can_struct)
print("Done!")

# list the files in the directory
thread_list = list()
for file in os.listdir(sys.argv[1]):
    print(f"PROCESSING FILE {os.path.join(sys.argv[1], file)}...")

    # start a thread for each file
    t = threading.Thread(target=file_processing_routine, args=(os.path.join(sys.argv[1]),))
    t.start()
    thread_list.append(t)

    print(f"DONE PROCESSING {os.path.join(sys.argv[1], file)}!\n")

# wait for the threads to finish
for t in thread_list:
    t.join()