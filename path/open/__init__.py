import tkFileDialog
from Tkinter import *

def import_file():
    '''
    open omgevings file
    '''
    filename = tkFileDialog.askopenfilename()
    File = open(filename,"r")
    return File.read()

def get_matrix(File):
    '''
    Haal matrix uit file voor omgeving
    '''
    File = File.splitlines()
    File = File[12:len(File)]
    new_matrix = []

    for lines in File:
        lines = lines.split(",")
        lines = lines[0:len(lines)-1]
        int_line = []
        for point in lines:
            int_line = int_line + [int(point)]
        new_matrix = new_matrix + [int_line]
    return new_matrix

def get_startpoint(File):
    '''
    :param File: File of matrix(envirment)
    gets startpoint
    :return: startpoint [x,y]
    '''

    File = File.splitlines()
    points= File[8].split(":")
    points[1] = points[1].replace(" ","")
    str_coordinaten = points[1].split(",")
    coordinaten = [int(str_coordinaten[0]),int(str_coordinaten[1])]
    return coordinaten

def get_endpoint(File):
    '''
    :param File: File of matrix(envirment)
    gets endpoint
    :return: endpoint [x,y]
    '''
    File = File.splitlines()
    points = File[9].split(":")
    points[1] = points[1].replace(" ", "")
    str_coordinaten = points[1].split(",")
    coordinaten = [int(str_coordinaten[0]), int(str_coordinaten[1])]
    return coordinaten

def view_envirement(matrix,startpoint,endpoint):
    envirement_gui = Toplevel()
    envirement_gui.geometry(str(len(matrix[1])*4)+'x'+str(len(matrix)*4))

    enviroment = Canvas(envirement_gui, bg="white", height=len(matrix)*4, width=len(matrix[1])*4)
    enviroment.pack()

    yteller = 0
    for y in matrix:
        xteller = 0
        for x in y:
            if x == 1:
                enviroment.create_rectangle(xteller*4-2,yteller*4-2,xteller*4+2,yteller*4+2,fill ='black',width=0)
            elif x == 0:
                enviroment.create_rectangle(xteller*4-2,yteller*4-2,xteller*4+2,yteller*4+2,fill ='white',width=0)
            xteller = xteller +1
        yteller = yteller +1

    enviroment.create_oval(startpoint[0] * 4 - 2, startpoint[1] * 4 - 2, startpoint[0] * 4 + 2,startpoint[1] * 4 + 2, fill="green", width=1)
    enviroment.create_oval(endpoint[0] * 4 - 2, endpoint[1] * 4 - 2, endpoint[0] * 4 + 2,endpoint[1] * 4 + 2, fill="red", width=1)

    envirement_gui.mainloop()




