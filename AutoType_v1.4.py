# python code for auto typing
import pyautogui
import time
from tkinter import *

def setSize(event):
    wid=root.winfo_width()
    hig=root.winfo_height()
    iw=700
    ih=830
    newWid=int(53*((wid/iw))) 
    newHig=float(12*((hig/ih)))
    newHig="{0:0.1f}".format(newHig)
    
    # current_height = e.cget('height')
    
    # print("hig :",newHig," wid : ",newWid," Entry height: ",current_height)
    
    e.config (width=newWid)
    e.config (height=newHig)
    start_typing.config(width=newWid)
    

root=Tk()  
root.geometry("700x830+155+60") 
root.title("Auto Type")  
root.minsize(700,830)
root.config(bg="#ffffff")
start_after=Label(root,text="Enter text you want to AutoType",
                  font=("Open sans", 18,),
                    bg="#FFFFFF")
start_after.pack(side=TOP ,pady=12)

e = Text(root, width=53,height=12, bg="#e0e0e0", font=("Open Sans", 14))
e.pack(pady=10)

dell=Label(root,text="Start autotyping after(sec)",font=("Open Sans", 14),bg="#ffffff").pack()


s =Entry(root,width=10,bg="#e0e0e0", font=("Open Sans", 14))
s.pack(pady=10)
s.insert(0,5)

spd=Label(root,text="Set typing speed (1-10)",font=("Open Sans", 14),bg="#ffffff").pack()


x=Scale(root, from_=1,to=10,orient="horizontal",length=300,bg="#ffffff",width=20,sliderlength=50, troughcolor='#aed5f2')
x.set(10)
x.pack(pady=10)

# s is sleep
# x is speed

def typei(s,x):
      
    if s=="":
        s=5 
    time.sleep(int(s))

    text=e.get(1.0,END)
    xx=((11-float(x))/100)
    
    pyautogui.typewrite(text, interval = xx)

def shift_line_to_left(s):
    arr=s.splitlines()
    ans=""
    for i in arr:
        ans=ans+i.strip()+"\n"
    e.delete(1.0, END)
    e.insert(1.0, ans)

def pointerInside(e):
    e.widget['background']="#d4d7d9"
def pointerOutside(e):
    e.widget['background']="#F0F0F0"


leftShift= Button(root,text="Remove indentation",activebackground="#F0F0F0",font=("Open Sans", 14,),bg="#F0F0F0",border=0,command=lambda:shift_line_to_left(e.get(1.0,END)))
leftShift.pack(side=TOP,pady=10)
leftShift.bind("<Enter>",pointerInside)
leftShift.bind("<Leave>",pointerOutside)

start_typing=Button(root,text="Start AutoTyping",activebackground="#F0F0F0",width=53,font=("Arial", 16,"bold"),
                    border=0,bg="#F0F0F0",command=lambda:typei(s.get(),x.get()))

start_typing.pack(side=TOP,padx=10,pady=10)
start_typing.bind("<Enter>",pointerInside)
start_typing.bind("<Leave>",pointerOutside)
root.bind("<Configure>",setSize)
root.mainloop()