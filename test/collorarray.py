from Tkinter import *

gui = Tk()
gui.geometry("1200x150")
canvas = Canvas(gui,width=1200,height=150,bg='white')
canvas.place(x=0,y=0)

for x in range(0,1000,1):
    if x < 500:
        color = '#%02x%02x%02x' % (0,x*255/500, 255-x*255/500)
    else:
        color = '#%02x%02x%02x' % ((x-500)*255/500, 255-(x-500)*255/500,0)

    canvas.create_line(x,0,x,150,fill=color)

gui.mainloop()