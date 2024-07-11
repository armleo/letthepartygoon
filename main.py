import os
import random
import sys
from pathlib import Path, PurePath
import urllib

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
playlists = dict()

def reset():
    playlists_directories = []
    playlists = dict()


def addplaylist(dir):
    
    print("Reading directory:", dir)
    cont = os.listdir(dir)
    print("Directory content:", len(cont), cont)
    if len(cont) != 0:
        playlists_directories.append(dir)
        random.shuffle(cont)
        playlists[dir] = cont
    

def saveplaylist(path):
    newPlaylistFile = open(path, "w+", encoding="utf-8")
    print("#EXTM3U",file=newPlaylistFile)
    
    done = False
    while not done:
        done = True
        for p in playlists_directories:
            print("Working on ", p)
            if (len(playlists[p]) != 0):
                f = os.path.normpath(os.path.join(p,playlists[p].pop()))
                print(urllib.parse.quote(f), file=newPlaylistFile)
                done = False
            else:
                print("Done", len(playlists[p]))
                done = True
                break
    

def b3s2k3():
    reset()

    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")
    addplaylist("kiz")
    addplaylist("kiz")
    addplaylist("kiz")

    saveplaylist("b3s2k3.m3u")

def b3s3():
    reset()
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")
    addplaylist("salsa")

    saveplaylist("b3s3.m3u")



os.makedirs("bachata", exist_ok=True)
os.makedirs("kiz", exist_ok=True)
os.makedirs("salsa", exist_ok=True)

b3s2k3()
# b3s3()

