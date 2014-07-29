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
        #self.atoken=""
        #self.asecret=""
        
        self.getAccess()
        self.parent = parent
        self.initUI()
        self.loadSavedTweets()
        
    def initUI(self):
        
        self.parent.title("TDrafter")
        self.pack(fill = BOTH, expand=True)
        
        self.writeBox = Text(self, width = 50, height = 3, padx = 10, pady = 10)
        self.writeBox.insert("1.0","draft your tweet here!")
        self.writeBox.pack(side = TOP, padx = 10, pady = 10)
        self.writeBox.bind("<KeyRelease>", self.updateCount)
        
        self.charNum = StringVar()
        self.counter = Label(self, textvariable=self.charNum).pack(side=TOP)
        
        self.saveButton = Button(self, text="Save", command = lambda: self.saveCurrent()).pack(side=TOP)
        
        self.tweetButton = Button(self, text="Tweet!", command = lambda: self.tweet()).pack(side = BOTTOM)
        
        self.deleteButton = Button(self, text="Delete", command = lambda: self.delete()).pack(side = BOTTOM)
        
        self.saveBox = Listbox(self, width = 70, height = 100)
        
        
    def loadSavedTweets(self): #also prints them :)
        self.saveBox.delete(0, END) #deletes what's currently in there
        self.writeBox.delete("1.0", END)
        print ("Loaded, I guess")
        theFile = open("savedTweets.p", "r")
        try:
            self.tweets = pickle.load(theFile)
            for item in self.tweets:
                self.saveBox.insert(0, item.strip())
        except:
            self.tweets = []
            
        theFile.close()
        self.saveBox.pack(padx=10, pady=10, side=BOTTOM)
        print ("Tweets array: ", self.tweets)
        
        
    def getWriteBox(self):
        contents = self.writeBox.get("1.0", END)
        return contents
    
    def getSaveBox(self):
        index = int(self.saveBox.curselection()[0])
        return self.saveBox.get(index)
        
    def tweet(self):
        draft = self.getSaveBox().strip()
        api = tp.API(self.auth)
        api.update_status(draft)
        print "Tweeted. Phew!"

    def saveCurrent(self):
        draft = self.getWriteBox()
        self.tweets.append(draft)
        self.saveTweets()
        
    def saveTweets(self):
        theFile = open("savedTweets.p", "w")
        pickle.dump(self.tweets, theFile)
        theFile.close()
        print ("Saved, I guess")
        self.loadSavedTweets()
        
        
    def delete(self):
        theTweet = self.getSaveBox()
        print theTweet
        self.tweets.remove(theTweet)
        self.saveTweets()
        self.loadSavedTweets()
    
    def updateCount(self, hello):
        value = self.count()
        value = str(value-1)
        print value
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
        

def main():
    root = Tk()
    #root.resizable(0, 0)    disables window resizing
    root.geometry("500x500") #must be created before others
    app = Example(root)
    root.mainloop()
        
if __name__ == '__main__':
    main()