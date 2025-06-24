from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from json import dump, load

def read_json():
    with open("Data/idea.json", mode="r", encoding="utf-8") as read_file:
        return load(read_file)
    
def write_json(dict_to_json):
    with open("Data/idea.json", mode="w", encoding="utf-8") as write_file:
        return dump(dict_to_json, write_file, indent=4)

class Pyidea(App):
    
    BINDINGS = [("a", "add_idea", "Add an idea")]

    def compose(self):
        yield Header
        yield Footer
        

if __name__ == "__main__":
    app = Pyidea()
    app.run()