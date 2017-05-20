from path import set
import tkFileDialog
from datetime import datetime

filename = tkFileDialog.asksaveasfilename()

print str(filename)+'\n'

matrix = set.creat_matrix(100,100)
filedata = ['jelle vissers','testmatrix',100,100]

# bestand openen voor schrijven
matrix_file = open(filename,'w')

matrix_file.write("Created by  : "+ filedata[0]+str('\n'))
matrix_file.write("Discription : "+ filedata[1]+str('\n'))
matrix_file.write("Maked on    : "+ str(datetime.now())+str('\n'))
matrix_file.write("Version     : "+ "0.1 \n")
matrix_file.write("Width       : "+ str(filedata[2])+str('\n'))
matrix_file.write("Height      : "+ str(filedata[3])+str('\n'))
matrix_file.write("\n\n")

for y in matrix:
    for x in y:
        matrix_file.write(str(x)+",")
    matrix_file.write("\n")

matrix_file.close()