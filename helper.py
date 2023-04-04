# Author/s: Yee Chuen Teoh                                  (Author that contribute to the script)
# Title: helper.py                                          (the name of the script)
# Project: OTHELLO-RL                                       (the main project name, what project this script is apart of?)
# Description: helper methods/functions for 673 RL project  (summary of what the script does)
# Reference/Directions:
'''
Usage:
    python helper.py
'''
# Updates:  (4/4/2023)
'''
4/4/2023
    - import numpy
    - addition of two helper functions pos_to_index and index_to_pos
    - creation of the script
'''

#____________________________________________________________________________________________________
# imports 
import numpy as np

#____________________________________________________________________________________________________
# functions/set ups

def pos_to_index(i,j):
    '''
    input: 
        @param i,j --> 2dim coordinate in the board

    output:
        @return n --> the location of (i,j) in the 1dim vertex
    '''
    if i > 7 or i < 0 or j > 7 or j < 0:
        print("invalid coordiate for function pos_to_index")
        return -1
    else:
        return 8*i+j
    
def index_to_pos(n):
    '''
    input: 
        @param n --> 1dim location in vertex of some coordinate

    output:
        @return (i,j) --> list of size 2 with index 0 = value for i, index 1 = value for j
    '''
    if n < 0 or n > 63:
        print("invalid coordiate for function index_to_pos")
        return -1
    else:
        j=n%8
        i=int((n-j)/8)
        return (i,j)
     
def main():    
    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    # TODO: change your python script title
    print("\n-------------------- START of \"<helper.py>\" script --------------------")
    main()           
    print("-------------------- END of \"<helper.py>\" script --------------------\n")