#!/usr/bin/env python
import os, sys, re as rgx
from typing import Tuple
current_dir = os.getcwd()

import sqlite3 as sql

 
def TerminatePy(err = 0):
    exit(err)
def ExitPrint(string):
    print(string)
    TerminatePy()
    
def EnterNewShellAndExit(PATH):
    os.chdir(PATH)
    os.system("bash")
    TerminatePy(0)
     

def GetPWD():
    return os.path.dirname(os.path.realpath(__file__))
def getArg(index) -> tuple[str, list]:
    return sys.argv[index], sys.argv

def convPlatform(PATH):
    return PATH # rgx.sub(r"\\", r"//", PATH)
    

databasePath = f'{GetPWD()}/data/repo-brain.db'
con = sql.connect(f'{databasePath}')

def SavedDirTravel():
    repoId, args = getArg(1)
    if len(args) > 2:
        newRepoRegistry = args[1];
        if args[2] == 'add':
            print("Registering new Repo Name:", newRepoRegistry)
            err = DbSaveCurrentRepo(newRepoRegistry)
            if err: print(err)
        elif args[2] == 'remove':
            pass 
        else:
            return print("Use add or remove");
    else:
        repoPath, err = DbGetRepo(repoId)
        EnterNewShellAndExit(repoPath)
        if err: print(err)
        
            

    
     
    
    
def DbGetRepo(repoId) -> tuple[str, Exception | bool]:
     repositoryPath = ""
     
     tableName = 'repositories'
     
     try:
        res = con.execute(f"SELECT path FROM {tableName} WHERE name = ?", [repoId] );
        con.commit()
        [repositoryPath] = res.fetchone()
        
        if repositoryPath is None:
            raise Exception(f"NO ROW IN {tableName} matches {repoId}")
            
     except Exception as e:
         print(e)
         
         return "", e
     
     
     return repositoryPath, False;
 
def DbSaveCurrentRepo(repoId) -> Exception | bool:
     tableName = 'repositories'
     con.execute(f"CREATE TABLE IF NOT EXISTS {tableName}(name TEXT, path TEXT)" );
     try:
         
        res = con.execute(f"INSERT INTO {tableName} VALUES(?,?)",(repoId, os.getcwd(), ));
        con.commit()
        con.close()
     except Exception as e:
         print(e)
         return e     
     
     return False;
 

SavedDirTravel()
