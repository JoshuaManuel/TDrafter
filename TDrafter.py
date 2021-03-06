'''
Created on Jul 24, 2014

Author: Joshua Manuel

If you have any issues, contact me at:
@QuiteRather
manueljosh3[at]gmail.com

THIS CODE IS CURRENTLY PROVIDED WITHOUT A LISENCE, WHICH MEANS, TECHNICALLY YOU HAVE NO LEGAL RIGHT TO USE IT.
I THINK.

If you need to uninstall the program, don't forget to remove the hidden /.TDrafter file in your home directory

>:/

'''

from Tkinter import *
from threading import Thread
import Queue
import tkFileDialog
import tkMessageBox
import cPickle as pickle
import tweepy as tp
import webbrowser
import os
import os.path
import shutil

class TDrafter(Frame, Thread):
    
    def run(self):
        #The program's API key for Twitter
        self.apikey="kFccJJtoM20smgxwIjGnCcqDX"
        self.apisecret="7cz3XcENohWT2N2KvRh6pwXXs0WC9gHVb6Mf9pW8caGoGlbDIV"
        
        self.insertIndex = None
        self.tweets = []
        self.auth = tp.OAuthHandler(self.apikey, self.apisecret)
        self.api = tp.API(self.auth)
        
        self.home = os.path.expanduser("~")
        if not os.path.exists(self.home + "/.TDrafter"):
            os.makedirs(self.home + "/.TDrafter")
        
        #SETUP THE WINDOW
        self.parent = Tk()
        self.parent.resizable(0, 0)
        self.parent.geometry("750x170+300+300")
        self.parent.protocol("WM_DELETE_WINDOW", self.ask_quit)
        Frame.__init__(self, background="white")
        
        
        ###########fill the window############ 
        
        
        self.parent.title("TDrafter")
        self.pack(fill = BOTH, expand=True)
        
        self.writeBox = Text(self, wrap = WORD, padx = 10, pady = 10, width = 40, height = 4)
        self.writeBox.insert("1.0","draft your tweet here!")
        self.writeBox.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.writeBox.bind("<KeyRelease>", self.updateCount)
        
        self.counter = Label(self, text = self.count(), bg = "white")
        self.counter.grid(padx = 10, row = 0, column = 0, sticky = SW)
        
        self.saveButton = Button(self, text = "Save", command = lambda: self.saveCurrent()).grid(row = 0, column = 0, sticky = SE, padx = 10)
        
        self.tweetButton = Button(self, text = "Tweet!", command = lambda: self.tweet()).grid(row = 0, column = 2, sticky = N)
        self.deleteButton = Button(self, text = "Edit", command = lambda: self.edit()).grid(row = 0, column = 2, sticky = EW)
        self.editButton = Button(self, text = "Delete", command = lambda: self.delete()).grid(row = 0, column = 2, sticky = S)

        self.saveBox = Listbox(self, width = 40)
        self.saveBox.grid(row = 0, column = 1, sticky = E, rowspan = 1, padx = 10)
        self.createMenu()
        
        self.mainloop()
        
    def getWriteBox(self):
        contents = self.writeBox.get("1.0", END)
        return contents
    
    def getSaveBox(self):
        index = int(self.saveBox.curselection()[0])
        return self.saveBox.get(index)
        
    def tweet(self):
        draft = self.getSaveBox().strip()
        print draft
        try:
            self.api.update_status(draft)
            tkMessageBox.showinfo("TDrafter", message='Tweeted!')
        except tp.TweepError:
            self.getAccess()
            
    def renderTweets(self):
        self.saveBox.delete(0, END)
        for item in self.tweets:
            self.saveBox.insert(END, item.strip())

    def saveCurrent(self):
        if len(self.getWriteBox()) > 140:
            print "Sorry, too long! This is twitter, remember?"
        else:
            draft = self.getWriteBox().strip()
            if self.insertIndex == None:
                self.tweets.append(draft)
            else:
                try:
                    self.tweets[self.insertIndex] = draft
                except:
                    print "Error inserting the tweet back"
            
            self.insertIndex = None
            self.writeBox.delete("1.0", END)
            self.renderTweets()
            self.saveBox.selection_set(END)
            self.saveBox.see(END)
        
    def delete(self):
        theTweet = self.getSaveBox()
        self.tweets.remove(theTweet)
        self.saveTweets()
        self.loadSavedTweets()
        if self.insertIndex != None:
            self.saveBox.selection_set(self.insertIndex)
            self.saveBox.see(self.insertIndex)
        else:
            self.saveBox.selection_set(END)
            self.saveBox.see(END)
        
    def edit(self):
        self.writeBox.delete("1.0", END)
        toEdit = self.getSaveBox().strip()
        self.insertIndex = int(self.saveBox.curselection()[0])
        self.writeBox.insert(INSERT, toEdit)
    
    def updateCount(self, a):
        value = self.count()
        value = str(value-1)
        self.counter.config(text = value)
        
    def count(self):
        a = self.getWriteBox()
        return len(a)
    
    def getAccess(self):
        try:
            webbrowser.open(self.auth.get_authorization_url())
            
            def callback():
                pin = enter.get()
                top.destroy()
                try:
                    token = self.auth.get_access_token(pin)
                    self.auth.set_access_token(token.key, token.secret)
                except:
                    self.auth = None
                    pass
                
            
            top = Toplevel()
            top.title("TDrafter")
            msg = Label(top, text="You haven't logged in yet!\nEnter your verification pin to log in:\n(A browser window should have opened)")
            msg.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)
            
            enter = Entry(top)
            enter.grid(row = 1, column = 0, padx = 10)
            
            button = Button(top, text="Submit", command=callback)
            button.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = S)
            top.pack()
        except:
            pass
        
    def createMenu(self):
        self.menuBar = Menu(self)
        self.fileMenu = Menu(self.menuBar)
        self.fileMenu.add_command(label = "New", command = self.newWindow)
        self.fileMenu.add_command(label = "Open", command = self.loadState)
        self.fileMenu.add_command(label = "Save As...", command = self.saveState)
        self.fileMenu.add_command(label = "Delete", command = self.deleteState)
        self.menuBar.add_cascade(label="File", menu = self.fileMenu)
        self.parent.config(menu=self.menuBar)
        
    def newWindow(self):
        print "function will be replaced"
        
    def loadState(self):
        path = tkFileDialog.askdirectory(initialdir=self.home + "/.TDrafter")
        print "Loadstate: ", path
        dataFile = open(path + "/access.p", "r")
        self.auth = pickle.load(dataFile)
        dataFile.close()
        tweetsFile = open(path + "/tweets.p", "r")
        self.tweets = pickle.load(tweetsFile)
        tweetsFile.close()
        self.renderTweets()
        
        self.api = tp.API(self.auth)
        self.info = self.api.me()
        self.renderName()
        
    def saveState(self):
        path = tkFileDialog.askdirectory(initialdir=self.home + "/.TDrafter")
        print "saveState", path
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        dataFile = open(path + "/access.p", "w")
        pickle.dump(self.auth, dataFile)
        dataFile.close()
        tweetsFile = open(path + "/tweets.p", "w")
        pickle.dump(self.tweets, tweetsFile)
        tweetsFile.close()
        
    def deleteState(self):
        path = tkFileDialog.askdirectory(initialdir=self.home + "/.TDrafter")
        shutil.rmtree(path)
        
    def renderName(self):
        name = self.info.screen_name
        a = Label(text=name, bg="white").grid(sticky=N, padx = 10, pady = 10)
    
    def ask_quit(self):
        if tkMessageBox.askyesno("Save?", "Save session first?"):
            self.saveState()
        self.quit()
        
if __name__ == '__main__':
    foo = TDrafter()
    foo.run()