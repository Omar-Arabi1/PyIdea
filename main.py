from json import dump, load
import typer
from colorama import Fore, init
import os
import pathlib

init()

app = typer.Typer()

"""
Author: Omar Arabi

Date: 24 June 2025

Description:
this cli tool allows you to save ideas in "folders" so to speak you save headers to these
ideas and link full markdown files for more detail on them for example 
GoProjects:
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

"""
TODO: 
1. fix not being able to add new folders bug ✅
2. error handling for the entered link (exists as a file, is a markdown file) ✅
"""
    
@app.command() 
def add_idea(sub_folder: str, idea: str, link: str = ""):
    ideas_json: dict = read_json()

    # by splitting the values on whitespace doesn't allow the user to enter a bunch of spaces 
    # which would work if we compared it to an empty string since a whitespace spammed one isn't considered empty
    if len(idea.split()) == 0 or len(sub_folder.split()) == 0:
        print(Fore.RED + "The idea or sub-folder is empty dumbass")
        return
    else:
        for folder in ideas_json.keys():
            # checking if the idea exists withing the sub-folder the is selected by comparing the subfolder and checking if its value
            # exists withing the sub-folder the same for the link
            if sub_folder.upper() == folder and idea in ideas_json[folder].keys() or link in ideas_json[folder].values():
                print(Fore.RED + "idea/link already exists dumbass")
                return

    if not os.path.isfile(link):
        print(Fore.RED + f"{link} doesn't exist or is a directory")
        return 
    elif  pathlib.Path(link).suffix != ".md":
        print(Fore.RED + f"{link} must be in markdown")
        return 
    elif len(ideas_json.keys()) != 0 and sub_folder in ideas_json.keys():
        for l in ideas_json[sub_folder.upper()].values():
            if not os.path.isfile(l) and l != "":
                print(Fore.RED + f"{link} got deleted or something unknown so it got removed")

    if sub_folder.upper() in ideas_json.keys():
        ideas_json[sub_folder.upper()].update({ idea: link }) # we make the sub-folder uppercase don't ask me why its fun
    else:
        ideas_json.update({ sub_folder.upper(): { idea: link } })
    write_json(ideas_json)

if __name__ == "__main__":
    app()