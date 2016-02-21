from Tkinter import *
import tkFont
import glob
import os

complete = 0 #control persistance of interface

class UserList:
    def __init__(self,myParent,idx):
        self.myParent = myParent
        self.Con1 = Frame(myParent)
        self.Con1.pack()

        self.labelFont = tkFont.Font(family="Helvetica",size=12)

        self.first = Label(self.Con1,text="Provide usernames separated by a space:",
 font=self.labelFont)
        self.first.pack()

        infile = open('.devices','r')
        inline = infile.readline()
        self.start = '' #First devices
        self.line = '' #Device we're editing
        self.finish = '' #Last devices
        internal = 0

        while internal < idx:
            self.start = self.start + inline 
            inline = infile.readline()
            internal = internal+1

        self.line = inline        
        inline = infile.readline()

        while inline != '':
            self.finish = self.finish + inline
            inline = infile.readline()
        infile.close()

        #display current users
        split = self.line.split()
        self.front = ''
        for i in range(3):
            self.front = self.front + split.pop(0) +'  '#name, type, flocation

        cusers = '' #users
        while len(split) != 0:
            cusers = cusers + split.pop(0)+'  '

        self.text = Text(self.Con1,height=2,width=60,padx=5)
        self.text.insert(INSERT, cusers)
        self.text.pack()
        self.text.focus()

        self.button = Button(self.Con1, command=self.done,text="Done")
        self.button.pack()

    def done(self):

        devfile = open('.devices','w')
        users = self.text.get(1.0,END) #get current list of users
        newfile = self.start + self.front + users[0:-1] + self.finish
        devfile.write(newfile)

        self.myParent.destroy()

class Editor:
    def __init__(self,myParent,bigInterface):
        self.bigInterface=bigInterface
        self.myParent=myParent
        self.Con1 = Frame(myParent)
        self.Con1.pack()

        self.labelFont = tkFont.Font(family="Helvetica",size=12)

        self.first = Label(self.Con1,text="Storage Device Name:", font=self.labelFont)
        self.first.pack()

        self.dtext = "/data"
        self.location = Entry(self.Con1)
        self.location.insert(0, self.dtext)
        self.location.pack()
        self.location.focus()

        #Have text dissappear on click
        self.location.bind("<ButtonRelease-1>", self.default(self.dtext,self.location))
        self.location.bind("<FocusOut>", self.default(self.dtext,self.location))

        self.fb = Label(self.Con1,text="Backup Device Name:",font=self.labelFont)
        self.fb.pack()

        self.dtext = "/databackup"
        self.locb = Entry(self.Con1)
        self.locb.insert(0, self.dtext)
        self.locb.pack()

        self.ua = Label(self.Con1,text="Architecture: ",font=self.labelFont)
        self.ua.pack()

        self.listitem = self.getTypes()
        self.varlist = StringVar(myParent)
        self.varlist.set("Pick Storage Array Architecture")

        self.drop = OptionMenu(self.Con1, self.varlist, *self.listitem[1])
        self.drop.pack()

        self.ub = Label(self.Con1,text="Users: ",font=self.labelFont)
        self.ub.pack()

        self.user = Text(self.Con1,height=2,width=30)
        self.user.insert(INSERT, "tom haw")
        self.user.pack(padx=20)
        self.user.focus()

        self.button = Button(self.Con1, command=self.addClick,text="Add Storage Device", background="red")
        self.button.pack()

    def default(event,text,box):
        current = box.get()
        #print current,'l'
        if current == text:
            #print "YES"
            box.delete(0,END)
        elif current == '':
            box.insert(0,text)

    def addClick(self):
        #requires listitem - listing of script locations and names
        print self.varlist.get()

        inlabel = self.varlist.get()
        listindex =  self.listitem[1].index(inlabel) #find index of script
        infile = open(self.listitem[0][listindex],'r')
        
        out = infile.readline() # bash line
        
        frequency = infile.readline() #Frequency comment

        key = ['#daily\n','#weekly\n','#monthly\n'] #possible comments
        to = ['/etc/cron.daily/','/etc/cron.weekly/','/etc/cron.monthly/']

        try:
            findex = key.index(frequency)
        except:
            print "The frequency comment in the selected script is not present or incorect (must be #monthly, #weekly, or #daily)"
            exit()

        floc = to[findex]+inlabel+'.cron' #Where we're putting the file
        #floc = '../test'+self.location.get()+'.cron' #Testing Only !!!!!!!!!

        #Next mount points
        out = out + '\n'
        out = out + 'DIR_DATA=\"' +self.location.get() +'\"\n'
        out = out + 'DIR_BACKUP=\"' +self.locb.get() +'\"\n'

        #Users
        users = self.user.get(1.0,END)
        out = out + 'DATA_USERS=\"'+users[0:-1] +'\"\n'

        readline = infile.readline() #Fill in script
        while readline != '':
            out = out + readline
            readline = infile.readline()

        ofile = open(floc,'w')
        ofile.write(out)

        devfile = open('.devices','a')
        devfile.write(self.location.get()+' '+inlabel+'  '+floc+' '+users[0:-1]+  '\n')
        devfile.close()

        self.myParent.destroy()
        self.bigInterface.destroy()


    def getTypes(self): 
        #Get all .cron  files, returns [paths,names]
        directory = 'scripts/'
        locations = glob.glob('{0}*.cron'.format(directory)) 
    
        names = []
        for loc in locations:
            names.append(loc.split('/')[-1].split('.')[0])
            #select just file name and not path

        return [locations,names]

class Interface:                         
    def __init__(self, myParent,devices):

        #------ constants for controlling layout ------
        button_width = 20
        short_button_width = 10

        button_padx = "2m"
        button_pady = "1m"
        short_padx = 15

        buttons_frame_padx =  "3m"
        buttons_frame_pady =  "2m"
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"

        full_width = 60
        frame_width = 30
        # -------------- end constants ----------------

        self.headFont = tkFont.Font(family="Helvetica",size=16)
        self.labelFont = tkFont.Font(family="Helvetica",size=12)

        self.myParent = myParent
        self.Con1 = Frame(myParent)
        self.Con1.pack(side=TOP,
            ipadx=buttons_frame_ipadx,  
            ipady=buttons_frame_ipady,  
            padx=buttons_frame_padx,    
            pady=buttons_frame_pady,    
            )

        self.devices = devices

        logo = PhotoImage(file="logo_sqs.png")
        self.title = Label(self.Con1, image=logo)
        self.title.photo = logo
        self.title.pack()

        self.Left = Frame(myParent,width=frame_width)
        self.Center = Frame(myParent,width=frame_width)
        self.Right = Frame(myParent,width=frame_width)

        self.Exit = Frame(myParent,width=full_width)
        self.Exit.pack(side=BOTTOM,
            ipadx=buttons_frame_ipadx,
            ipady=buttons_frame_ipady,
            )

        self.Left.pack(side=LEFT,
            ipadx=buttons_frame_ipadx,
            ipady=buttons_frame_ipady,
            )

        self.Center.pack(side=LEFT,
            ipadx=buttons_frame_ipadx,
            ipady=buttons_frame_ipady,
            )

        self.Right.pack(side=LEFT,
            ipadx=buttons_frame_ipadx,
            ipady=buttons_frame_ipady,
            )

        idx = 0
        for dev in devices:
            self.listn = Label(self.Left, text=dev[0]+' '+dev[1], 
font=self.labelFont,width=frame_width)
            self.listn.pack(side=TOP)
            self.user = Button(self.Center, 
command= lambda idx=idx: self.userClick(idx), text="Users")
            self.user.configure(
                width=short_button_width,
                padx=short_padx,
                pady=button_pady
            )
            self.user.pack(side=TOP)
            self.edit = Button(self.Right, 
command= lambda idx=idx: self.deleteClick(idx), text="Delete")
            self.edit.configure(
                width=short_button_width, 
                padx=short_padx,    
                pady=button_pady     
            )
            self.edit.pack(side=TOP)
            idx = idx + 1

        self.title = Label(self.Con1, text="Current Storage Devices",
font=self.headFont,padx=full_width)
        self.title.pack(side=TOP)

        self.button = Button(self.Exit, command=self.editClick,
text="Add New Storage Device", background="green")
        self.button.focus_force() #Not really needed
        self.button.configure(
            width=button_width,  ### (1)
            padx=button_padx,    ### (2)
            pady=button_pady     ### (2)
            )
        self.button.pack(side=TOP)

        self.ex = Button(self.Exit, command=self.exitClick,
text="Exit",background="red")
        self.ex.configure(
            width=button_width,  ### (1)
            padx=button_padx,    ### (2)
            pady=button_pady     ### (2)
            )
        self.ex.pack(side=TOP)

    def deleteClick(self,idx):
        infile = open('.devices','r')
        inline = infile.readline()
        outlist = ''
        internal = 0
        while inline != '':
            if internal != idx: #if we're not the desired target, keep
                outlist = outlist + inline
            else:
                os.remove(inline.split()[2])
            inline = infile.readline() 
            internal = internal+1
        infile.close()
        infile = open('.devices','w')
        infile.write(outlist)
        infile.close()

        self.myParent.destroy()

    def userClick(self,idx):
        r3 = Tk()
        r3.wm_title("Users")
        UserList(r3,idx)

    def exitClick(self):
        global complete
        complete = 1
        self.myParent.destroy()

    def editClick(self):
        r2 = Tk()
        #r2.geometry("600x400")
        new = Editor(r2,self.myParent)
        r2.wm_title("Add New Storage Device")
        r2.mainloop()

#Loop to keep main menu refreshed

while complete == 0:

    devfile = open('.devices','r')
    inline = devfile.readline()
    devices = []
    while inline != '':
        split = inline.split()
        devices.append(split)
        inline = devfile.readline()

    root = Tk()
    root.wm_title("LabHive Control Panel")
    myapp = Interface(root, devices)
    root.mainloop()      
