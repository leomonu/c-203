from gc import disable
import re
import socket
from threading import Thread
from tkinter import *

# nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))



class GUI:
    def __init__(self):
        self.window=Tk()
        self.window.withdraw()

        self.login=Toplevel()
        self.login.title("Login")
        
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=400)

        self.text=Label(self.login,text="Please Login To Continue",justify=CENTER,font="Helvetica 14 bold")
        self.text.place(relheight=0.15,relx=0.2,rely=0.07)

        self.labelName=Label(self.login,text="Name",font="Helvetica 14 bold")
        self.labelName.place(relheight=0.1,relx=0.1,rely=0.2)

        self.entrybox=Entry(self.login,font="Helvetica 14 bold")
        self.entrybox.place(relwidth=0.5,relheight=0.10,relx=0.35,rely=0.2)

        self.entrybox.focus()
        self.gobutton = Button(self.login,text="CONTINUE",font="Helvetica 14 bold",command=lambda:self.goAhead(self.entrybox.get()))
        self.gobutton.place(relx=0.4,rely=0.5)

        self.window.mainloop()

    def goAhead(self,name):
        self.login.destroy()
        self.chartLayout(name)
        rev=Thread(target=self.receive)
        rev.start() 

    def chartLayout(self,name):
        self.name=name
        self.window.deiconify()
        self.window.title("ChatRoom")
        self.window.resizable(width=False,height=False)

        self.window.configure(width=470,height=550,bg="black")
        self.labelHead = Label(self.window,text=self.name,bg="#17202A",fg="#EAECEE",font="Helvetica 14 bold",pady=5)
        self.labelHead.place(relwidth=1)

        self.line=Label(self.window,width=450,bg='#ABB2B9')
        self.line.place(relwidth=1,relheight=0.012,rely=0.07)
        
        self.textContent=Text(self.window,width=20,height=2,bg="#17202A",fg="#EAECEE",font="Helvetica 14 bold",pady=5,padx=5)
        self.textContent.place(relwidth=1,relheight=0.745,rely=0.08)

        self.labelBottom = Label(self.window,bg="#ABB2B9",height=80)
        self.labelBottom.place(relwidth=1,rely=0.825)

        self.enterMsg = Entry(self.window,bg="#2C3E50",fg="#EAECEE",font="Helvetica 14 bold")
        self.enterMsg.place(relwidth=0.74,relheight=0.07,rely=0.008,relx=0.0011)
        self.enterMsg.focus()

        self.send = Button(self.window,text="SEND",font="Helvetica 14 bold",bg="#ABB2B9",width=20,command=lambda:self.sendMsg(self.enterMsg.get()))
        self.send.place(relx=0.77,rely=0.008,relwidth=0.22,relheight=0.06)
        self.textContent.config(cursor="arrow")
        scrollbar=Scrollbar(self.textContent)
        scrollbar.place(relx=0.94,relheight=1)
        scrollbar.config(command=self.textContent.yview)
        

    def sendMsg(self,msg):
        self.textContent.config(state=DISABLED)
        self.msg=msg
        self.enterMsg.delete(0,END)
        s=Thread(target=self.write)
        s.start()

    def showMsg(self,msg):
        self.textContent.config(state=NORMAL)
        self.textContent.insert(END,msg+"\n\n")
        self.textContent.config(state=DISABLED)
        self.textContent.see(END)


    def write(self):

            self.textContent.config(state=DISABLED)
            while True:
                msg=(f"{self.name}:{self.msg}")
                client.send(msg.encode('utf-8'))
                self.showMsg(msg)
                break
           



    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMsg(message)
            except:
                print("An error occured!")
                client.close()
                break
    


g=GUI()

