# python code for auto typing
import pyautogui
import time
from tkinter import *

root=Tk()  
root.geometry("1200x800+155+60") 
root.title("Auto Type")  
root.resizable(height=FALSE, width=FALSE)
root.config(bg="#ffffff")
start_after=Label(root,text="Enter text you want to AutoType",
                  font=("Open sans", 18,),
                    bg="#FFFFFF")
start_after.pack(side=TOP ,pady=15)

e = Text(root, width=85,height=12, bg="#e0e0e0", font=("Open Sans", 14))
e.pack(pady=10)

dell=Label(root,text="Start autotyping after(sec)",font=("Open Sans", 14),bg="#ffffff").pack()


s =Entry(root,width=10,bg="#e0e0e0", font=("Open Sans", 14))
s.pack(pady=10)
s.insert(0,5)

spd=Label(root,text="Set typing speed (1-10)",font=("Open Sans", 14),bg="#ffffff").pack()

x =Entry(root,width=10,bg="#e0e0e0", font=("Open Sans", 14))
x.pack(pady=10)
x.insert(1,10)

def typei(s,x):
      
    if s=="":
        s=5 
    time.sleep(int(s))

    text=e.get(1.0,END)
    if x=="":
        x=5
        
    xx=((11-float(x))/50)
    
    pyautogui.typewrite(text, interval = xx)

start_typing=Button(root,text="Start AutoTyping",width=50,font=("Arial", 16,"bold"),
                    border=0,bg="#F0F0F0",command=lambda:typei(s.get(),x.get()))

start_typing.pack(side=TOP,padx=10,pady=10)

root.mainloop()