import time
import os

def main_changes():
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat('ex2.py')
    ther = "Wed Mar 30 19:49:22 2022"
    if time.ctime(mtime) != ther:
        print(time.ctime(mtime))
        print(f"You have been hacked")
        return False
    return True
