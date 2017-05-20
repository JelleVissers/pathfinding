from path import set
from path import open
from path import A_algorithm
from Tkinter import *
import tkMessageBox
from path.simulate import A,dijkstra_,simple

root = Tk()
sim_view = []           # global name for simulatie window
functielistbox = Listbox(root,width = 30,height = 18)
multiplier = 0
preview = Canvas(root,bg="white", height=146, width=282)
omgevings_matrix= []    # matrix met data van de momgeving
startpoint = []         # coordinaten van het beginpunt
endpoint   = []         # coordinaten van het eindpunt

def open_omgeving():
    global omgevings_matrix
    global startpoint
    global endpoint

    matrixfile = open.import_file()
    omgevings_matrix = open.get_matrix(matrixfile)
    startpoint = open.get_startpoint(matrixfile)
    endpoint   = open.get_endpoint(matrixfile)
    preview_cavas()

def view_envirement():
    global omgevings_matrix
    global startpoint
    global endpoint

    open.view_envirement(omgevings_matrix,startpoint,endpoint)

def menubalk():
    global root
    global omgevings_matrix
    '''
    Initaliseer menubalk in het programma
    '''
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=set.make_enviroment)
    filemenu.add_command(label="Open", command=open_omgeving)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    viewmenu = Menu(menubar, tearoff=0)
    viewmenu.add_command(label="View environment",command=view_envirement)
    menubar.add_cascade(label="View", menu=viewmenu)

    helpmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)

def run():
    global omgevings_matrix
    global startpoint
    global endpoint
    global functielistbox

    if len(omgevings_matrix) is not 0:
        functie = functielistbox.curselection()

        if len(functie) == 0:
            tkMessageBox.showerror("error","Select search method ")
        elif functie[0] == 0:
            A.simulate(omgevings_matrix,startpoint,endpoint)              # zet simulatie omgeving op
        elif functie[0] == 1:
            dijkstra_.simulate(omgevings_matrix, startpoint, endpoint)
        elif functie[0] == 2:
            simple.simulate(omgevings_matrix, startpoint, endpoint)


    else:
        tkMessageBox.showerror("error","No environment imported")

def preview_cavas():
    global root
    global startpoint
    global endpoint
    global omgevings_matrix
    global preview


    resize_widt  = 280/len(omgevings_matrix[0])
    resize_height = 144/len(omgevings_matrix)
    if resize_height < resize_widt:
        factor = resize_height
    else:
        factor = resize_widt

    addfactor = (280-len(omgevings_matrix[0])*factor)/2
    yaddfactor = (144-len(omgevings_matrix*factor))/2

    preview.create_rectangle(5,5,280,144,fill="white",outline="gray",width=1)
    preview.create_rectangle(addfactor, 5, addfactor+len(omgevings_matrix[0])*factor, 144, fill="white",width=1)

    yteller = 0

    for y in omgevings_matrix:
        xteller = 0
        for x in y:
            if x == 1:
                preview.create_rectangle(addfactor+xteller*factor-factor/2,yaddfactor+yteller*factor-factor/2,addfactor+xteller*factor+factor/2,yaddfactor+yteller*factor+factor/2,fill ='black',width=1)
            xteller = xteller +1
        yteller = yteller +1

    preview.create_oval(addfactor+startpoint[0] *factor-factor, yaddfactor+startpoint[1] *factor-factor, addfactor+startpoint[0] *factor+factor,yaddfactor+startpoint[1] *factor+factor, fill="green", width=0)
    preview.create_oval(addfactor+endpoint[0] *factor-factor, yaddfactor+endpoint[1] * factor-factor, addfactor+endpoint[0] *factor+factor,yaddfactor+endpoint[1] *factor+factor, fill="red", width=0)

def main():
    global root
    global preview
    global functielistbox

    root.geometry("300x600")
    root.title("Find path")
    root.resizable(False, False)

    menubalk()

    preview.create_rectangle(5, 5, 280, 144, fill="white", width=1)
    preview.place(x=3, y=40)

    # ---- add labels          --------
    envirement_label= Label(root,text="Preview environment",font=('Verdana bold',16))
    envirement_label.place(x=10,y=15)

    methode_label= Label(root,text="Search methods",font=('Verdana bold',16))
    methode_label.place(x=10,y=220)


    # ---- add functie listbox --------
    functielistbox.insert(1, "A* algorithm")
    functielistbox.insert(2, "Dijkstra's algorithm")
    functielistbox.insert(3, "Simple search")
    functielistbox.place(x=10,y=250)

    # ---- add run button      --------
    run_button = Button(root,text='Run',command=run,width=28)
    run_button.place(x=7,y=560)

    root.mainloop()


if __name__ == '__main__':
    main()