from Tkinter import *
import tkFileDialog
import tkMessageBox
from datetime import datetime


filedata = ['','',0,0]
mouseinfo =[0,0,False]
enviroment = []
matrix = []
start_coordinaten=[0,0]
end_coordinaten=[0,0]
#     ------  button functies  -----------
def save():
    global matrix
    global filedata
    global start_coordinaten
    global end_coordinaten

    filename = tkFileDialog.asksaveasfilename()

    # bestand openen voor schrijven
    matrix_file = open(filename, 'w')

    matrix_file.write("Created by  : " + filedata[0] + str('\n'))
    matrix_file.write("Discription : " + filedata[1] + str('\n'))
    matrix_file.write("Maked on    : " + str(datetime.now()) + str('\n'))
    matrix_file.write("Version     : " + "0.1 \n")
    matrix_file.write("Width       : " + str(filedata[2]) + str('\n'))
    matrix_file.write("Height      : " + str(filedata[3]) + str('\n'))
    matrix_file.write("\n\n")
    matrix_file.write("start : "+str(start_coordinaten[0])+','+str(start_coordinaten[1])+"\n")
    matrix_file.write("end   : "+str(end_coordinaten[0])+','+str(end_coordinaten[1])+"\n")
    matrix_file.write("\n\n")

    for y in matrix:
        for x in y:
            matrix_file.write(str(x) + ",")
        matrix_file.write("\n")

    matrix_file.close()

def creat_matrix(width,height):
    x = []
    for width_teller in range(0,width,1):
        x = x +[0]
    matrix = []
    for height_teller in range(0,height,1):
        matrix = matrix + [x]

    return matrix

def matrix_replace(matrix,x_coordinaten,y_coordinaten):
    '''
    verander waarde 0 naar 1 op gegeven positie in matrix
    '''
    yteller = 0
    test_matrix = []
    for y in matrix:
        xteller = 0
        x_line = []
        for x in y:
            if xteller == x_coordinaten and yteller == y_coordinaten:
                x_line = x_line + [1]
            else:
                x_line = x_line + [matrix[yteller][xteller]]
            xteller = xteller + 1
        yteller = yteller + 1

        test_matrix = test_matrix + [x_line]
    return test_matrix

def matrix_replace_zero(matrix,x_coordinaten,y_coordinaten):
    '''
        verander waarde 1 naar 0 op gegeven positie in matrix
        '''
    yteller = 0
    test_matrix = []
    for y in matrix:
        xteller = 0
        x_line = []
        for x in y:
            if xteller == x_coordinaten and yteller == y_coordinaten:
                x_line = x_line + [0]
            else:
                x_line = x_line + [matrix[yteller][xteller]]
            xteller = xteller + 1
        yteller = yteller + 1

        test_matrix = test_matrix + [x_line]
    return test_matrix

def new_environment_info():
    '''
    scherm voor het invoeren van document gegevens
    bij het openen van een nieuw program
    '''
    def get_data():
        '''
        haal data uit enty en sluit scherm
        '''
        global filedata

        raw_data = [name.get()]
        raw_data = raw_data+[discription.get()]
        raw_data = raw_data+[width.get()]
        raw_data = raw_data+[Height.get()]

        print raw_data

        try:
            filedata[0] = str(raw_data[0])
            filedata[1] = str(raw_data[2])
            raw_width   = int(raw_data[2])
            raw_height  = int(raw_data[3])

            if raw_height < 151 and raw_width < 251:
                filedata[2] = raw_width
                filedata[3] = raw_height
                info_screen.quit()
                info_screen.destroy()

            else:
                tkMessageBox.showerror("Not possible",message="maximum size limit has been exceeded \n Maximum Width 250 \n Maximum height 150")
        except:
            tkMessageBox.showerror("Not possible",message="Give a number for the width and height")



    info_screen = Toplevel()
    info_screen.title("Set project data")
    #L_title = Label(info_screen, text="project data" )
    #L_title.config(font=("Bolt", 20))
    #L_title.grid(row=0,column=1)
    L_name = Label(info_screen, text="User Name")
    L_name.grid(row=1, column=0)
    L_discription = Label(info_screen, text="Discription")
    L_discription.grid(row=2, column=0)
    L_width= Label(info_screen, text="Environment width")
    L_width.grid(row=3, column=0)
    L_height = Label(info_screen, text="Environment height")
    L_height.grid(row=4, column=0)

    name = Entry(info_screen,bd=5)
    name.grid(row=1,column=1)
    discription = Entry(info_screen, bd=5)
    discription.grid(row=2, column=1)
    width = Entry(info_screen,bd=5)
    width.grid(row=3,column=1)
    Height = Entry(info_screen, bd=5)
    Height.grid(row=4, column=1)

    Load = Button(info_screen,text="Generate",command=get_data)
    Load.grid(row=5,column=1)
    info_screen.resizable(False, False)

    info_screen.mainloop()

def printmatrix(matrix):
    for lines in matrix:
        print lines

def mousePressed(event):
    global mouseinfo
    mouseinfo = [event.x,event.y,True]

def mouseRightPressed(event):
    global mouseinfo
    global mouseinfo
    mouseinfo = [event.x, event.y, False]

def update_enviroment():
    global enviroment
    global matrix
    global oldmatrix
    global start_coordinaten
    global end_coordinaten
    yteller = 0

    for y in matrix:
        xteller = 0
        for x in y:
            if x == 1:
                enviroment.create_rectangle(xteller*6-3,yteller*6-3,xteller*6+3,yteller*6+3,fill ='black',width=0)
            elif x == 0:
                enviroment.create_rectangle(xteller*6-3,yteller*6-3,xteller*6+3,yteller*6+3,fill ='white',width=0)
            xteller = xteller +1
        yteller = yteller +1
    print start_coordinaten[0],start_coordinaten[1]
    enviroment.create_oval(start_coordinaten[0] * 6 - 4, start_coordinaten[1] * 6 - 4,start_coordinaten[0] * 6 + 4, start_coordinaten[1] * 6 + 4, fill="green", width=1)
    enviroment.create_oval(end_coordinaten[0] * 6 - 4, end_coordinaten[1] * 6 - 4, end_coordinaten[0] * 6 + 4,end_coordinaten[1] * 6 + 4, fill="red", width=1)

def mouseRelease(event):
    global mouseinfo
    global matrix
    # program for mousepressed
    coordinaten = [[mouseinfo[0],event.x],[mouseinfo[1],event.y]]
    x_min = min([mouseinfo[0],event.x])
    x_max = max([mouseinfo[0],event.x])
    y_min = min([mouseinfo[1], event.y])
    y_max = max([mouseinfo[1], event.y])

    # stel maximale waarden en minmale waarden binnen range van envirement
    if x_min < 0: x_min = 0
    if x_max > filedata[2] * 6: x_max = filedata[2] * 6
    if y_min < 0: y_min = 0
    if y_max > filedata[3] * 6: y_max = filedata[3] * 6

    # reken coordinaten om naar vaken
    x_max = int(x_max/6)
    x_min = int(x_min/6)
    y_max = int(y_max/6)
    y_min = int(y_min/6)

    if mouseinfo[2]:
       for x in range(x_min,x_max,1):
           for y in range(y_min,y_max,1):
               matrix = matrix_replace(matrix,x,y)

    if mouseinfo[2] == False:
       for x in range(x_min,x_max,1):
           for y in range(y_min,y_max,1):
               matrix = matrix_replace_zero(matrix,x,y)
    update_enviroment()

def set_StartEnd(event):
    x_coordinaten = event.x/6
    y_coordinaten = event.y/6

    def start():
        global start_coordinaten
        start_coordinaten = [x_coordinaten,y_coordinaten]
        askwindow.quit()
        askwindow.destroy()
        update_enviroment()
    def stop():
        global end_coordinaten
        end_coordinaten = [x_coordinaten,y_coordinaten]
        askwindow.quit()
        askwindow.destroy()
        update_enviroment()

    askwindow = Toplevel()
    askwindow.resizable(False, False)
    start_button = Button(askwindow,text= "create startpoint",command=start)
    stop_button  = Button(askwindow,text= "create Endpoint", command = stop)
    start_button.grid(row=0,column=0)
    stop_button.grid(row=1,column=0)

    askwindow.mainloop()

def make_enviroment():
    global mouseinfo
    global matrix
    global enviroment
    new_environment_info()
    matrix = creat_matrix(filedata[2],filedata[3])
    screen = Toplevel()                          # open window
    screen.title("Make envirement")
    screen.geometry(str(filedata[2]*6)+"x"+str(filedata[3]*6))
    screen.resizable(width=False,height=False)
    enviroment = Canvas(screen,bg="white",height=filedata[3]*6,width=filedata[2]*6)

    #for line_width in range(0,filedata[2],1):
    #    line = enviroment.create_line(line_width*6,0,line_width*6,filedata[3]*6,fill='gray')

    #for line_height in range(0,filedata[3],1):
    #    line = enviroment.create_line(0,line_height*6,filedata[2]*6,line_height*6,fill='gray')

    enviroment.pack()

    # ------ set muisfunctie in everment -------------
    enviroment.bind("<Button-1>",mousePressed)
    enviroment.bind("<Button-2>",mouseRightPressed)
    enviroment.bind("<ButtonRelease>", mouseRelease)
    enviroment.bind("<Double-Button-1>", set_StartEnd)

    menubar = Menu(screen)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Save", command=save)
    menubar.add_cascade(label="File", menu=filemenu)

    screen.config(menu=menubar)

    screen.mainloop()
