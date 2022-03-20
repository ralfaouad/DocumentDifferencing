from cProfile import label
from cgitb import grey, text

from fileinput import filename
from tkinter import *
from tkinter import filedialog
from webbrowser import open_new_tab
from xml.etree.ElementTree import XML


from pyotp import Any

root=Tk()
root.title("XML Differencing tool")
root.iconbitmap('hnet.com-image.ico')
root['bg']='#ffffff'



width= root.winfo_screenwidth() 
height= root.winfo_screenheight()

#setting tkinter window size
root.geometry("%dx%d" % (width, height))

dotted_label=Label(root,text="-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
dotted_label.pack(pady=250)



def browse1():
     root.filename= filedialog.askopenfile(initialdir='/Sample XML Docs',title ="Select a file")
     label=Label(root,text=root.filename)
     label.place(x=850,y=100)

def browse2():
     root.filename= filedialog.askopenfile(initialdir='/Sample XML Docs',title ="Select a file")
     label=Label(root,text=root.filename)
     label.place(x=850,y=200)

   

def get_ES():
    label=Label("")

def get_similarity():
    label=Label("")

def get_Patched():
    open_new_tab("patched.xml")


def get_Reverse_Patched():
    open_new_tab("Reverse_Patched.xml")


def compute():
    label=""


b1=Button(root,text="DOC A",bg= "#4db6ac",fg="#ffffff",height=3,width=60,font=('Times',13,'bold'))
b1.place(x=100,y=70)


b2=Button(root,text="DOC B",bg="#4db6ac",fg="#ffffff",height=3,width=60,font=('Times',13,'bold'))
b2.place(x=100,y=170)

b3=Button(root,text="ES IS:              ",bg="#0b4a44",fg="#ffffff",height=6,width=60,command=get_ES,font=('Times',13,'bold'))
b3.place(x=900,y=350)

b4=Button(root,text="SIMILARITY  IS :                   ",bg="#0b4a44",fg="#ffffff",height=6,width=60,command=get_similarity,font=('Times',13,'bold'))
b4.place(x=200,y=350)

b5=Button(root,text="GET PATCHED FILE",bg="#16645c",fg="#ffffff",height=6,width=120,command=get_Patched,font=('Times',13,'bold'))
b5.place(x=250,y=500)

b6=Button(root,text="GET REVERSE PATCHED",bg="#16645c",fg="#ffffff",height=6,width=120,command=get_Reverse_Patched,font=('Times',13,'bold'))
b6.place(x=250,y=650)

browse1=Button(root,text="Browse XML File",command=browse1)
browse1.place(x=720,y=70,height=70,width=100)

browse2=Button(root,text="Browse XML File",command=browse2)
browse2.place(x=720,y=180,height=60,width=100)

compute=Button(root,text="Compute",command=compute)
compute.place(x=1540,y=270)



root.mainloop()