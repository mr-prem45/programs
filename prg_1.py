from tkinter import *;
tk = Tk()
tk.title("My First Application");
tk.geometry("400x200");

label1=Label(tk,text="Name:")
label1.grid(row=0,column=1)
p=Entry(tk).grid(row=0,column=2)       

label2=Label(tk,text="Age:")
label2.grid(row=2,column=1)
p=Entry(tk).grid(row=2,column=2)  

label3=Label(tk,text="Mobile No. :")
label3.grid(row=4,column=1)
p=Entry(tk).grid(row=4,column=2)  

submit = Button(tk,text="Submit",background="green").grid(row=7,column=2)
#Create First Frame
f_a = Frame(tk)
f_a.grid(pady=10)

l_a = Label(f_a,text = "Krish")
l_a.grid(row=11,column=1)
#create second frame 
f_b = Frame(tk)
f_b.grid(pady=10)

l_a = Label(f_a,text = "Kush")
l_a.grid(row=13,column=1)

tk.mainloop();
