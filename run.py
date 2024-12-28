#!/usr/bin/env python
import os
current_dir = os.getcwd()

import sqlite3 as sql

def TerminatePy(err = 0):
    exit(err)
    
def EnterNewShellAndExit():
    os.system("bash")
    
    TerminatePy(1)
    exit(1)

def MainShell_Pending_CD(Path)   :
    current_dir = os.getcwd()
    # print(f"Current Working Directory: {current_dir}")

    os.chdir(f'{current_dir}/{Path}')
     
    updated_dir = os.getcwd()
    
    
    print(f'{current_dir}/{Path}')
    
    TerminatePy()
    
    return EnterNewShellAndExit()
    

# impl 
#     

ver = MainShell_Pending_CD("glib")

