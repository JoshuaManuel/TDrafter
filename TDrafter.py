'''
Created on Jul 24, 2014

VERSION: 1.1.0

*This is the first version ready for a multiplatform use
*If you encounter errors when starting up the program, try making empty files called "savedTweets.p" and "data.p" in the program's current directory

Author: Joshua Manuel

If you have any issues, contact me at:
@QuiteRather
manueljosh3[at]gmail.com

THIS CODE IS CURRENTLY PROVIDED WITHOUT A LISENCE, WHICH MEANS, TECHNICALLY YOU HAVE NO LEGAL RIGHT TO USE IT.
I THINK.

>:/

'''

from Tkinter import *
import cPickle as pickle
import tweepy as tp
import webbrowser

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        
        self.apikey="kFccJJtoM20smgxwIjGnCcqDX"
        self.apisecret="7cz3XcENohWT2N2KvRh6pwXXs0WC9gHVb6Mf9pW8caGoGlbDIV"
        
        self.insertIndex = None
        self.tweets = []
        self.auth = tp.OAuthHandler(self.apikey, self.apisecret)
        
        self.parent = parent
        self.initUI()
        self.loadSavedTweets()
        self.loadAccess()
        
    def initUI(self):
        
        self.parent.title("TDrafter")
        self.pack(fill = BOTH, expand=True)
        
        self.writeBox = Text(self, wrap = WORD, padx = 10, pady = 10, width = 40, height = 4)
        self.writeBox.insert("1.0","draft your tweet here!")
        self.writeBox.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.writeBox.bind("<KeyRelease>", self.updateCount)
        
        self.charNum = StringVar()
        self.counter = Label(self, textvariable=self.charNum, bg = "white").grid(padx = 10, row = 0, column = 0, sticky = SW) #remeber COUNTER GRID!!!
        
        self.saveButton = Button(self, text="Save", command = lambda: self.saveCurrent()).grid(row = 0, column = 0, sticky = SE, padx = 10)
        
        self.tweetButton = Button(self, text="Tweet!", command = lambda: self.tweet()).grid(row = 0, column = 2, sticky = N)
        self.deleteButton = Button(self, text="Edit", command = lambda: self.edit()).grid(row = 0, column = 2, sticky = EW)
        self.editButton = Button(self, text="Delete", command = lambda: self.delete()).grid(row = 0, column = 2, sticky = S)

        self.saveBox = Listbox(self, width = 40)
        
    def clearBoth(self):
        self.saveBox.delete(0, END) #deletes what's currently in there
        self.writeBox.delete("1.0", END)
    
    def loadSavedTweets(self): #also prints them :)
        self.saveBox.delete(0, END)
        theFile = open("savedTweets.p", "a")
        theFile.close()
        theFile = open("savedTweets.p", "r")
        try:
            self.tweets = pickle.load(theFile)
            for item in self.tweets:
                self.saveBox.insert(END, item.strip())
        except:
            pass
        theFile.close()
        self.saveBox.grid(row = 0, column = 1, sticky = E, rowspan = 1, padx = 10)
        
    def getWriteBox(self):
        contents = self.writeBox.get("1.0", END)
        return contents
    
    def getSaveBox(self):
        try:
            index = int(self.saveBox.curselection()[0])
            return self.saveBox.get(index)
        except:
            pass
        
    def tweet(self):
        draft = self.getSaveBox().strip()
        print draft
        try:
            api = tp.API(self.auth)
            api.update_status(draft)
            print "Tweeted. Phew!"
        except tp.TweepError:
            self.getAccess()

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
            self.saveTweets()
            self.loadSavedTweets()
            self.writeBox.delete("1.0", END)
            self.saveBox.selection_set(END)
            self.saveBox.see(END)
            
        
    def saveTweets(self):
        theFile = open("savedTweets.p", "w")
        pickle.dump(self.tweets, theFile)
        theFile.close()
        
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
        self.loadSavedTweets()
    
    def updateCount(self, hello):
        value = self.count()
        value = str(value-1)
        self.charNum.set(value)
        
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
                self.saveAccess()
                self.tweet()
            
            top = Toplevel()
            top.title("TDrafter")
            msg = Label(top, text="Enter your verification pin to log in:\n(A browser window should have opened)")
            msg.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)
            
            enter = Entry(top)
            enter.grid(row = 1, column = 0, padx = 10)
            
            button = Button(top, text="Submit", command=callback)
            button.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = S)
            top.pack()
        except:
            print "You didn't enter the pin! C'mon, man..."
            pass
    
    def saveAccess(self):
        theFile = open("data.p", "w")
        pickle.dump (self.auth, theFile)
        print "Saved your auth token"
        
    def loadAccess(self):
        try:
            theFile = open("data.p", "a")
            theFile.close()
            theFile = open("data.p", "r")
            self.auth = pickle.load(theFile)
            theFile.close()
            print "Loaded access token"
        except:
            print "No auth token yet!"
            self.getAccess()
        

def main():
    root = Tk()
    root.resizable(0, 0)    #disables window resizing
    root.geometry("750x170+300+300") #must be created before others
    app = Example(root)
    root.mainloop()
        
if __name__ == '__main__':
    main()
