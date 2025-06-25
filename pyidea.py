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
    with open("/usr/local/bin/Pyidea/Data/idea.json", mode="r", encoding="utf-8") as read_file:
        return load(read_file)

# writing to the json file containing the ideas and their destinations    
def write_json(dict_to_json):
    with open("/usr/local/bin/Pyidea/Data/idea.json", mode="w", encoding="utf-8") as write_file:
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
def add_idea(label: str, idea: str, link: str = ""):
    ideas_json: dict = read_json()
    check_if_exists(label, ideas_json) # we always run this to always check for if links are missed

    # by splitting the values on whitespace doesn't allow the user to enter a bunch of spaces 
    # which would work if we compared it to an empty string since a whitespace spammed one isn't considered empty
    if len(idea.split()) == 0 or len(label.split()) == 0:
        print(Fore.RED + "The idea or sub-folder is empty")
        return
    else:
        for folder in ideas_json.keys():
            # checking if the idea exists withing the sub-folder the is selected by comparing the subfolder and checking if its value
            # exists withing the sub-folder the same for the link
            if label.upper() == folder and idea in ideas_json[folder].keys() or link in ideas_json[folder].values() and link != "":
                print(Fore.RED + "idea/link already exists")
                return

    # we chceck if its a file and if it is a markdown file
    if not os.path.isfile(link) and link != "":
        print(Fore.RED + f"{link} doesn't exist or is a directory")
        return 
    elif  pathlib.Path(link).suffix != ".md" and link != "":
        print(Fore.RED + f"{link} must be in markdown")
        return 

    # if there is a sub-folder and the user chose it we update it if not we create it
    if label.upper() in ideas_json.keys():
        ideas_json[label.upper()].update({ idea: link }) # we make the sub-folder uppercase don't ask me why its fun
        print(Fore.GREEN + "the idea was added")
    else:
        ideas_json.update({ label.upper(): { idea: link } })
        print(Fore.GREEN + "the idea and the sub-folder were added")

    write_json(ideas_json)

@app.command()
def list_labels():
    ideas_json: dict = read_json()
    labels = list(ideas_json.keys()) 

    if len(labels) == 0:
        print(Fore.RED + "There are no ideas yet to list use the 'add-idea' command to add an idea")
        return
    
    for label in labels:
        check_if_exists(label, ideas_json) 
        ideas = list(ideas_json[label].keys()) 
        print(Fore.BLACK + label + ":") 
        for index, idea in enumerate(ideas):
            # we are getting the values (links) for each sub-folder and checking if its empty if it is 
            # we print something else other than it
            if list(ideas_json[label].values())[index] != "":
                print(Fore.GREEN + f" {Fore.BLUE + ">>> " + str(index + 1)} - {Fore.GREEN + idea} - {Fore.CYAN + "link: " + list(ideas_json[label].values())[index]}")
            else:
                print(Fore.GREEN + f" {Fore.BLUE + ">>> " + str(index + 1)} - {Fore.GREEN + idea} - {Fore.CYAN + "link: wasn't provided"}")

@app.command()
def remove_idea(label_name: str, idea_index: int):
    ideas_json: dict = read_json()
    labels = list(ideas_json.keys())

    if len(labels) == 0:
        print(Fore.RED + "There are no ideas yet to list use the 'add-idea' command to add an idea")
        return

    for label in labels:
        check_if_exists(label, ideas_json)
    
    # for each folder we take its keys (ideas)
    for label in labels:
        ideas = list(ideas_json[label].keys())
        if label_name.upper() == label:
            for index, idea in enumerate(ideas):
                if idea_index - 1 == index: # we subract one because the value entered will be one indexed
                    print(Fore.GREEN + f"{idea} is removed")
                    ideas_json[label].pop(idea)
                    # we check if there is no ideas left then we will remove the sub-folder because it is empty
                    if len(list(ideas_json[label].keys())) == 0: 
                        print(Fore.GREEN + f"{label} is removed")
                        ideas_json.pop(label)
                        
                    write_json(ideas_json)
                    return
                # we then redo the loop because if we don't we could only remove the first one 
                # because the first loop already ended so it won't repeat without putting this line
                else:
                    continue

            print(Fore.RED + "the index you entered doesn't exist")
            return    
    print(Fore.RED + "the folder name you entered doesn't exist")
    return

@app.command()
def remove_label(label_name: str):
    ideas_json = read_json()
    labels = ideas_json.keys()

    if len(labels) == 0:
        print(Fore.RED + "There are no ideas yet to list use the 'add-idea' command to add an idea")
        return

    for label in labels:
        if label_name.upper() == label:
            print(Fore.GREEN + f"removed {label}")
            ideas_json.pop(label)
            write_json(ideas_json)
            return
    
    print(Fore.RED + "the label doesn't exist")

# run the file as a python binary not as typer's
if __name__ == "__main__":
    app()