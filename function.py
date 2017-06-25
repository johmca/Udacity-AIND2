#print('Starting suduko.py....')

#get the display function from utils.py file provided. this shows a graphical
#representation of the grid
from utils import display

#Define strings for rows and columns
rows='ABCDEFGHI'
cols='123456789'
grid_state='..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'


#----------------------------------------------------
# cross
#----------------------------------------------------
# Inputs  string1
#         string2
# Outputs list
#
# This function receives two strings and combines each
# character of string 1 with each character of string 2 to
# form a list which is returned. For example:
# cross('abc' 'xyz') returns ('ax','ay,'az','bx','by','bz','cx','cy,'cz')
#------------------------------------------------------
def cross (a, b):
    return [s+t for s in a for t in b]

#----------------------------------------------------
# grid_values
#----------------------------------------------------
# Inputs  string                 String holding grid contents
#         list                   List of grid positions
# Outputs dictionary             Dictionary with pairs of
#                                grid position : grid content
#
# This function receives two strings and combines each
# character of strign 1 with each character of string 2 to
# form a new string3 which is returned. For example:
# cross('abc' 'xyz') returns ('ax','ay,'az','bx','by','bz','cx','cy,'cz')
#------------------------------------------------------
def grid_values (a,b):
    grid = dict(zip(a,b))
    return grid


#Call cross() to cross multiply rows and columns to get list of all boxes
boxes = cross(rows,cols)

#Call cross() to create list of row units (all boxes in each row of grid)
row_units = [cross(r, cols) for r in rows]

#Call cross()to create list of col units (all boxes in each col of grid)
col_units = [cross(rows, c) for c in cols]

#Call cross() to create list of square units (all boxes in each sub-square of grid)
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#Call grid_values() to build dictonary object containing each element of the grid with its content
grid_dict=grid_values(boxes,grid_state)

# Debug
#print ('Rows are '+rows)
#print ('Cols are '+cols)
#print('Boxes are',','.join(boxes))
#print('Row units are',','.join(row_units[0]))
#print('Col units are',','.join(col_units[0]))
#print('Square units are',','.join(square_units[0]))
display(grid_dict)
#print("Grid is",grid_dict['A5'])
