from json import dump, load
import typer
from colorama import Fore, init

init()

app = typer.Typer()

"""
Author: Omar Arabi

Date: 24 June 2025

Description:
this cli tool allows you to save ideas in "folders" so to speak you save headers to these
ideas and link full markdown files for more detail on them for example 
GoProject:
    project: create a CLI tools
    link: /home/omar-arabi/obsidian/CLIGo.md
"""

# header -> link (optional) -> sub-folder


# loading/reading the json file containing the ideas and their destinations
def read_json():
    with open("Data/idea.json", mode="r", encoding="utf-8") as read_file:
        return load(read_file)

# writing to the json file containing the ideas and their destinations    
def write_json(dict_to_json):
    with open("Data/idea.json", mode="w", encoding="utf-8") as write_file:
        return dump(dict_to_json, write_file, indent=4)

@app.command()
def add_idea(sub_folder: str, idea: str, link: str = ""):
    ideas_json: dict = read_json()

    if len(idea.split()) == 0 or len(sub_folder.split) == 0:
        print(Fore.RED + "The idea or sub-folder is empty dumbass")
        return
    else:
        for folder in ideas_json.keys():
            if sub_folder == folder and ideas_json.get(folder) == idea:
                print(Fore.RED + "The idea is already exists dumbass")
                return

    ideas_json.update({ sub_folder.upper(): idea })
    
    write_json(ideas_json)

if __name__ == "__main__":
    app()
