#!/usr/bin/env python
import os
import sys
import sqlite3 as sql
from typing import List, Optional

class Repository:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

def terminate_py(err: int = 0) -> None:
    exit(err)

def enter_new_shell_and_exit(path: str) -> None:
    os.chdir(path)
    os.system("bash")
    terminate_py(0)

def get_pwd() -> str:
    return os.path.dirname(os.path.realpath(__file__))

def db_delete_repo_row(name: str) -> None:
    with sql.connect(database_path) as con:
        con.execute("DELETE FROM repositories WHERE name = ?", [name])
        con.commit()

def db_get_repo_list() -> List[Repository]:
    with sql.connect(database_path) as con:
        res = con.execute("SELECT * FROM repositories")
        return [Repository(name=row[0], path=row[1]) for row in res.fetchall()]

def db_get_repo(repo_id: str) -> Optional[str]:
    with sql.connect(database_path) as con:
        res = con.execute("SELECT path FROM repositories WHERE name = ?", [repo_id])
        row = res.fetchone()
        return row[0] if row else None

def db_save_current_repo(repo_id: str) -> None:
    with sql.connect(database_path) as con:
        con.execute("CREATE TABLE IF NOT EXISTS repositories(name TEXT, path TEXT)")
        con.execute("INSERT INTO repositories VALUES(?, ?)", (repo_id, os.getcwd()))
        con.commit()

def display_repositories() -> None:
    repos = db_get_repo_list()
    for repo in repos:
        print(f'Access Name: {repo.name}, Path: {repo.path}')

def saved_dir_travel() -> None:
    if len(sys.argv) < 2:
        print("""
            (git automation help)
            
            ARGS: list, fix, <arg:repo>, 
            <arg:repo>: add, delete/remove ..
        """)
        return

    command, *args = sys.argv[1], sys.argv[2:]

    if command == "list":
        display_repositories()
    elif command in ["delete", "remove"] and args:
        db_delete_repo_row(args[0][0])
    elif command in ['clean', 'fix']:
        for repo in db_get_repo_list():
            if not os.path.isdir(repo.path):
                print(f"Path does not exist.. removing: {repo.path}")
                db_delete_repo_row(repo.name)
    elif command == 'add' and args:
        print("Registering new Repo Name:", args[0][0])
        db_save_current_repo(args[0][0])
    else:
        repo_path = db_get_repo(command)
        if repo_path:
            enter_new_shell_and_exit(repo_path)
        else:
            print(f"Repository '{command}' not found.")

database_path = f'{get_pwd()}/data/repo-brain.db'

if __name__ == "__main__":
    saved_dir_travel()
