from cProfile import label
from cgitb import text
from fileinput import filename
from tkinter import *
from tkinter import filedialog
from webbrowser import open_new_tab
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
     root.filename= filedialog.askopenfile(initialdir='C:/Users/Lenovo/Desktop/Sample XML Docs',title ="Select a file")
     label=Label(root,text=root.filename)
     label.place(x=600,y=120)
    
   
def upload2Click():
     root.filename= filedialog.askopenfile(initialdir='C:/Users/Lenovo/Desktop/Sample XML Docs',title ="Select a file")
     label=Label(root,text=root.filename)
     label.place(x=600,y=220)
   

def get_ES():
    label=Label("")

def get_similarity():
    label=Label("")

def get_Patched():
    open_new_tab("patched.xml")


def get_Reverse_Patched():
    open_new_tab("Reverse_Patched.xml")



b1=Button(root,text="DOC A",bg= "#676D6A",fg="black",height=3,width=60,command=upload1Click,font=('Times',10))
b1.place(x=100,y=100)


b2=Button(root,text="DOC B",bg="#676D6A",fg="black",height=3,width=60,command=upload2Click,font=('Times',10))
b2.place(x=100,y=200)

b3=Button(root,text="ES IS:           ",bg="#676D6A",fg="black",height=6,width=60,command=get_ES,font=('Times',10))
b3.place(x=900,y=300)

b4=Button(root,text="SIMILARITY  IS :                 ",bg="#676D6A",fg="black",height=6,width=60,command=get_similarity,font=('Times',10))
b4.place(x=200,y=300)

b5=Button(root,text="GET PATCHED FILE",bg="#676D6A",fg="black",height=6,width=120,command=get_Patched,font=('Times',10))
b5.place(x=350,y=500)

b6=Button(root,text="GET REVERSE PATCHED",bg="#676D6A",fg="black",height=6,width=120,command=get_Reverse_Patched,font=('Times',10))
b6.place(x=350,y=700)




root.mainloop()