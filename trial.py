from cProfile import label
from cgitb import text
from fileinput import filename
from tkinter import *
from tkinter import filedialog
from xml.etree.ElementTree import XML




root=Tk()
root.title("XML Differencing tool")
root.iconbitmap('hnet.com-image.ico')
root['bg']='#303633'


width= root.winfo_screenwidth() 
height= root.winfo_screenheight()

#setting tkinter window size
root.geometry("%dx%d" % (width, height))

def upload1Click():
     root.filename= filedialog.askopenfile(initialdir='/',title ="Select a file")
    
   
def upload2Click():
     root.filename= filedialog.askopenfile(initialdir='/',title ="Select a file")

def get_ES():
    label=Label("")

def get_TED():
    label=Label("")

def get_Patched():
    label=Label("")



b1=Button(root,text="UPLOAD FILE 1",bg= "#676D6A",fg="black",height=6,width=120,command=upload1Click,font=('Times',10))
b1.place(x=350,y=100)


b2=Button(root,text="UPLOAD FILE 2",bg="#676D6A",fg="black",height=6,width=120,command=upload2Click,font=('Times',10))
b2.place(x=350,y=225)

b3=Button(root,text="GET  EDIT SCRIPT",bg="#676D6A",fg="black",height=6,width=120,command=get_ES,font=('Times',10))
b3.place(x=350,y=350)

b4=Button(root,text="GET TED",bg="#676D6A",fg="black",height=6,width=120,command=get_TED,font=('Times',10))
b4.place(x=350,y=475)

b5=Button(root,text="GET PATCHED FILE",bg="#676D6A",fg="black",height=6,width=120,command=get_Patched,font=('Times',10))
b5.place(x=350,y=600)



root.mainloop()