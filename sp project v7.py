from Tkinter import * 
from tkSimpleDialog import askstring
from tkFileDialog import asksaveasfilename
from tkFileDialog import askopenfilename
import tkMessageBox
import sys
import keyword
from string import ascii_letters, digits, punctuation, join

import cPickle as pickle
import string
co45_d=pickle.load(open('store',"rb"))
co45_d3=pickle.load(open('word_store',"rb"))

#removing punctuations
valid = string.ascii_uppercase + string.ascii_lowercase
valid+='0123456789'
co45_d2={}
for i in valid:
    co45_d2[i]=True


def pythonSyntax():
    root = Tk()
    sht = SyntaxHighlightingText(root)
    sht.pack()
    root.mainloop()

class SyntaxHighlightingText(Text):

    tags = {'kw': 'orange',
            'int': 'red'}

    def __init__(self, root):
        Text.__init__(self, root)
        self.config_tags()
        self.characters = ascii_letters + digits + punctuation

        self.bind('<Key>', self.key_press)

    def config_tags(self):
        for tag, val in self.tags.items():
            self.tag_config(tag, foreground=val)

    def remove_tags(self, start, end):
        for tag in self.tags.keys():
            self.tag_remove(tag, start, end)

    def key_press(self, key):
        cline = self.index(INSERT).split('.')[0]
        lastcol = 0
        char = self.get('%s.%d'%(cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d'%(cline, lastcol))

        buffer = self.get('%s.%d'%(cline,0),'%s.%d'%(cline,lastcol))
        tokenized = buffer.split(' ')

        self.remove_tags('%s.%d'%(cline, 0), '%s.%d'%(cline, lastcol))

        start, end = 0, 0
        for token in tokenized:
            end = start + len(token)
            if token in keyword.kwlist:
                self.tag_add('kw', '%s.%d'%(cline, start), '%s.%d'%(cline, end))
            else:
                for index in range(len(token)):
                    try:
                        int(token[index])
                    except ValueError:
                        pass
                    else:
                        self.tag_add('int', '%s.%d'%(cline, start+index))

            start += len(token)+1

class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)               
        self.makewidgets()
        self.settext(text, file)
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN, undo=True)
        sbar.config(command=text.yview)                  
        text.config(yscrollcommand=sbar.set)           
        sbar.pack(side=RIGHT, fill=Y)                   
        text.pack(side=LEFT, expand=YES, fill=BOTH)     
        self.text = text
    def settext(self, text='', file=None):
        if file: 
            text = open(file, 'r').read()
        self.text.delete('1.0', END)                   
        self.text.insert('1.0', text)                  
        self.text.mark_set(INSERT, '1.0')              
        self.text.focus()                                
    def gettext(self):                               
        return self.text.get('1.0', END+'-1c')         


class SimpleEditor(ScrolledText):                        
    def __init__(self, parent=None, file=None): 
        frm=Tk()
        frm.geometry('600x600+100+50')
        frm.title('Text Editor')
        menubar=Menu(frm)
        filemenu=Menu(menubar,tearoff=0)
        filemenu.add_command(label='Open',command=self.onOpen)
        filemenu.add_command(label='Save',command=self.onSave)
        filemenu.add_command(label='Find',command=self.onFind)
        filemenu.add_command(label='Quit',command=self.onQuit)     
        menubar.add_cascade(label='File',menu=filemenu)

        filemenu1=Menu(menubar,tearoff=0)
        filemenu1.add_command(label='Copy',command=self.onCopy)
        filemenu1.add_command(label='Cut',command=self.onCut)
        filemenu1.add_command(label='Paste',command=self.onPaste)
        filemenu1.add_command(label='Delete',command=self.onDelete)
        filemenu1.add_command(label='Select All',command=self.onSelect)
        filemenu1.add_command(label='Undo',command=self.onUndo)
        filemenu1.add_command(label='Redo',command=self.onRedo)

        menubar.add_cascade(label='Edit',menu=filemenu1)

        filemenu2=Menu(menubar,tearoff=0)
        filemenu2.add_command(label='Team Members',command=self.onTeam)
        filemenu2.add_command(label='Acknowledgements',command=self.onCredits)
        filemenu2.add_command(label='References',command=self.references)        
        filemenu2.add_command(label='Python Syntax Checker',command=pythonSyntax)        
        menubar.add_cascade(label='Misc',menu=filemenu2)

        filemenu3=Menu(menubar,tearoff=0)
        filemenu3.add_command(label='C',command=self.c)
        filemenu3.add_command(label='C++',command=self.cpp)
        filemenu3.add_command(label='Java',command=self.java)
        filemenu3.add_command(label='HTML',command=self.html)
        menubar.add_cascade(label='Templates',menu=filemenu3)

        filemenu4=Menu(menubar,tearoff=0)
        filemenu4.add_command(label='Word Count',command=self.onCount)
        filemenu4.add_command(label='Spell check',command=self.onCheck)
        filemenu4.add_command(label='See Meaning',command=self.onMeaning)
        menubar.add_cascade(label='Lexical Features',menu=filemenu4)

        ScrolledText.__init__(self, parent, file=file)
        frm.config(menu=menubar)

    def onSelect(self):
        self.text.tag_add(SEL, '1.0', END)

    def onCount(self):
        alltext=self.gettext()
        charCount=str(len(alltext))
        textline=alltext.split("\n")
        lineCount=str(len(textline))
        textword=alltext.split()
        wordCount=str(len(textword))
        tkMessageBox.showinfo(title="Word Count",message="Number of words = "+wordCount+"\nNumber of characters = "+charCount+"\nNumber of lines = "+lineCount)
        
    def onCredits(self):
        tkMessageBox.showinfo(title="Acknowledgements",message="We are extremely grateful on being given this opportunity \
to create and develop a text editor from scratch.\n\nThrough this project we were provided with the opportunity to learn a new programming language: Python. \
Each member of the group was able to adequately implement some functions and had a chance to learn and master different aspects of the language.\n\n\
We would like to thank Mr. Deepak Prabhu for providing us with the prospect of using our programming skills to implement a real world function.")

    def references(self):
        tkMessageBox.showinfo(title="References",message="Online tutorials  on GUI development in Python\n\n1)effbot.org\n\n2)tutorialspoint.com\n\n3)YouTube Tutorials by Derek Banas- youtube.com")
        return    

    def ext(self):
        e=tkMessageBox.askyesno(title="Quit",message="Are you sure?")
        if e>0:
            self.destroy()
            return

    def onTeam(self):
        tkMessageBox.showinfo(title="Member Details",message="11CO37 - Gaurav Mokhasi\n11CO43 - Jay Priyadarshi\n11CO45 - Aditya Kadam\n11CO46 - Karan Sabhani")

    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.gettext()                      
            open(filename, 'w').write(alltext)

    def onOpen(self):
        filename = askopenfilename()
        if filename:
            alltext = open(filename, 'r').read()
            self.settext(alltext)

    def onCopy(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(text)

    def onDelete(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)        
        self.text.delete(SEL_FIRST, SEL_LAST)

    def onCut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)        
        self.text.delete(SEL_FIRST, SEL_LAST)           
        self.clipboard_clear()              
        self.clipboard_append(text)
        
    def onPaste(self):                                    
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass

    def onUndo(self):
        self.text.edit_undo()

    def onRedo(self):
        self.text.edit_redo()

    def c(self):
        alltext = open('c.txt', 'r').read()
        self.settext(alltext)

    def cpp(self):
        alltext = open('cpp.txt', 'r').read()
        self.settext(alltext)

    def java(self):
        alltext = open('java.txt', 'r').read()
        self.settext(alltext)

    def html(self):
        alltext = open('html.txt', 'r').read()
        self.settext(alltext)
        

    def onFind(self):
        target = askstring('SimpleEditor', 'Search String?')
        if target:
            where = self.text.search(target, INSERT, END)  
            if where:                                    
                print where
                pastit = where + ('+%dc' % len(target))   
                self.text.tag_add(SEL, where, pastit)     
                self.text.mark_set(INSERT, pastit)         
                self.text.see(INSERT)                    
                self.text.focus()

    def onCheck(self):
        #self.gettext()
        #target = askstring('SimpleEditor', 'Enter word to check spelling')

        target2 = self.text.get(SEL_FIRST, SEL_LAST)
        target2.strip()
        
        target=''

        for i in target2:
            if(co45_d2.has_key(i)):
                target+=i
            
        if(co45_d.has_key(target.lower()) or co45_d3.has_key(target.lower())):
            tkMessageBox.showinfo(title="Spell Checker",message="Word is Correct!")
        else:
            tkMessageBox.showinfo(title="Spell Checker",message="Sorry , Word is Incorrect!")
            
    def onMeaning(self):
        #self.gettext()
        #target = askstring('SimpleEditor', 'Enter word to check spelling')

        target2 = self.text.get(SEL_FIRST, SEL_LAST)
        target2.strip()
        
        target=''

        for i in target2:
            if(co45_d2.has_key(i)):
                target+=i
            
        if(co45_d3.has_key(target.lower())):
            tkMessageBox.showinfo(title="Meaning Box",message=target+" :\n"+co45_d3[target])
        else:
            tkMessageBox.showinfo(title="Meaning Box",message="Sorry , Word is not present in dictionary!")


    def onQuit(self):
        ans=tkMessageBox.askyesno(title="Quit",message="Are you sure?")
        if ans:
            exit()
            return

    
if __name__ == '__main__':    
    SimpleEditor().mainloop()
