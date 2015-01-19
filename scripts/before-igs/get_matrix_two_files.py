import sys


filein = open(sys.argv[1],'r')
fileout = open(sys.argv[2],'w')

set_x = set()
set_y = set()


matrix = {}
for line in filein:
    line = line.rstrip()
    fields = line.split()
    key = fields[1]+'-'+fields[2]
    matrix[key] = matrix.get(key,0) + 1
    set_x.add(int(fields[1]))
    set_y.add(int(fields[2]))

#print set_x
#print set_y
set_x = list(set_x)
set_y = list(set_y)

set_x.sort()
set_y.sort()
#print set_x
#print set_y    
for x in set_x:
    for y in set_y:
        if str(x)+'-'+str(y) in matrix:
            to_print = str(x)+'-'+str(y)+' '+ str(matrix[str(x)+'-'+str(y)]) +'\n'
            fileout.write(to_print)
        
fileout.close()
