from json import dump, load
import typer
from colorama import Fore, init
import os
import pathlib

# we use this to start colorama to color the output
init()

# we create the app
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

# loading/reading the json file containing the ideas and their destinations
def read_json():
    with open("Data/idea.json", mode="r", encoding="utf-8") as read_file:
        return load(read_file)

# writing to the json file containing the ideas and their destinations    
def write_json(dict_to_json):
    with open("Data/idea.json", mode="w", encoding="utf-8") as write_file:
        return dump(dict_to_json, write_file, indent=4)
    
def check_if_exists(s_folder: str, idea_json: dict):
    # we check if there are any sub-folders to check for the links inside of them
    if len(idea_json.keys()) != 0 and s_folder.upper() in idea_json.keys():
        keys = list(idea_json[s_folder.upper()].keys()) # we take the sub-folders out so that we could change each link separately
        for i, l in enumerate(idea_json[s_folder.upper()].values()):
            # we check if it exists and is a file and also if it isn't empty 
            # because that would give error messages for no reason and also check the extension
            if not os.path.isfile(l) and l != "" and not pathlib.Path(l).suffix != ".md":
                # if it is not found we make it empty and notify the user
                print(Fore.RED + f"{l} got deleted or changed its absolute so it got removed")
                idea_json[s_folder.upper()][keys[i]] = "" 
                write_json(idea_json)

@app.command() 
def add_idea(sub_folder: str, idea: str, link: str = ""):
    ideas_json: dict = read_json()
    check_if_exists(sub_folder, ideas_json) # we always run this to always check for if links are missed

    # by splitting the values on whitespace doesn't allow the user to enter a bunch of spaces 
    # which would work if we compared it to an empty string since a whitespace spammed one isn't considered empty
    if len(idea.split()) == 0 or len(sub_folder.split()) == 0:
        print(Fore.RED + "The idea or sub-folder is empty dumbass")
        return
    else:
        for folder in ideas_json.keys():
            # checking if the idea exists withing the sub-folder the is selected by comparing the subfolder and checking if its value
            # exists withing the sub-folder the same for the link
            if sub_folder.upper() == folder and idea in ideas_json[folder].keys() or link in ideas_json[folder].values() and link != "":
                print(Fore.RED + "idea/link already exists dumbass")
                return

    # we chceck if its a file and if it is a markdown file
    if not os.path.isfile(link) and link != "":
        print(Fore.RED + f"{link} doesn't exist or is a directory")
        return 
    elif  pathlib.Path(link).suffix != ".md" and link != "":
        print(Fore.RED + f"{link} must be in markdown")
        return 

    # if there is a sub-folder and the user chose it we update it if not we create it
    if sub_folder.upper() in ideas_json.keys():
        ideas_json[sub_folder.upper()].update({ idea: link }) # we make the sub-folder uppercase don't ask me why its fun
    else:
        ideas_json.update({ sub_folder.upper(): { idea: link } })

    write_json(ideas_json)

@app.command()
def list_sub_folders():
    ideas_json: dict = read_json()
    sub_folders = list(ideas_json.keys())     
    
    for sub_folder in sub_folders:
        check_if_exists(sub_folder, ideas_json) 
        ideas = list(ideas_json[sub_folder].keys()) 
        print(Fore.BLACK + sub_folder + ":") 
        for index, idea in enumerate(ideas):
            # we are getting the values (links) for each sub-folder and checking if its empty if it is 
            # we print something else other than it
            if list(ideas_json[sub_folder].values())[index] != "":
                print(Fore.GREEN + f" {Fore.BLUE + ">>> " + str(index + 1)} - {Fore.GREEN + idea} - {Fore.CYAN + "link: " + list(ideas_json[sub_folder].values())[index]}")
            else:
                print(Fore.GREEN + f" {Fore.BLUE + ">>> " + str(index + 1)} - {Fore.GREEN + idea} - {Fore.CYAN + "link: wasn't provided"}")

# run the file as a python binary not as typer's
if __name__ == "__main__":
    app()