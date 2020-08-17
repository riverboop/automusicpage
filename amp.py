#Auto Music Page Version 1.3  by Rin Dyke
import os
import string
import tkinter
from tkinter import *
import tkinter.filedialog as filedialog
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import argparse
import subprocess
#args
parser = argparse.ArgumentParser(description='Creates an webpage with mp3 from an album')
parser.add_argument('-in', "--input_folder", type=str,  help='the folder with the audio files and album cover')
parser.add_argument('-nw', "--no_window", action='store_true', default='False', help='don\'t open the gui')
parser.add_argument('-nz', "--no_zip", action='store_true', default="False", help='create a zip file with the songs')
global args
args = parser.parse_args()
curdir = os.getcwd
tempdir = args.input_folder

def getandmake():
    songlist = []
    pathlist = []
    titlelist = []
    blocks=[]
    a = ""
    imgext = (".jpeg", ".jpg", ".png")
#convert ogg to mp3
    for file in os.listdir(tempdir):
        if file.endswith(".ogg"):
            filepath = tempdir + "/" + file
            command = "ffmpeg -i \""+filepath+"\" -map_metadata 0:s:0 -acodec libmp3lame \""+filepath.strip(".ogg")+".mp3\""
            subprocess.call(command, shell=True)
            os.remove(filepath)
        if file.endswith(".mp3"):
            pathlist.append(tempdir + "/" + file)
            songlist.append(file)
        elif file.endswith(imgext):
            cover = file
        songlist.sort()
        pathlist.sort()
    x = 0
    audio = ""
    bigblock = ""
    a = audio                         
    album = ""
    for song in pathlist:
        audio = MP3(song, ID3=EasyID3)
#zip files
        if(str(args.no_zip) == "False"):
            zipcom= "zip " + tempdir + "/album.zip \"" + str(song) + "\""
            subprocess.call(zipcom, shell=True)
#get id3 data
        try:
            title = str(audio["title"])
        except:
            title = input(song + " title: ")
        titlelist.append(title.strip("[] \'"))
        var2 = "<li> <h4>" + titlelist[x] + "</h4> <audio controls> <source src=\"" + songlist[x] + "\"type=\"audio/mpeg\"> </audio> </li>"
        blocks.append(var2)
        bigblock += blocks[x]
        x += 1
    if(album == ""):
        try:
            album = str(audio["album"])
        except:
            album = input("album: ")
            album = album.strip("[] \'")
#create html file
        try:
            var1 = "<!DOCTYPE html> <html> <head> <link href=\"/main.css\" type=\"text/css\" rel=\"stylesheet\"> </head>  <body> <img width=120 height=120 src=\"" + cover + "\"> <h1>" + album + "</h1> <ol>"
            out = var1 + bigblock + "</ol> </body> </html>"
            f = open(tempdir + "/" + "index.html", "w")
            f.write(out)
            if (str(args.no_window)== "False"):
                lbl.set("HTML File Created!")
            else:
                print("HTML File Created!")
#excpetion handling
        except UnboundLocalError:
            if (str(args.no_window) == "True"):
                if (bigblock == ""):
                    print ("ERROR: No music files")
                else:
                    print("ERROR: No album cover image")
if (str(args.no_window) == "True"):
    getandmake()
else: 
    class Gui:
        def __init__(self, master):
            self.master = master
            master.title("Auto Music Page v1.2")
            self.open_button = Button(master, text="Open Folder", command=self.open)
            self.open_button.place(relx=0.5, rely=0.5, anchor=CENTER)
            self.close = Button(master, text="Exit", command=self.close)
            self.close.place(relx=0.5, rely=0.75, anchor=CENTER)
            global lbl
            lbl = tkinter.StringVar(master)
            lbl.set("")
            self.stdlbl = Label(master, textvariable=lbl)
            self.stdlbl.place(relx=0.5, rely=0.25, anchor=CENTER)
        def open(self):
            root = tkinter.Tk()
            root.withdraw()
            curdir = os.getcwd()
            global tempdir
            tempdir = filedialog.askdirectory(parent=root, initialdir=curdir, title='Select a folder with songs')
            lbl.set("")
            getandmake()
        def close(self):
            root.destroy()
            root.quit()
    root = Tk()
    root.geometry("300x200") #width x height
    my_gui = Gui(root)
    root.mainloop()
    
    
