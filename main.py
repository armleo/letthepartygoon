import tkinter as tk
import tkinter.filedialog
import os
import random
import sys

frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS
    print("cd into", os.path.dirname(sys.executable))
    os.chdir(os.path.dirname(sys.executable))
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    print("cd into", bundle_dir)
    os.chdir(bundle_dir)

print('we are', frozen, 'frozen')
print('bundle dir is', bundle_dir)
print('sys.argv[0] is', sys.argv[0])
print('sys.executable is', sys.executable)
print('os.getcwd is', os.getcwd())

playlists_directories = []
lbls = []
playlists = dict()


def addplaylist(dir):
    
    print("Reading directory:", dir)
    cont = os.listdir(dir)
    print("Directory content:", len(cont), cont)
    if len(cont) != 0:
        playlists_directories.append(dir)
        random.shuffle(cont)
        playlists[dir] = cont
    
def newPlaylistSelectButton():
    dir = tkinter.filedialog.askdirectory()
    
    addplaylist(dir)

    lbl = tk.Label(window,text=dir)
    lbl.pack()
    lbls.append(lbl)
    

def saveNewPlaylistButton():
    saveNewPlaylistPath = tkinter.filedialog.asksaveasfilename(filetypes=[("m3u result playlist","*.m3u")], defaultextension="m3u")
    saveplaylist(saveplaylist)
    sys.exit(0)

def saveplaylist(path):
    new_playlist = []
    done = False
    while not done:
        for p in playlists_directories:
            print("Working on ", p)
            if (len(playlists[p]) != 0):
                new_playlist.append(os.path.normpath(os.path.join(p,playlists[p].pop())))
            else:
                print("Done", len(playlists[p]))
                done = True
        else:
            done = True
    print(new_playlist)
    print(path)
    newPlaylistFile = open(path, "w+", encoding="utf-8")
    print("#EXTM3U",file=newPlaylistFile)
    for f in new_playlist:
        print(f, file=newPlaylistFile)
    

def b3s2k3():
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")
    addplaylist("kiz")
    addplaylist("kiz")
    addplaylist("kiz")

    saveplaylist("output.m3u")

    sys.exit(0)

def b3s3():
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")
    addplaylist("salsa")

    saveplaylist("output.m3u")

    sys.exit(0)


os.makedirs("bachata", exist_ok=True)
os.makedirs("kiz", exist_ok=True)
os.makedirs("salsa", exist_ok=True)


window = tk.Tk()

button = tk.Button(window, text='3xBachata,2xSalsa,3xKiz', command=b3s2k3)
button.pack()

button = tk.Button(window, text='3xBachata,3xSalsa', command=b3s3)
button.pack()


window.mainloop()
