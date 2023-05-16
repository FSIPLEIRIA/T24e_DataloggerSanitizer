import sys
import numpy as np

if len(sys.argv) == 1:
    print("Insufficient arguments provided!")
    print(f"Usage: python {sys.argv[0]} [filename.csv]")
    sys.exit(-1)

# load filename to numpy matrix
mat = np.loadtxt(sys.argv[1], delimiter=';')
print(mat)
