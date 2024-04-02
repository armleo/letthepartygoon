import tkinter as tk
import tkinter.filedialog
import os
import random
import sys

playlists_directories = []
lbls = []
playlists = dict()

def newPlaylistSelect():
    dir = tkinter.filedialog.askdirectory()
    playlists_directories.append(dir)
    
    lbl = tk.Label(window,text=dir)
    lbl.pack()
    lbls.append(lbl)

    print("Reading directory:", dir)
    cont = os.listdir(dir)
    print("Directory content:", len(cont), cont)
    if len(cont) != 0:
        random.shuffle(cont)
        playlists[dir] = cont
    

    
def saveNewPlaylist():
    saveNewPlaylistPath = tkinter.filedialog.asksaveasfilename(filetypes=[("m3u result playlist","*.m3u")], defaultextension="m3u")
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
    
    print(new_playlist)
    print(saveNewPlaylistPath)
    newPlaylistFile = open(saveNewPlaylistPath, "w+", encoding="utf-8")
    print("#EXTM3U",file=newPlaylistFile)
    for f in new_playlist:
        print(f, file=newPlaylistFile)
    sys.exit(0)

window = tk.Tk()

button = tk.Button(window, text='Select playlist folder', command=newPlaylistSelect)
button.pack()
save_button = tk.Button(window, text='Save playlist', command=saveNewPlaylist)
save_button.pack()

window.mainloop()
