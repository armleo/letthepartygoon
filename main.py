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
    global playlists_directories
    global playlists
    playlists_directories = []
    playlists = dict()


def addm3u(filepath, shuffle = True):
    print(f"Reading {filepath}")
    cont = []
    with open(filepath, "r") as f:
        lines = f.read().split("\n")
        for l in lines:
            if len(l) and l[0] == "#":
                print(f"Ignoring line {l}")
            elif len(l) > 0:
                print(f"Adding song {l} from playlit")
                cont.append(l)
    playlists_directories.append(filepath)
    playlists[filepath] = cont
    print(cont)

def addplaylist(dir, shuffle = True):
    
    print("Reading directory:", dir)
    cont = os.listdir(dir)
    print("Directory content:", len(cont), cont)
    
    if len(cont) != 0:
        playlists_directories.append(dir)
        playlists[dir] = []
        if shuffle:
            random.shuffle(cont)
        
        for c in cont:
            playlists[dir].append(os.path.normpath(os.path.join(dir, c)))
    

def saveplaylist(path):
    newPlaylistFile = open(path, "w+", encoding="utf-8")
    print("#EXTM3U",file=newPlaylistFile)
    
    done = False
    while not done:
        done = True
        for p in playlists_directories:
            print("Working on ", p)
            if (len(playlists[p]) != 0):
                print(urllib.parse.quote(playlists[p].pop()), file=newPlaylistFile)
                done = False
            else:
                print("Done", len(playlists[p]))
                done = True
                break
    newPlaylistFile.close()
    

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

def exp():
    reset()

    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")
    #addplaylist("kiz", False)
    #addplaylist("kiz", False)
    #addplaylist("kiz", False)
    addm3u("kizpl.m3u", False)
    addm3u("kizpl.m3u", False)
    addm3u("kizpl.m3u", False)
    saveplaylist("exp.m3u")

def b3s3():
    reset()
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")
    addplaylist("salsa")

    saveplaylist("b3s3.m3u")

def b3s2():
    reset()
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")

    saveplaylist("b3s2.m3u")


def b3s1():
    reset()
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    

    saveplaylist("b3s1.m3u")

def b4s2():
    reset()
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")

    saveplaylist("b4s2.m3u")

def b4s2b4s2k1():
    reset()
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("bachata")
    addplaylist("salsa")
    addplaylist("salsa")
    addplaylist("kiz")

    saveplaylist("b4s2b4s2k1.m3u")

os.makedirs("bachata", exist_ok=True)
os.makedirs("kiz", exist_ok=True)
os.makedirs("salsa", exist_ok=True)


b3s2k3()
b3s3()
b3s2()
b4s2()
b3s1()
b4s2b4s2k1()
exp()
