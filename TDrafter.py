'''
Created on Jul 24, 2014

@author: hal
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
        self.counter = Label(self, textvariable=self.charNum).grid(padx = 10, row = 0, column = 0, sticky = SW) #remeber COUNTER GRID!!!
        
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
        theFile = open("savedTweets.p", "r")
        try:
            self.tweets = pickle.load(theFile)
            for item in self.tweets:
                print "printing", item
                self.saveBox.insert(END, item.strip())
        except:
            self.tweets = []
            print error
            
        theFile.close()
        self.saveBox.grid(row = 0, column = 1, sticky = E, rowspan = 1, padx = 10)
        
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
            api = tp.API(self.auth)
            #api.update_status(draft)
            print "Tweeted. Phew!"
        except tp.TweepError:
            print tp.tweepError
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
            self.saveTweets()
            self.insertIndex = None
            self.writeBox.delete("1.0", END)
        
    def saveTweets(self):
        theFile = open("savedTweets.p", "w")
        pickle.dump(self.tweets, theFile)
        theFile.close()
        self.loadSavedTweets()
        
    def delete(self):
        theTweet = self.getSaveBox()
        self.tweets.remove(theTweet)
        self.saveTweets()
        self.loadSavedTweets()
        
    def edit(self):
        self.writeBox.delete("1.0", END)
        toEdit = self.getSaveBox().strip()
        self.insertIndex = int(self.saveBox.curselection()[0])
        print "insertIndex: ", self.insertIndex
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
        self.auth = tp.OAuthHandler(self.apikey, self.apisecret)
        webbrowser.open(self.auth.get_authorization_url())
        pin = raw_input("Type your verification pin: ").strip()
        token = self.auth.get_access_token(pin)
        self.auth.set_access_token(token.key, token.secret)
        print self.auth
        self.saveAccess()
    
    def saveAccess(self):
        theFile = open("data.p", "w")
        pickle.dump (self.auth, theFile)
        print "Saved THE TOKEN!"
        
    def loadAccess(self):
        try:
            theFile = open("data.p", "r")
            self.auth = pickle.load(theFile)
            print "Loaded access token"
        except:
            print "No auth token yet!"
        

def main():
    root = Tk()
    root.resizable(0, 0)    #disables window resizing
    root.geometry("750x170+300+300") #must be created before others
    app = Example(root)
    root.mainloop()
        
if __name__ == '__main__':
    main()
