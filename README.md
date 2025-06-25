# PyIdea
a CLI tool to organize your ideas where you can write headers to your ideas
and then add a link to a markdown file for more detail

---

## Table of contents:
- [General Use](#general-use)
    - [add idea](#add-idea)
    - [list label](#list-label)
    - [remove idea](#remove-idea)
    - [remove label](#remove-label)
- [Setup](#setup)

---

## General Use:
to add an idea use the `add-idea` sub-command use the `--link` optioin to add a link
to an existing markdown file '(.md)' if its anything else it won't be accepted

list them through `list-label`

remove an idea through `remove-idea` sub-command it takes two parameters the label (sub-folder)
and the index (one indexed) to remove it

remove a full label through `remove-label` which takes only the label (sub-folder) to remove 

***NOTE:*** *the labels will only be saved in all caps even if you enter them in lowercase because its cool*

---

## add idea:
use `add-idea` option add teh label then then the header to the idea like

`pyidea add-idea <label> <idea-header>`

***NOTE:*** *the project will be saved as fully uppercase even if you enter it as lowercase*

you can use the `--link` option to add a *link to an existing markdown file you have* example:

`pyidea add-idea <label> <idea-header> --link </full/path/to/file.md>`

***NOTE:*** *the file you link must be a markdown file*

---

## list label:
use `list-label` to list them they will be printed like this

---

## remove idea:
use this to remove a single idea you write it like this

`pyidea remove-idea <label> <idea-one-indexed>`

this will remove the idea you want to remove in that label

***NOTE:*** *if a label has nothing left in it it will be removed as well*

---

## remove label:
use this to remove a full label and its contents write it like this

`pyidea remove-label <label>`

this will remove an entire label and its contents as said

---

## setup:
*will write it once I figure it out hehe*