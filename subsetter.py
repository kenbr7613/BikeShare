 #This file reads in a set of training data and divides it into x
#subsets with the name file01, file02 etc.

import sys
import random
import math
import os


if len(sys.argv) == 1:
    print "Which file?"
    fpath =raw_input("> ")
    num_sets = 8
elif len(sys.argv) == 2:
    fpath = sys.argv[1]
    num_sets = 8
else:
    fpath = sys.argv[1]
    num_sets = int(sys.argv[2])

f = open(fpath)
data = f.readlines()
f.close()
header = data[0]
data.remove(header)

filename = os.path.splitext(fpath)[0]
ext = os.path.splitext(fpath)[1]

random.shuffle(data)

ss_size = int(math.floor(len(data) / num_sets))
for ss in range(0, num_sets-1):
    sub_file = open(filename + str(ss).zfill(3) + ext, 'w')
    sub_file.write(header)
    for i in range(ss * ss_size, (ss+1) * ss_size):
        sub_file.write(data[i])
    sub_file.close()

sub_file = open(filename + str(num_sets-1).zfill(3) + ext, 'w')
sub_file.write(header)
for i in range((num_sets-1) * ss_size, len(data)):
    sub_file.write(data[i])
sub_file.close()

    
    
