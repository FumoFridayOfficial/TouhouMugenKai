import os,json,hashlib, re,subprocess,easygui,requests,io,configparser, time, psutil, threading, webbrowser,sys

from datetime import datetime
from datetime import timedelta
from dearpygui import dearpygui as dpg
from GamesInfo import TouhouGames
from PIL import Image
from pathlib import Path
from os import listdir
from os.path import isfile, join
import DearPyGui_Markdown as dpg_markdown

CURRENTBUILD = ["1.0.0","Beta","05/25/2023"]

dpg.create_context()
dpg.create_viewport(title=f'Touhou Mugen-kai: {CURRENTBUILD[1]} {CURRENTBUILD[0]}', width=930, height=700,resizable=False)
ViewPortWidth = dpg.get_viewport_width()
ViewPortHeight = dpg.get_viewport_height()
OfficialTouhouGames = ["Touhou 1 - Highly Responsive to Prayers","Touhou 2 - Story of Eastern Wonderland","Touhou 3 - Phantasmagoria of Dimensional Dream","Touhou 4 - Lotus Land Story","Touhou 5 - Mystic Square","Touhou 6 - Embodiment of Scarlet Devil","Touhou 7 - Perfect Cherry Blossom","Touhou 7.5 - Immaterial and Missing Power","Touhou 8 - Imperishable Night","Touhou 9 - Phantasmagoria of Flower View","Touhou 9.5 - Shoot the Bullet","Touhou 10 - Mountain of Faith","Touhou 10.5 - Scarlet Weather Rhapsody","Touhou 11 - Subterranean Animism","Touhou 12 - Undefined Fantastic Object","Touhou 12.3 - Hisoutensoku","Touhou 12.5 - Double Spoiler","Touhou 12.8 - Fairy Wars","Touhou 13 - Ten Desires","Touhou 13.5 - Hopeless Masquerade","Touhou 14 - Double Dealing Character","Touhou 14.3 - Impossible Spell Card","Touhou 14.5 - Urban Legend in Limbo","Touhou 15 - Legacy of Lunatic Kingdom","Touhou 15.5 - Antinomy of Common Flowers","Touhou 16 - Hidden Star in Four Seasons","Touhou 16.5 - Violet Detector","Touhou 17 - Wily Beast and Weakest Creature","Touhou 17.5 - Sunken Fossil World","Touhou 18 - Unconnected Marketeers","Touhou 18.5 - 100th Black Market"]
CurrentDirectory = str(os.path.dirname(__file__)) # TEMP FOLDER
if getattr(sys, 'frozen', False):
    executable_dir = os.path.dirname(sys.executable) # EXECUTABLE RELATIVE FOLDER
    LibrariesDirectory = executable_dir+"\\Libraries\\"
else:
    LibrariesDirectory = CurrentDirectory+"\\Libraries\\"
    executable_dir = CurrentDirectory
default_font_path = f'{CurrentDirectory}\\rounded-mgenplus-2cp-regular.ttf'
bold_font_path = f'{CurrentDirectory}\\fonts\\InterTight-Bold.ttf'
italic_font_path = f'{CurrentDirectory}\\fonts\\InterTight-Italic.ttf'
italic_bold_font_path = f'{CurrentDirectory}\\fonts\\InterTight-BoldItalic.ttf'
SelectedPatch = None

os.chdir(executable_dir)

dpg_markdown.set_font_registry(dpg.add_font_registry())
dpg_font = dpg_markdown.set_font(
    font_size=17,
    default=default_font_path,
    bold=bold_font_path,
    italic=italic_font_path,
    italic_bold=italic_bold_font_path
)
dpg.bind_font(dpg_font)
dpg.add_font_range_hint(dpg.mvFontRangeHint_Default,parent=dpg_font)
dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese,parent=dpg_font)
dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full,parent=dpg_font)
dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common,parent=dpg_font)


class Game: #   The unpatched file will be usually the .exe to start the game, if the games has a patched file(for official th games they provide an english patched version) then it will be True and it will take that patched file too.
    """
    A Class Game object to create new games with it's title,folder path and .exe, more info can be attributed.

    Attributes:
    - title (str): the title of the game(Requiered).
    - installed (bool): whether the game is currently installed on the system(Requiered).
    - unpatched_file (str)|Also know as file .exe path: the path to the game.exe file before being patched(Requiered).
    - ---Everything below is optional---
    - patched (bool): whether the game has been patched with updates(if it has thcrap).
    - patched_file (str): the path to the game.exe file after being patched(if applicable).
    - desc (str): a brief description of the game(Optional).
    - developer (str): the name of the game's developer(Optional).
    - publisher (str): the name of the game's publisher(Optional).
    - released (str): the date when the game was released(Optional).
    - genre (str): the genre of the game (e.g. action, adventure, RPG, etc.)(Optional).
    - id (int): a unique identifier for the game(Optional).
    - cover (str): the path to the game's cover art image(Optional).
    - abbreviation (str): an abbreviation or acronym for the game's title(Optional).
    - number (int): the number of the game in a series (if applicable)(Optional).
    - character (str): the name of the main character in the game (if applicable)(Optional).
    """
    all_games = []
    def __init__(self, title, installed, unpatched_file,patched=False, patched_file=None,
                 desc=None, developer=None, publisher=None, released=None, genre=None, id=None, cover=None,
                 abbreviation=None, number=None, character=None):
        self.title = title
        self.installed = installed
        self.patched = patched
        self.unpatched_file = unpatched_file
        self.patched_file = patched_file
        self.desc = desc
        self.developer = developer
        self.publisher = publisher
        self.released = released
        self.genre = genre
        self.id = id
        self.cover = cover
        self.abbreviation = abbreviation
        self.number = number
        self.character = character
        self.path_valid = self.check_path_validity()
        Game.all_games.append(self)

    def get_unpatched_hash(self):
        # Compute hash of unpatched file
        pass
    
    def get_patched_hash(self):
        # Compute hash of patched file
        if not self.patched:
            return None
        
        sha256 = hashlib.sha256()
        with open(self.patched_file, "rb") as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def get_game_sha256(*self,library, title):
        try:
            for game in library.games:
                if game.title == title:
                    sha256 = hashlib.sha256()
                    with open(game.unpatched_file, "rb") as f:
                        while True:
                            data = f.read(65536)
                            if not data:
                                break
                            sha256.update(data)
                    return sha256.hexdigest()
        except:return None

    def check_path_validity(self):
        if self.unpatched_file is None or self.unpatched_file == "None":
            return False
        else:
            return os.path.exists(self.unpatched_file)

    def __str__(self):
        return f"Title: {self.title}\nInstalled: {self.installed}\nPatched: {self.patched}\nUnpatched file: {self.unpatched_file}\nPatched file: {self.patched_file}\nDescription: {self.desc}\nDeveloper: {self.developer}\nPublisher: {self.publisher}\nReleased: {self.released}\nGenre: {self.genre}\nID: {self.id}\nCover: {self.cover}\nAbbreviation: {self.abbreviation}\nNumber: {self.number}\nCharacter: {self.character}\nValid path: {self.path_valid}"

# Class library
# We create a new library like this LibraryName1 = Library('Library test 1')
class Library:
    """
    A Class Library object to create new libraries which has a name and a list of games, games can be added later to each library.
    It provides methods to add and remove games, as well as a method to load a library from a JSON file and save a library to a JSON file.

    Attributes:
    - name (str): the name of the library(Requiered).
    """
    def __init__(self, name):
        """ It provides methods to add and remove games, as well as a method to load a library from a JSON file and save a library to a JSON file.

        Attributes:
        - name (str): the name of the library(Requiered)."""
        self.name = name
        self.games = []
    
    def add_game(self, game):
        """ Adds a game object to the library."""
        self.games.append(game)
    
    def remove_game(self, game):
        """Removes a game object from the library."""
        if game in self.games:
            self.games.remove(game)
        else:
            print("Game not found in library.")
    
    def __len__(self):
        """Return the number of games in the library."""
        return len(self.games)

    def load(self, filename): # This may not be used as much.
        """Load a library from a JSON file."""
        with open(filename, 'r') as file:
            data = json.load(file)
        self.name = data['Library']
        self.games = [Game(**game_data) for game_data in data['games']]
        pass
    
    def save(self, filename):
        """Save the library to a JSON file."""
        with open(filename,'w'):
            LibraryData = {
                'Library': self.name,
                'games': [game.__dict__ for game in self.games]
            }
            with open(filename, 'w') as file:
                json.dump(LibraryData, file, indent=4)
        pass

    def get_file_path(self):
        """Returns the file path of the JSON file for the library."""
        # Assuming the library name is unique and can be used in the file name
        # Essentially, it will read only .json files from "Libraries" folder.
        file_name = f"{self.name}.json"
        file_path = os.path.join(executable_dir+"\\Libraries", file_name)
        return file_path

    def list_games(self):
        """Returns a list of all games in the library."""
        return [game.title for game in self.games]

    def list_int_games(self):
        """Returns a int of all games in the library."""
        for i,game in enumerate(self.games):
            i = i + 1
        return i -1

class LibraryManager:
    """ This class creates a LibraryManager, which is responsible for managing a list of libraries.
        It contains methods for adding/removing libraries, saving/loading libraries to/from a file, editing a library's name, listing the libraries, and searching for a library. """

    def __init__(self):
        """Initializes the LibraryManager object and creates an empty list of libraries."""
        self.libraries = []

    def add_library(self, library):
        """Adds a library to the list of libraries managed by the LibraryManager."""
        self.libraries.append(library)

    def remove_library(self, library):
        """Removes a library from the list of libraries managed by the LibraryManager."""
        self.libraries.remove(library)

    def save_libraries(self, filename):
        """Saves the list of libraries managed by the LibraryManager to a file."""
        data = {"libraries": [{"name": library.name, "games": [{"title": game.title, "installed": game.installed, "unpatched_file": game.unpatched_file, "patched": game.patched, "patched_file": game.patched_file, "desc": game.desc, "developer": game.developer, "publisher": game.publisher, "released": game.released, "genre": game.genre, "id": game.id, "cover": game.cover, "abbreviation": game.abbreviation, "number": game.number, "character": game.character} for game in library.games]} for library in self.libraries]}
        with open(filename, "w") as file:
            json.dump(data, file,indent=4)

    def edit_library(self,index,name):
        """Edits the name of the library at the given index."""
        self.libraries[index].name = name
        return self.libraries[index]

    def load_libraries(self, filename):
        """Loads the list of libraries managed by the LibraryManager from a file."""
        with open(filename, "r") as file:
            data = json.load(file)
        for library_data in data["libraries"]:
            library = Library(library_data["name"])
            library.games = [Game(game_name,installed=False, unpatched_file=None) for game_name in library_data["games"]]
            self.libraries.append(library)

    def list_libraries(self):
        """Creates a list of libraries managed by the LibraryManager.\nTo access the name of the library use <Library>.name"""
        LibraryList = []
        for library in self.libraries:
            LibraryList.append(library)
        return LibraryList
    
    def print_libraries(self):
        """Prints the list of libraries managed by the LibraryManager."""
        for library in self.libraries:
            print(library.name)

    def remove_duplicate_libraries(self):
        """Remove duplicate library instances from the LibraryManager's libraries list, using each library's 'name' attribute as the unique identifier."""
        unique_libraries = {}
        for library in self.libraries:
            unique_libraries[library.name] = library
        self.libraries = list(unique_libraries.values())

    def order_libraries_by_name(self):
        """Orders the list of libraries managed by the manager in alphabetical order by name."""
        self.libraries = sorted(self.libraries, key=lambda x: x.name)

    def search_libraries(self, name):
        """Searches for a library with the given name and returns the library object and its index in the list of libraries."""
        libraryIndex = -1
        for library in self.libraries:
            libraryIndex += 1
            if library.name == name:
                return library, libraryIndex

    def update_game_info_all_libraries(self, game_title, **kwargs):
        """Update the information of a game across all libraries by its title.

        Args:
        - game_title (str): The title of the game to be updated.
        - **kwargs: Keyword arguments representing the updated information of the game.
        The keyword should match the attribute name of the game, and the value should be the new value for that attribute.
        """
        for library in self.libraries:
            for game in library.games:
                if game.title == game_title:
                    for key, value in kwargs.items():
                        setattr(game, key, value)

                    # Update the JSON file with the modified game information
                    library_file_path = library.get_file_path()
                    with open(library_file_path, 'r') as file:
                        library_data = json.load(file)

                    for game_data in library_data['games']:
                        if game_data['title'] == game_title:
                            game_data.update(kwargs)

                    with open(library_file_path, 'w') as file:
                        json.dump(library_data, file, indent=4)

# CONFIG INI FILES TO LOAD
configINI = configparser.ConfigParser()

if getattr(sys, 'frozen', False):
    print("Running as an executable (.exe)")
    configINI.read(os.path.join(executable_dir, "LauncherConfig.ini"))
else:
    print("Running as a .py script")
    configINI.read(os.path.join(CurrentDirectory, "LauncherConfig.ini"))

EmulatorPath = configINI['EmulatorFolderPath']['path']
EmulatorConfigINI = configparser.ConfigParser()
EmulatorConfigINI.read(str(EmulatorPath)+'\\np21nt.ini',encoding='utf-8')

DisclaimerAcceptedINI = configINI['Disclaimer']['Accepted']

def validate_library(library_data):
    if "Library" not in library_data:
        return False
    if "games" not in library_data:
        return False
    for game_data in library_data["games"]:
        if "title" not in game_data:
            return False
        if "installed" not in game_data:
            return False
        if "unpatched_file" not in game_data:
            return False
        if "desc" not in game_data:
            return False
        if "developer" not in game_data:
            return False
        if "publisher" not in game_data:
            return False
        if "released" not in game_data:
            return False
        if "genre" not in game_data:
            return False
        if "id" not in game_data:
            return False
    return True

# Initialize the library manager and add libraries to it's manager
manager = LibraryManager()

Temporal_Library = Library("Temporal Library")
manager.add_library(Temporal_Library)

def print_games(library):
    print(f"\n----------------------------\nGames in {library.name}:")
    for game in library.games:
        print(game.title)

def print_games_detailed(self):
    for game in self.games:
        print("Title:", game.title)
        print("Installed:", game.installed)
        print("Patched:", game.patched)
        print("Unpatched file:", game.unpatched_file)
        print("Patched file:", game.patched_file)
        print("Description:", game.desc)
        print("Developer:", game.developer)
        print("Publisher:", game.publisher)
        print("Release date:", game.released)
        print("Genre:", game.genre)
        print("ID:", game.id)
        print("Cover:", game.cover)
        print("Abbreviation:", game.abbreviation)
        print("Number:", game.number)
        print("Character:", game.character)
        print("\n")

# Iterate over each file in the directory
for filename in os.listdir(LibrariesDirectory):
    if filename.endswith(".json"):
        with open(os.path.join(LibrariesDirectory, filename), "r") as f:
            try:library_data = json.load(f)
            except json.decoder.JSONDecodeError as DecodeError:print(f"---------------\nCouldn't load file {f}, JSONDecodeError\nMost probably is not a valid library file\n{DecodeError}\n---------------\n")
            if validate_library(library_data):
                library = Library(library_data["Library"])
                for game_data in library_data["games"]:
                    game = Game(game_data["title"], game_data["installed"], game_data["unpatched_file"],
                                game_data["patched"], game_data["patched_file"], game_data["desc"],
                                game_data["developer"], game_data["publisher"], game_data["released"],
                                game_data["genre"],game_data["id"],None,
                                game_data["abbreviation"],game_data["number"],game_data["character"])
                    library.add_game(game)
                #print_games_detailed(library)
                manager.add_library(library)
            else:
                print(f"{filename} is not a valid library file.")

manager.remove_duplicate_libraries()

def help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[255, 255, 0])
    with dpg.tooltip(t):dpg.add_text(message,wrap=400)

def comment(message): #Dev comments inside the GUI
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(#)", color=[55, 200, 0])
    with dpg.tooltip(t):dpg.add_text(message)


def Log(Action):
    dpg.add_text(default_value="["+str(datetime.now())+"]"+" -> "+str(Action)+"\n",wrap=400,parent="StatusActions")
    with open(executable_dir+"\\LibraryLog.txt", "a", encoding='utf-8') as log_file:
        log_file.write("["+str(datetime.now())+"]"+" -> "+str(Action)+"\n")

def DisclaimerReaded(s,a,u):
    if u == True:
        dpg.configure_item(item="DisclaimerWindow",show=False)
        configINI['Disclaimer'] = {'Accepted': True}
        with open(executable_dir+'\LauncherConfig.ini', 'w') as configfile:configINI.write(configfile)
    elif u == False:
        dpg.configure_item(item="DisclaimerWindow",show=False)
        configINI['Disclaimer'] = {'Accepted': False}
        with open(executable_dir+'\LauncherConfig.ini', 'w') as configfile:configINI.write(configfile)
        dpg.stop_dearpygui()

def hyperlink(text, address):
    b = dpg.add_button(label=text, callback=lambda:webbrowser.open(address))
    dpg.bind_item_theme(b, "hyperlinkTheme")

def _hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h*6.) # assume int() truncates!
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return (255*v, 255*t, 255*p)
    if i == 1: return (255*q, 255*v, 255*p)
    if i == 2: return (255*p, 255*v, 255*t)
    if i == 3: return (255*p, 255*q, 255*v)
    if i == 4: return (255*t, 255*p, 255*v)
    if i == 5: return (255*v, 255*p, 255*q)

def _Clipboard(s,a,u):dpg.set_clipboard_text(u)

def AllGamesTitles():
    existing_games = list(set(game.title for game in Game.all_games))
    existing_games.sort()
    return existing_games

def GetGameOBJbyTitle(title):
    for game in Game.all_games:
        if game.title == title:
            return game

def openFolder(s,a,u):
    os.startfile(u)

def find_process_by_name(process_name, timeout=10):
    end_time = time.time() + timeout
    while time.time() < end_time:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                return proc.info['pid']
        time.sleep(1)
    return None

def find_process_by_pid(pid):
    process = psutil.Process(pid)
    return process.is_running() if process else None

with dpg.window(label="Log",tag="LogWindow",show=False,on_close=dpg.delete_item("LogWindow"),no_resize=False,pos=(100, 100), width=450,height=320):
    dpg.add_text("Status")
    dpg.add_separator()
    with dpg.group(tag="StatusActions"):pass

def FoundGamesInFoundLibrary(found_library,Parent):
    for n,found_game in enumerate(found_library.games):
        UserData = []
        UserData.append(found_game)
        UserData.append(found_library)
        UUID = dpg.generate_uuid()
        UserData.append(str(UUID))
        with dpg.tree_node(label=found_game.title,filter_key=f"{found_game.title},{found_game.genre},{found_library.name},{found_game.released},{found_game.publisher},{found_game.developer}"):
            with dpg.group(horizontal=True):dpg.add_text("Title:",filter_key=f"{found_game.title}"),dpg.add_input_text(tag="E1Title"+str(found_library)+str(UUID),readonly=True,default_value=found_game.title,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Library:"),dpg.add_input_text(tag="E1Library"+str(found_library)+str(UUID),readonly=True,default_value=found_library.name,width=-1)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Remove",user_data=UserData,callback=RemoveSpecificGame)
                dpg.add_button(label="Edit",user_data=UserData,callback=EditSpecificGame)
                dpg.add_button(label="Save",tag="SaveDataGame"+str(found_library)+str(UUID),user_data=UserData,callback=SaveEditSpecificGame,show=False)
                dpg.add_button(label="Cancel Edit",tag="CancelEditGame"+str(found_library)+str(UUID),user_data=UserData,callback=CancelEditSpecificGame,show=False)
            if found_game.installed == True:
                dpg.add_text(f"Installed: Yes",filter_key="I: Yes")
            elif found_game.installed == False:
                dpg.add_text(f"Installed: No",filter_key="I: No")
            if found_game.patched == True:
                dpg.add_text(f"Patched: Yes",filter_key="P: Yes")
            elif found_game.patched == False:
                dpg.add_text(f"Patched: No",filter_key="P: No")
            elif found_game.patched == None:
                dpg.add_text(f"Patched: No",filter_key="P: No ")
            with dpg.group(horizontal=True):dpg.add_text("Unpatched file:"),dpg.add_input_text(tag="E1Unpatchedfile"+str(found_library)+str(UUID),readonly=True,default_value=found_game.unpatched_file,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Patched file:"),dpg.add_input_text(tag="E1Patchedfile"+str(found_library)+str(UUID),readonly=True,default_value=found_game.patched_file,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Description:"),dpg.add_input_text(tag="E1Description"+str(found_library)+str(UUID),readonly=True,default_value=found_game.desc,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Developer:",filter_key=found_game.developer),dpg.add_input_text(tag="E1Developer"+str(found_library)+str(UUID),readonly=True,default_value=found_game.developer,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Publisher:",filter_key=found_game.publisher),dpg.add_input_text(tag="E1Publisher"+str(found_library)+str(UUID),readonly=True,default_value=found_game.publisher,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Released:",filter_key=found_game.released),dpg.add_input_text(tag="E1Released"+str(found_library)+str(UUID),readonly=True,default_value=found_game.released,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Genre:",filter_key=f"{found_game.genre}"),dpg.add_input_text(tag="E1Genre"+str(found_library)+str(UUID),readonly=True,default_value=found_game.genre,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Id:",filter_key=found_game.id),dpg.add_input_text(tag="E1Id"+str(found_library)+str(UUID),readonly=True,default_value=found_game.id,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Cover:"),dpg.add_input_text(tag="E1Cover"+str(found_library)+str(UUID),readonly=True,default_value=found_game.cover,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Abbreviation:",filter_key=found_game.abbreviation),dpg.add_input_text(tag="E1Abbreviation"+str(found_library)+str(UUID),readonly=True,default_value=found_game.abbreviation,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Number:"),dpg.add_input_text(tag="E1Number"+str(found_library)+str(UUID),readonly=True,default_value=found_game.number,width=-1)
            with dpg.group(horizontal=True):dpg.add_text("Character:"),dpg.add_input_text(tag="E1Character"+str(found_library)+str(UUID),readonly=True,default_value=found_game.character,width=-1)
            dpg.add_text("SHA-256 value from unpatched file:"),dpg.add_input_text(readonly=True,default_value=found_game.get_game_sha256(library=found_library,title=found_game.title),width=-1)

def CreateBackupLibraries(s,a,u):
    today = datetime.now()
    try:os.mkdir(executable_dir+"\\Libraries\\Backup\\Backup"+str(today.strftime('%Y-%m-%d')))
    except:pass
    for library in manager.list_libraries():
        if library.name == "Temporal Library":print("")
        else:
            found_library = (manager.search_libraries(library.name))[0]
            found_library.save(f"{executable_dir}\\libraries\\Backup\\Backup"+str(today.strftime('%Y-%m-%d'))+"\\"+f"{found_library.name}.json")
    refresh_libraries()
    Log(f"BackupCreated at {executable_dir}\\Libraries\\Backup\\Backup{str(today.strftime('%Y-%m-%d'))}")

def RemoveSelectedLibrary(s,a,u):
    print(u)
    try:dpg.delete_item("WarningPopup")
    except:pass
    if u == "Temporal Library":
        with dpg.window(label="Error",tag="ErrorPopup",pos=(int(dpg.get_viewport_width())/2, int(dpg.get_viewport_height())/2),on_close=True,no_resize=True,no_collapse=True,width=300,height=150):
            dpg.add_text("You can't modify nor save 'Temporal Libraly'")
            dpg.add_text(u,color=[255,0,0])
            dpg.add_text("Only change the games inside.")
            dpg.add_separator()
            dpg.add_button(label="Close",callback=lambda:dpg.delete_item("ErrorPopup"))
        dpg.bind_item_theme("ErrorPopup",Red_TitleBgActive)
    else:
        def Remove(s,a,u):
            found_library = (manager.search_libraries(u))[0]
            manager.remove_library(found_library)
            dpg.delete_item(found_library.name+"Tree")
            if os.path.exists(executable_dir+"\\Libraries\\"+found_library.name+".json"):
                os.remove(executable_dir+"\\Libraries\\"+found_library.name+".json")
            else:
                print("The file does not exist") 
            refresh_libraries()
            dpg.delete_item("WarningPopup")
            Log(f"{found_library.name} has been removed")

        with dpg.window(label="Warning",tag="WarningPopup",pos=(int(dpg.get_viewport_width())/3.5, int(dpg.get_viewport_height())/3),on_close=True,no_resize=True,no_collapse=True,width=450,height=150):
            dpg.add_text("Are you sure you want to delete library")
            dpg.add_text(u,color=[255,255,0])
            dpg.add_text("It will be deleted from your library folder.")
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Yes",user_data=u,callback=Remove)
                dpg.add_button(label="No",callback=lambda:dpg.delete_item("WarningPopup"))
        dpg.bind_item_theme("WarningPopup",Red_TitleBgActive)

def RemoveSpecificGame(s,a,u):
    print("\n\n",u[0],u[1])
    GameToRemove = u[0]
    LibraryFrom = u[1]
    Game.all_games.remove(GameToRemove)
    LibraryFrom.remove_game(GameToRemove)
    Log(f"Game {u[0].title} has been removed from library {u[1].name}")
    del GameToRemove
    refresh_libraries()

def EditSpecificGame(s,a,u):
    global OldTitle,OldUnpatchedFile,OldPatchedFile,OldDescription,OldDeveloper,OldPublisher,OldReleased,OldGenre,OldId,OldAbbreviation,OldNumberF,OldCharacter
    print("\n\n----------\nEditing:",u[0],u[1])
    GameToEdit = u[0]
    LibraryFrom = u[1]
    Number = u[2]

    dpg.configure_item(item="E1Title"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Unpatchedfile"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Patchedfile"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Description"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Developer"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Publisher"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Released"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Genre"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Id"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Abbreviation"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Number"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="E1Character"+str(LibraryFrom)+str(Number),readonly=False)
    dpg.configure_item(item="SaveDataGame"+str(LibraryFrom)+str(Number),show=True)
    dpg.configure_item(item="CancelEditGame"+str(LibraryFrom)+str(Number),show=True)

    OldTitle = dpg.get_value(item="E1Title"+str(LibraryFrom)+str(Number))
    OldUnpatchedFile = dpg.get_value(item="E1Unpatchedfile"+str(LibraryFrom)+str(Number))
    OldPatchedFile = dpg.get_value(item="E1Patchedfile"+str(LibraryFrom)+str(Number))
    OldDescription = dpg.get_value(item="E1Description"+str(LibraryFrom)+str(Number))
    OldDeveloper = dpg.get_value(item="E1Developer"+str(LibraryFrom)+str(Number))
    OldPublisher = dpg.get_value(item="E1Publisher"+str(LibraryFrom)+str(Number))
    OldReleased = dpg.get_value(item="E1Released"+str(LibraryFrom)+str(Number))
    OldGenre = dpg.get_value(item="E1Genre"+str(LibraryFrom)+str(Number))
    OldId = dpg.get_value(item="E1Id"+str(LibraryFrom)+str(Number))
    OldAbbreviation = dpg.get_value(item="E1Abbreviation"+str(LibraryFrom)+str(Number))
    OldNumberF = dpg.get_value(item="E1Number"+str(LibraryFrom)+str(Number))
    OldCharacter = dpg.get_value(item="E1Character"+str(LibraryFrom)+str(Number))

def CancelEditSpecificGame(s,a,u):
    GameToEdit = u[0]
    LibraryFrom = u[1]
    Number = u[2]
    GameToEditOld = u[0]

    dpg.set_value(item="E1Title"+str(LibraryFrom)+str(Number),value=OldTitle)
    dpg.set_value(item="E1Unpatchedfile"+str(LibraryFrom)+str(Number),value=OldUnpatchedFile)
    dpg.set_value(item="E1Patchedfile"+str(LibraryFrom)+str(Number),value=OldPatchedFile)
    dpg.set_value(item="E1Description"+str(LibraryFrom)+str(Number),value=OldDescription)
    dpg.set_value(item="E1Developer"+str(LibraryFrom)+str(Number),value=OldDeveloper)
    dpg.set_value(item="E1Publisher"+str(LibraryFrom)+str(Number),value=OldPublisher)
    dpg.set_value(item="E1Released"+str(LibraryFrom)+str(Number),value=OldReleased)
    dpg.set_value(item="E1Genre"+str(LibraryFrom)+str(Number),value=OldGenre)
    dpg.set_value(item="E1Id"+str(LibraryFrom)+str(Number),value=OldId)
    dpg.set_value(item="E1Abbreviation"+str(LibraryFrom)+str(Number),value=OldAbbreviation)
    dpg.set_value(item="E1Number"+str(LibraryFrom)+str(Number),value=OldNumberF)
    dpg.set_value(item="E1Character"+str(LibraryFrom)+str(Number),value=OldCharacter)

    dpg.configure_item(item="E1Title"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Unpatchedfile"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Patchedfile"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Description"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Developer"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Publisher"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Released"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Genre"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Id"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Abbreviation"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Number"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Character"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="SaveDataGame"+str(LibraryFrom)+str(Number),show=False)
    dpg.configure_item(item="CancelEditGame"+str(LibraryFrom)+str(Number),show=False)

def SaveEditSpecificGame(s,a,u):
    GameToEdit = u[0]
    LibraryFrom = u[1]
    Number = u[2]
    GameToEditOld = u[0]

    Title = dpg.get_value(item="E1Title"+str(LibraryFrom)+str(Number))
    UnpatchedFile = dpg.get_value(item="E1Unpatchedfile"+str(LibraryFrom)+str(Number))
    PatchedFile = dpg.get_value(item="E1Patchedfile"+str(LibraryFrom)+str(Number))
    Description = dpg.get_value(item="E1Description"+str(LibraryFrom)+str(Number))
    Developer = dpg.get_value(item="E1Developer"+str(LibraryFrom)+str(Number))
    Publisher = dpg.get_value(item="E1Publisher"+str(LibraryFrom)+str(Number))
    Released = dpg.get_value(item="E1Released"+str(LibraryFrom)+str(Number))
    Genre = dpg.get_value(item="E1Genre"+str(LibraryFrom)+str(Number))
    Id = dpg.get_value(item="E1Id"+str(LibraryFrom)+str(Number))
    Abbreviation = dpg.get_value(item="E1Abbreviation"+str(LibraryFrom)+str(Number))
    NumberF = dpg.get_value(item="E1Number"+str(LibraryFrom)+str(Number))
    Character = dpg.get_value(item="E1Character"+str(LibraryFrom)+str(Number))

    GameToEdit.title = Title
    GameToEdit.unpatched_file = UnpatchedFile
    GameToEdit.patched_file = PatchedFile
    GameToEdit.desc = Description
    GameToEdit.developer = Developer
    GameToEdit.publisher = Publisher
    GameToEdit.released = Released
    GameToEdit.genre = Genre
    GameToEdit.id = Id
    GameToEdit.abbreviation = Abbreviation
    GameToEdit.number = NumberF
    GameToEdit.character = Character

    dpg.configure_item(item="E1Title"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Unpatchedfile"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Patchedfile"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Description"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Developer"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Publisher"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Released"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Genre"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Id"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Abbreviation"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Number"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="E1Character"+str(LibraryFrom)+str(Number),readonly=True)
    dpg.configure_item(item="SaveDataGame"+str(LibraryFrom)+str(Number),show=False)
    dpg.configure_item(item="CancelEditGame"+str(LibraryFrom)+str(Number),show=False)

    refresh_libraries()
    Log(f"Game {OldTitle} has been changed with new values.\nValuesChanged\nOld title -> {OldTitle} <- New title -> {GameToEdit.title}"+
        f"\nOld Unpatched File -> {OldUnpatchedFile} <- New Unpatched File -> {GameToEdit.unpatched_file}"+
        f"\nOld Patched File -> {OldPatchedFile} <- New Patched File -> {GameToEdit.patched_file}"+
        f"\nOld Description -> {OldDescription} <- New Description -> {GameToEdit.desc}"+
        f"\nOld developer -> {OldDeveloper} <- New Developer -> {GameToEdit.developer}"+
        f"\nOld publisher -> {OldPublisher} <- New publisher -> {GameToEdit.publisher}"+
        f"\nOld released -> {OldReleased} <- New released -> {GameToEdit.released}"+
        f"\nOld genre -> {OldGenre} <- New genre -> {GameToEdit.genre}"+
        f"\nOld id -> {OldId} <- New id -> {GameToEdit.id}"+
        f"\nOld abbreviation -> {OldAbbreviation} <- New abbreviation -> {GameToEdit.abbreviation}"+
        f"\nOld number -> {OldNumberF} <- New number -> {GameToEdit.number}"+
        f"\nOld character -> {OldCharacter} <- New character -> {GameToEdit.character}")

def EditSelectedLibrary(s,a,u):
    print("Editing library:",u)
    EditingLibrary = (manager.search_libraries(u))[0]
    try:dpg.delete_item("EditPopup")
    except:pass

    def ChangeLibraryName(s,a,u):
        if u == "Temporal Library":
            with dpg.window(label="Error",tag="ErrorPopup",pos=(int(dpg.get_viewport_width())/2, int(dpg.get_viewport_height())/2),on_close=True,no_resize=True,no_collapse=True,width=300,height=150):
                dpg.add_text("You can't modify nor save 'Temporal Libraly'")
                dpg.add_text(u,color=[255,0,0])
                dpg.add_text("Only change it games inside.")
                dpg.add_separator()
                dpg.add_button(label="Close",callback=lambda:dpg.delete_item("ErrorPopup"))
            dpg.bind_item_theme("ErrorPopup",Red_TitleBgActive)
        else:
            newname = dpg.get_value("ChangeLibraryNameInput")
            print("New name: ",dpg.get_value("ChangeLibraryNameInput"))
            found_library_index = (manager.search_libraries(u))[1]
            manager.edit_library(found_library_index,dpg.get_value("ChangeLibraryNameInput"))
            os.rename(executable_dir+"\\libraries\\"+u+".json", executable_dir+"\\libraries\\"+newname+".json")
            refresh_libraries()
            dpg.delete_item("EditPopup")
            Log(f"Library called '{u}' changed name to '{newname}'")

    def AddorRemoveGameFromLibrary(s,a,u):
        print(s,a,u)
        Game = u[0]
        GameLibrary = u[1]
        for game in EditingLibrary.games:
            print("game.title:",game.title,"\nEditingLibrary:",EditingLibrary.name)
            if game.title == Game.title:
                Game = game
            else:print("Not the same")
        print("-------------\n////GameLibrary\n",EditingLibrary.name,"\n////GameTitle\n",Game.title+"\n")
        if a == "True" or a == True:
            EditingLibrary.add_game(Game)
            Log(f"Game '{Game.title}' has been added to '{EditingLibrary.name}'")
        else:
            EditingLibrary.remove_game(Game)
            Log(f"Game '{Game.title}' has removed from '{EditingLibrary.name}'")

    def ExitPopup():
        dpg.delete_item("EditPopup")
        refresh_libraries()

    with dpg.window(label="Editing",tag="EditPopup",pos=(int(dpg.get_viewport_width())/2, 40),no_close=True,no_resize=False,no_collapse=True,width=450,height=430):
        dpg.add_text("You can change the name of the library and the games it has.")
        with dpg.group(horizontal=True):
            dpg.add_text("Editing: ")
            dpg.add_text(u,color=[255,255,0])
        with dpg.group(horizontal=True):
            dpg.add_text("Change name: ")
            dpg.add_input_text(default_value=u,tag="ChangeLibraryNameInput")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Save name",user_data=u,callback=ChangeLibraryName)
            dpg.add_button(label="Exit",width=70,callback=ExitPopup)
        dpg.add_separator()
        dpg.add_text("Change library contents")

        with dpg.table(header_row=True, row_background=True,
                    borders_innerH=True, borders_outerH=True, borders_innerV=True,
                    borders_outerV=True, delay_search=True):

            dpg.add_table_column(label="Game title")
            dpg.add_table_column(label="Is game in library?",width=100,width_stretch=False,width_fixed=True)

            existing_games = set()

            for library in manager.list_libraries():
                GamesList = EditingLibrary.list_games()
                for game in library.games:
                    # Check if the game title has already been added
                    if game.title not in existing_games:
                        GameTitleandLibrary = []
                        GameTitleandLibrary.append(game)
                        GameTitleandLibrary.append(library.name)
                        if game.title in GamesList:
                            with dpg.table_row():
                                dpg.add_text(game.title)
                                with dpg.tooltip(dpg.last_item()):
                                    dpg.add_text(f"GAME INFO:\n------------\n{game}")
                                dpg.add_checkbox(default_value=True,user_data=GameTitleandLibrary,callback=AddorRemoveGameFromLibrary)
                        else:
                            with dpg.table_row():
                                dpg.add_text(game.title)
                                with dpg.tooltip(dpg.last_item()):
                                    dpg.add_text(f"GAME INFO:\n------------\n{game}")
                                dpg.add_checkbox(default_value=False,user_data=GameTitleandLibrary,callback=AddorRemoveGameFromLibrary)

                        existing_games.add(game.title)

def EditSingleLibrary(s,a,u):
    print("a: ",a)
    try:dpg.delete_item("SingleLibraryGroup")
    except:pass
    with dpg.group(tag="SingleLibraryGroup",parent="SingleLibraryTab"):
        found_library = (manager.search_libraries(a))[0]
        with dpg.tree_node(label=found_library.name,tag=found_library.name+"Tree"):
            Parent = dpg.last_item()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Remove",user_data=found_library.name,callback=RemoveSelectedLibrary)
                dpg.add_button(label="Edit",user_data=found_library.name,callback=EditSelectedLibrary)
            dpg.add_text(default_value="Amount of games: "+str(found_library.__len__()),parent=dpg.last_item())
            FoundGamesInFoundLibrary(found_library,Parent)
############################
def ChangeGamePath(s,a,u):
    DLPath = easygui.fileopenbox(msg='Please locate the UNPATCHED exe file',
                    title='Specify Exe File', default='c:\touhou\...\*.exe',
                    filetypes='*.exe')
    print(DLPath)
    filePath = DLPath
    dpg.set_value(item="GamePath",value=filePath)
    if os.path.exists(filePath):
        dpg.set_value(item="IsPathValid",value="Path exists!")
        dpg.configure_item(item="IsPathValid",tag="IsPathValid",color=(0,255,0))
        Log(f"Game {u} has change it's unpatched_file path from {SelectedGameOBJ.unpatched_file} to {filePath}")
        manager.update_game_info_all_libraries(game_title=u,unpatched_file=filePath,installed=True)
        refresh_libraries()
        return True
    dpg.set_value(item="IsPathValid",value="Invalid path!")
    dpg.configure_item(item="IsPathValid",tag="IsPathValid",color=(255,0,0))
    return False

def PathChanger(s,a,u):
    pathEXE = easygui.fileopenbox(msg='Please locate the UNPATCHED exe file',
                    title='Specify Exe File', default='c:\touhou\...\*.exe',
                    filetypes='*.exe')
    a = pathEXE
    PathValidator(s,a,u)

def PathValidator(s,a,u):
    g = u
    if os.path.exists(a):
        dpg.set_value(item=f"PathValidatorStatus{g}",value="Path exists!")
        dpg.configure_item(item=f"PathValidatorStatus{g}",color=(0,255,0))
        dpg.set_value(item=f"InputPath{g}",value=a)
        return True
    else:
        dpg.set_value(item=f"PathValidatorStatus{g}",value="Invalid path!")
        dpg.configure_item(item=f"PathValidatorStatus{g}",color=(255,0,0))
        return False

def SearchTouhouGamesInFolder():
    all_games = []

    official_games_pattern = r"(?:[Tt]ouhou)?[Tt]?[Hh]?[0-9][0-9][0-9]?([(]+?(thpatch_en)?[)]+?)?.exe|game.exe"
    patched_games_pattern = r"(?:Touhou)[0-9][0-9][0-9]?([(]+?(thpatch_en)?[)]+?)?.exe|[Tt][Hh][0-9][0-9][0-9]?\s?([(]+?(thpatch_en)?[)]+?).exe|[Tt][Hh][0-9][0-9][e].exe"
    pc98_games_pattern = r"[Tt][Hh]?[0-9][0-9].hdi"

    for game_title in OfficialTouhouGames:
        print("Searching for:", game_title)
        game_directory = os.path.join(dpg.get_value("InputPath9999"), game_title)
        is_installed = os.path.isdir(game_directory)

        game = {
            "game_title": game_title,
            "file_path": None,
            "patched_file_path": None,
            "is_patched": False,
            "is_installed": is_installed,
            "game_directory": game_directory
        }

        if is_installed:
            files = os.listdir(game_directory)

            # Look for patched versions
            for file in files:
                if re.match(patched_games_pattern, file):
                    game["patched_file_path"] = os.path.join(game_directory, file)
                    game["is_patched"] = True
                    break

            # Look for unpatched versions
            for file in files:
                if re.match(official_games_pattern, file):
                    game["file_path"] = os.path.join(game_directory, file)
                    break

            # Look for PC98 games
            for file in files:
                if re.match(pc98_games_pattern, file):
                    game["file_path"] = os.path.join(game_directory, file)
                    break

            all_games.append(game)
        else:
            game = {
                "game_title": game_title,
                "file_path": None,
                "patched_file_path": None,
                "is_patched": False,
                "is_installed": False,
                "game_directory": None
            }
            all_games.append(game)
    installedG = 0
    InstalledGames = []
    for game in all_games:
        print("Game title:", game["game_title"])
        print("File path:", game["file_path"])
        print("Patched File path:", game["patched_file_path"])
        print("Patched:", game["is_patched"])
        print("Installed:", game["is_installed"])
        print("Game directory:", game["game_directory"])
        print()
        with dpg.group(parent="OfficialGamesGroup"):
            dpg.add_separator()
            dpg.add_text("Title: "+game["game_title"])
            if game["file_path"] == None:dpg.add_text("Unpatched file path: NOT FOUND",color=[255,0,0])
            else:
                installedG = installedG + 1
                InstalledGames.append(game)
                dpg.set_value(item="InstalledTHGamesFound",value=f"Installed Touhou games found: {installedG}")
                dpg.add_text("Unpatched file path: "+str(game["file_path"]),color=[0,255,0])
            if game["patched_file_path"] == None:dpg.add_text("Patched file path: NOT FOUND",color=[255,0,0])
            else:dpg.add_text("Patched file path: "+str(game["patched_file_path"]),color=[0,255,0])
            dpg.add_text("Is it Installed?: "+str(game["is_installed"]))
            dpg.add_text("Is it patched?: "+str(game["is_patched"]))
            if game["game_directory"] == None:dpg.add_text("Game directory: NOT FOUND",color=[255,0,0])
            else:dpg.add_text("Game directory: "+str(game["game_directory"]),color=[0,255,0])
    dpg.add_button(parent="SaveInfoGames",label="Save path file to launcher.",user_data=InstalledGames,callback=SaveTouhouGamesPaths)
    dpg.add_text(default_value="this action cannot be undone, once saved it will read from the 'libraries' folder.",parent="SaveInfoGames")

def ListAllLibraries():
    dpg.delete_item("ListAllLibrariesGroup")
    with dpg.group(tag="ListAllLibrariesGroup",parent="AllLibrariesTab"):
        for library_name in manager.list_libraries():
            found_library = (manager.search_libraries(library_name.name))[0]
            with dpg.tree_node(label=found_library.name,tag=found_library.name):
                Parent = dpg.last_item()
                dpg.add_text("Games in library: "+str(found_library.__len__()))
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Save",user_data=found_library.name,callback=SaveSelectedLibrary)
                    dpg.add_button(label="Remove",user_data=found_library.name,callback=RemoveSelectedLibrary)
                    dpg.add_button(label="Edit",user_data=found_library.name,callback=EditSelectedLibrary)
                FoundGamesInFoundLibrary(found_library,Parent)

def ThcrapValidator():
    print("hi")
    #todo
    #Check installed patches
    #validate if thcrap is installed

def EmulatorSave(s,a,u):
    path = dpg.get_value("EmulatorFolderPath")
    if os.path.exists(path):
        try:configINI['EmulatorFolderPath'] = {'path': path}
        except:dpg.set_value("EmulatorPathStatus","A path hasn't been selected")
        else:
            with open(executable_dir+'\LauncherConfig.ini', 'w') as configfile:configINI.write(configfile)
            dpg.set_value("EmulatorPathStatus","Path has been saved")
    else:dpg.set_value("EmulatorPathStatus","This path doesn't exists")

def ListAllGames():
    dpg.delete_item("ListAllGamesGroup")
    with dpg.group(tag="ListAllGamesGroup",parent="AllGamesTab"):
        dpg.add_text("Games:")
        dpg.add_separator()
        dpg.add_text("Filter usage:\n"
                        "  \"\"               display all lines\n"
                        "  \"xxx\"         display lines containing \"xxx\"\n"
                        "  \"xxx,yyy\"  display lines containing \"xxx\" or \"yyy\"\n"
                        "  \"-xxx\"        hide lines containing \"xxx\"")

        dpg.add_input_text(label="Filter (include, -exclude)", callback=lambda s, a: dpg.set_value("TitleFilter", a))
        dpg.add_text("You can filter trough, 'Titles', 'Libraries', 'Genres','Developer','Publisher','date'")
        with dpg.filter_set(tag="TitleFilter"):
            for library in manager.list_libraries():
                dpg.add_text(library.name)
                dpg.add_separator()
                Parent = dpg.last_item()
                found_library = (manager.search_libraries(library.name))[0]
                FoundGamesInFoundLibrary(found_library,Parent)

def EditGameInfo():
    dpg.delete_item("EditGameInfoGroup")
    with dpg.group(tag="EditGameInfoGroup",parent="EditGameInfoTab"):
        dpg.add_text("Here you can edit a games info by itself.\nRemember that when you press SAVE all info will be saved across all libraries.\nThis is useful when you don't want to edit the same game on multiple libraries.")
        dpg.add_separator()
        dpg.add_combo(items=AllGamesTitles(),label="Select a game",callback=ChangeGameInfo)
        dpg.add_input_text(label="Game title",width=350,tag="ChangeGameTitle")
        dpg.add_separator()
        dpg.add_checkbox(label="Is it installed?",tag="ChangeGameInstalledCheckbox",callback=lambda sender,app_data: dpg.configure_item(item="ChangeGamePathInput",enabled=app_data))
        dpg.add_input_text(label="Game path folder",width=350,tag="ChangeGamePathInput")
        dpg.add_checkbox(label="Is the game patched?",tag="ChangeGamePatchedCheckbox",callback=lambda sender,app_data: dpg.configure_item(item="ChangeGamePatchedPathInput",enabled=app_data))
        dpg.add_input_text(label="Game patched path folder",width=350,tag="ChangeGamePatchedPathInput")
        dpg.add_separator()
        dpg.add_input_text(label="Description",multiline=True,tab_input=True,height=30,width=350,tag="ChangeGameDescriptionInput")
        dpg.add_input_text(label="Developer",width=350,tag="ChangeGameDeveloperInput")
        dpg.add_input_text(label="Publisher",width=350,tag="ChangeGamePublisherInput")
        dpg.add_input_text(label="Released",width=350,tag="ChangeGameReleasedInput")
        dpg.add_input_text(label="Genre",width=350,tag="ChangeGameGenreInput")
    #   NewGameCover = input("Cover art:")
        dpg.add_input_text(label="Abbreviation",width=350,tag="ChangeGameAbbreviationInput")
        dpg.add_button(label="Save changes",callback=SaveGameInfo)
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_text("Clear path of all games.")
            help("This will clear the path of ALL games inside all libraries\nHAVE A BACKUP BEFORE THIS!")
        dpg.add_button(label="Clear path of all games",callback=lambda:dpg.configure_item(item="ConfirmClearPath",show=True))

def ClearAllGamesPath():
    for library in manager.list_libraries():
        found_library = (manager.search_libraries(library.name))[0]
        for n,found_game in enumerate(found_library.games):
            manager.update_game_info_all_libraries(game_title=found_game.title,
                                                installed=False,
                                                unpatched_file="",
                                                patched=False,
                                                patched_file="")

def CreateNewGameWindow():
    with dpg.group(tag="AddNewGame",parent="GameCreatorGroup"):
        dpg.add_text("Add games:")
        dpg.add_separator()
        dpg.add_text("*Requiered")
        dpg.add_input_text(label="Game title",width=150,tag="GameTitleInput")
        dpg.add_checkbox(label="Is it installed?",tag="GameInstalledCheckbox",callback=lambda sender,app_data: dpg.configure_item(item="GamePathInput",enabled=app_data))
        dpg.add_input_text(label="Game path folder",width=150,tag="GamePathInput",enabled=False)
        dpg.add_separator()
        dpg.add_text("-Optional")
        dpg.add_checkbox(label="Is the game patched?",tag="GamePatchedCheckbox",callback=lambda sender,app_data: dpg.configure_item(item="GamePatchedPathInput",enabled=app_data))
        dpg.add_input_text(label="Game patched path folder",width=150,tag="GamePatchedPathInput",enabled=False)
        dpg.add_input_text(label="Description",multiline=True,tab_input=True,height=30,width=150,tag="GameDescriptionInput")
        dpg.add_input_text(label="Developer",width=150,tag="GameDeveloperInput")
        dpg.add_input_text(label="Publisher",width=150,tag="GamePublisherInput")
        dpg.add_input_text(label="Released",width=150,tag="GameReleasedInput")
        dpg.add_input_text(label="Genre",width=150,tag="GameGenreInput")
    #                 NewGameId = input("Id(assign a number): ") # The NewGameId should be incremental of how many games are in a library but ok.
    #                 NewGameCover = input("Cover art:")
        dpg.add_input_text(label="Abbreviation",width=150,tag="GameAbbreviationInput")
    #                 NewGameNumber = input("Number(Assing a number): ")
        #dpg.add_input_text(label="Character",width=150,tag="GameMCInput")
        dpg.add_combo(items=Libraries,tag="ComboLibraries")
        dpg.add_button(label="Create new game",callback=AddGame)
        dpg.add_text(default_value="",tag="GameCreationStatus")
    dpg.bind_item_theme("AddNewGame",input_text_Visible)

def ChangeGameInfo(s,a,u):
    global GameObj_Edit_Global
    GameOBJ = GetGameOBJbyTitle(a)
    GameObj_Edit_Global = GetGameOBJbyTitle(a)
    dpg.set_value(item="ChangeGameTitle",value=GameOBJ.title)
    dpg.set_value(item="ChangeGameInstalledCheckbox",value=GameOBJ.installed)
    dpg.set_value(item="ChangeGamePathInput",value=GameOBJ.unpatched_file)
    dpg.set_value(item="ChangeGamePatchedCheckbox",value=GameOBJ.patched)
    dpg.set_value(item="ChangeGamePatchedPathInput",value=GameOBJ.patched_file)
    dpg.set_value(item="ChangeGameDescriptionInput",value=GameOBJ.desc)
    dpg.set_value(item="ChangeGameDeveloperInput",value=GameOBJ.developer)
    dpg.set_value(item="ChangeGamePublisherInput",value=GameOBJ.publisher)
    dpg.set_value(item="ChangeGameReleasedInput",value=GameOBJ.released)
    dpg.set_value(item="ChangeGameGenreInput",value=GameOBJ.genre)
    dpg.set_value(item="ChangeGameAbbreviationInput",value=GameOBJ.abbreviation)

def SaveGameInfo(s,a,u):
    title_change = dpg.get_value(item="ChangeGameTitle")
    installed_change = dpg.get_value(item="ChangeGameInstalledCheckbox")
    unpatched_file_change = dpg.get_value(item="ChangeGamePathInput")
    patched_change = dpg.get_value(item="ChangeGamePatchedCheckbox")
    patched_file_change = dpg.get_value(item="ChangeGamePatchedPathInput")
    desc_change = dpg.get_value(item="ChangeGameDescriptionInput")
    developer_change = dpg.get_value(item="ChangeGameDeveloperInput")
    publisher_change = dpg.get_value(item="ChangeGamePublisherInput")
    released_change = dpg.get_value(item="ChangeGameReleasedInput")
    genre_change = dpg.get_value(item="ChangeGameGenreInput")
    abbreviation_change = dpg.get_value(item="ChangeGameAbbreviationInput")

    manager.update_game_info_all_libraries(game_title=GameObj_Edit_Global.title,
                                           title=title_change,
                                           installed=installed_change,
                                           unpatched_file=unpatched_file_change,
                                           patched=patched_change,
                                           patched_file=patched_file_change,
                                           desc=desc_change,
                                           developer=developer_change,
                                           publisher=publisher_change,
                                           released=released_change,
                                           genre=genre_change,
                                           abbreviation=abbreviation_change)

    refresh_libraries()
    Log(f"Game {GameObj_Edit_Global.title} has been changed with new values.\nValuesChanged\nOld title -> {GameObj_Edit_Global.title} <- New title -> {title_change}"+
        f"\nOld Unpatched File -> {GameObj_Edit_Global.unpatched_file} <- New Unpatched File -> {unpatched_file_change}"+
        f"\nOld Patched File -> {GameObj_Edit_Global.patched_file} <- New Patched File -> {patched_file_change}"+
        f"\nOld Description -> {GameObj_Edit_Global.desc} <- New Description -> {desc_change}"+
        f"\nOld developer -> {GameObj_Edit_Global.developer} <- New Developer -> {developer_change}"+
        f"\nOld publisher -> {GameObj_Edit_Global.publisher} <- New publisher -> {publisher_change}"+
        f"\nOld released -> {GameObj_Edit_Global.released} <- New released -> {released_change}"+
        f"\nOld genre -> {GameObj_Edit_Global.genre} <- New genre -> {genre_change}"+
        f"\nOld abbreviation -> {GameObj_Edit_Global.abbreviation} <- New abbreviation -> {abbreviation_change}")

def SaveTouhouGamesPaths(s,a,u):
    InstalledGames = u
    for i,game in enumerate(InstalledGames):
        manager.update_game_info_all_libraries(game_title=game["game_title"],
                                               unpatched_file=game["file_path"],
                                               patched_file=game["patched_file_path"],
                                               installed=True,
                                               patched=True)
        Log(f"Game {game['game_title']} has been updated."+f"\nNew directory for this game is {game['game_directory']}")

    dpg.add_text(default_value=f"{i} games have been updated with new info, you can check the logs now.",parent="SaveInfoGames",color=[255,255,0])
    refresh_libraries()

def Selected_Patch(s,a,u):
    global SelectedPatch
    print("Selected patch: ",a)
    SelectedPatch = a

def fix_patches_paths():
    game_folder = os.path.dirname(SelectedGameOBJ.unpatched_file)
    config_directory = os.path.join(game_folder, "thcrap", "config")

    def FixPatches():
        # Traverse through the patch configuration files
        files = []
        for i,file in enumerate(os.listdir(config_directory)):
            if file.endswith(".js") and file not in ["config.js", "game.js"]:
                patch_file_path = os.path.join(config_directory, file)
                files.append(file)
                # Load the patch configuration file
                with open(patch_file_path, "r") as f:
                    config = json.load(f)

                # Update the patch paths in the configuration
                for patch in config.get("patches", []):
                    patch_path = patch.get("archive")
                    if patch_path:
                        repo_index = patch_path.find("repos/")
                        if repo_index != -1:
                            patch["archive"] = patch_path[repo_index:]

                # Save the modified patch configuration file
                with open(patch_file_path, "w") as f:
                    json.dump(config, f, indent=4)
        Log(f"Patches fixed for {SelectedGameOBJ.title}, a total of {i} patches has been fixed.")
        dpg.add_text(parent=f"StatusPatches{SelectedGameOBJ.title}",default_value=f"Patches fixed for {SelectedGameOBJ.title}, a total of {i} patches has been fixed.",color=[255,255,0])
        for f in files:
            dpg.add_text(default_value=f"{f} has been fixed",parent=f"StatusPatches{SelectedGameOBJ.title}",color=[255,255,0])

    with dpg.window(label=f"{SelectedGameOBJ.title} patches",width=850,height=450,tag=f"{SelectedGameOBJ.title} patches"):
        dpg.add_text("This window is to fix patches that have an absolute path, it changes it to relative path without you having to do it manually, just click and confirm.")
        dpg.add_button(label=f"Fix all patches for {SelectedGameOBJ.title}",tag=f"FixPatchesButton{SelectedGameOBJ.title}",callback=FixPatches)
        with dpg.group(tag=f"StatusPatches{SelectedGameOBJ.title}"):pass
        with dpg.group():
            try:
                for file in os.listdir(config_directory):
                    if file.endswith(".js") and file not in ["config.js", "game.js"]:
                        patch_file_path = os.path.join(config_directory, file)
                        dpg.add_separator()
                        dpg.add_text(f"Patch: {file}\nLocation: {patch_file_path}")
            except:
                dpg.delete_item(item=f"FixPatchesButton{SelectedGameOBJ.title}")
                dpg.add_text(f"FileNotFoundError: [WinError 3] The system cannot find the path specified\nThis means that thcrap folder doesn't exists in {SelectedGameOBJ.title}",color=[255,0,0])

def StartWithCustomPath(s,a,u):
    if dpg.get_value("CheckboxStartWithCustompath") == True:
        dpg.configure_item(item="GamePath",enabled=False)
        dpg.configure_item(item="CustomTempPath",enabled=True)
    elif dpg.get_value("CheckboxStartWithCustompath") == False:
        dpg.configure_item(item="GamePath",enabled=True)
        dpg.configure_item(item="CustomTempPath",enabled=False)

#BR2#EDIT MENU##
def EditMenu():
    if dpg.does_item_exist("EditLibraryWindow") == False:
        with dpg.window(label="Editing",width=480,tag="EditLibraryWindow",show=False,height=540,no_open_over_existing_popup=False,pos=[200,30]):
            dpg.configure_item(item="EditLibraryWindow",on_close=dpg.hide_item("EditLibraryWindow"))
            dpg.show_item("EditLibraryWindow")
            with dpg.group(tag="LoadLibrary",show=True):
                with dpg.group(tag="LoadingBar",show=True):
                    dpg.add_loading_indicator(circle_count=8)
                    dpg.add_text("Loading")
                    dpg.add_text("It might take a while.")
                with dpg.group(tag="LoadingComplete",show=False):
                    with dpg.tab_bar(tag="TabBar01"):
                        with dpg.tab(label="Edit/Create libraries"):
                            with dpg.tab_bar(tag="TabBar02"):
                                with dpg.tab(label="Edit library"):
                                    with dpg.group(horizontal=True):
                                        dpg.add_text(f"Editing library {SelectedLibraryOBJ.name}")
                                        help("You can double-click any field to select the text and copy it!!\n\nUseful for the location path or any non-english text")
                                    dpg.add_separator()
                                    found_library = (manager.search_libraries(SelectedLibraryOBJ.name))[0]
                                    with dpg.tree_node(label=found_library.name,tag=found_library.name+"Tree"):
                                        Parent = dpg.last_item()
                                        with dpg.group(horizontal=True):
                                            dpg.add_button(label="Remove",user_data=found_library.name,callback=RemoveSelectedLibrary)
                                            dpg.add_button(label="Edit",user_data=found_library.name,callback=EditSelectedLibrary)
                                        dpg.add_text(default_value="Amount of games: "+str(found_library.__len__()),parent=dpg.last_item())
                                        FoundGamesInFoundLibrary(found_library,Parent)
                                with dpg.tab(label="Create new library"):
                                    dpg.add_text(f"Create a new library")
                                    dpg.add_separator()
                                    with dpg.group(horizontal=True):
                                        dpg.add_text("Name:")
                                        dpg.add_input_text(tag="LibraryNameInput")
                                    dpg.add_button(label="Save library",callback=CreateNewLibrary)
                                    dpg.add_text(tag="LibraryCreationStatus",default_value="")
                        with dpg.tab(label="Edit/Add Games"):
                            with dpg.tab_bar(tag="TabBarGames"):
                                with dpg.tab(label="Add a new game"):
                                    dpg.add_text(f"Adds a game to the launcher")
                                    with dpg.group(tag="GameCreatorGroup"):CreateNewGameWindow()
                                with dpg.tab(label="List of games",tag="AllGamesTab"):
                                    dpg.add_text(f"List all games readable for the launcher\nHere you can edit any game.\nNote that the games you edit here will only be edited on that specific library.\nIf you want to edit a game info by itself you should do it in the next tab.")
                                    ListAllGames()
                                with dpg.tab(label="Edit game info",tag="EditGameInfoTab"):
                                    EditGameInfo()

                        with dpg.tab(label="List all libraries",tag="AllLibrariesTab"):
                            dpg.add_text("Libraries:")
                            dpg.add_separator()
                            ListAllLibraries()
                        with dpg.tab(label="Options"):
                            dpg.add_button(label="Refresh libraries",callback=lambda:refresh_libraries())
                            dpg.add_button(label="How it works?",callback=lambda:InfoWindow())
                            dpg.add_button(label="Log window",callback=lambda:dpg.show_item(item="LogWindow"))
                            dpg.add_button(label="Save all libraries into one file",callback=lambda:manager.save_libraries(executable_dir+"\\Libraries\\\AllLibraries\\LibrariesFile.json"))
                            dpg.add_button(label="Print all games",callback=lambda:print([game.title for game in Game.all_games]))
                            dpg.add_button(label="Font manager",callback=lambda:dpg.show_font_manager())
                            dpg.add_button(label="Style editor",callback=lambda:dpg.show_style_editor())
                            dpg.add_button(label="Create backup",callback=CreateBackupLibraries)
                            dpg.add_button(label="Close",callback=lambda:dpg.stop_dearpygui())
        
        dpg.configure_item(item="LoadingComplete",show=True)
        dpg.configure_item(item="LoadingBar",show=False)
    elif dpg.is_item_visible("EditLibraryWindow") == False:
        dpg.show_item("EditLibraryWindow")

def LibrarySelected(s,a,u):
    global SelectedLibraryOBJ
    found_library = (manager.search_libraries(a))[0]
    SelectedLibraryOBJ = found_library
    GameLists = found_library.list_games()
    dpg.configure_item(item="GameList",items=GameLists)
#############################

def updateLaunchedGameInfo():
    def check_process_status(pid):
        start_time = time.time()
        try:
            dpg.set_value(item="CurrentGameStatus",value="Status: Playing.")
            dpg.configure_item(item="CurrentGameStatus",color=[0,255,0])
            while True:
                if find_process_by_pid(pid) is None:
                    break
                elapsed_time = time.time() - start_time
                formatted_time = str(timedelta(seconds=int(elapsed_time)))
                dpg.set_value(item="ElapsedTimeGame", value=f"Elapsed time: {formatted_time}")
                time.sleep(1)
        except psutil.NoSuchProcess:
            dpg.set_value(item="CurrentGameStatus",value="Status: Terminated.")
            dpg.configure_item(item="CurrentGameStatus",color=[255,0,0])
            dpg.configure_item(item="MenuBarPlayingGame",default_value=f"Currently Playing: Nothing",color=[255,255,255])
        else:
            dpg.set_value(item="CurrentGameStatus",value="Status: Terminated.")
            dpg.configure_item(item="CurrentGameStatus",color=[255,0,0])
            dpg.configure_item(item="MenuBarPlayingGame",default_value=f"Currently Playing: Nothing",color=[255,255,255])

    process_name = selected_game + ".exe"
    pid = find_process_by_name(process_name)
    emulatorRun = dpg.get_value("CheckBoxStartWithEmulator")
    if emulatorRun == True:
            pid = find_process_by_name("np21nt.exe")
    if pid is not None and emulatorRun == True:
        print("PID:", pid)
        dpg.set_value(item="CurrentGameStatus",value="Status: Launching...")
        dpg.configure_item(item="CurrentGameStatus",color=[255,255,0])
        dpg.set_value(item="PIDtext", value=f"PID: {pid}")
        dpg.set_value(item="GameLaunched", value=f"Game launched: {SelectedGameOBJ.title}")
        dpg.set_value(item="StatusGameInfo", value="Done.")
        dpg.set_value(item="LibraryLaunched", value=f"Launched from library: {SelectedLibraryOBJ.name}")
        status_thread = threading.Thread(target=check_process_status, args=(pid,))
        status_thread.start()
    else:
        dpg.set_value(item="PIDtext", value="PID: Process not found.")

def ErrorHandlingPopup(ERROR_MESSAGE):
    dpg.delete_item("ErrorStartPopup")
    with dpg.window(label=f"Error: Start game {SelectedGameOBJ.title}",tag="ErrorStartPopup",pos=(int(dpg.get_viewport_width())/3, int(dpg.get_viewport_height())/2),on_close=dpg.delete_item("ErrorStartPopup"),no_resize=True,no_collapse=True,width=500,height=210):
        dpg.add_text(f"{ERROR_MESSAGE}",color=[255,0,0],wrap=-1)
        dpg.add_text("If this occurrs it could very well be that this game doesn't support thcrap.\nCheck and confirm it uses or not thcrap and apply it if so.",wrap=-1)
        dpg.add_text("Also check if you are starting an .exe file.")
        dpg.add_text(f"Game started: {SelectedGameOBJ.title}\nPatched? {SelectedGameOBJ.patched}",wrap=-1)
        dpg.add_separator()
        dpg.add_button(label="Close",callback=lambda:dpg.delete_item("ErrorStartPopup"),width=100)
    dpg.bind_item_theme("ErrorStartPopup",Red_TitleBgActive)

def find_patches(game_folder):
    # Look for thcrap_loader.exe in the game folder
    thcrap_folder = Path(f"{game_folder}/thcrap/thcrap_loader.exe")
        
    if not thcrap_folder.is_file():
        return []  # No patches found

    # Look for JS files in the thcrap config folder
    js_files = [f for f in listdir(os.path.join(game_folder, "thcrap", "config")) if isfile(join(game_folder, "thcrap", "config", f))]
    js_files.remove("config.js")
    js_files.remove("games.js")

    # Get the patch names without the ".js" extension
    patch_names = [os.path.splitext(f)[0] for f in js_files]

    return patch_names

def SelectedGame(s,a,u):
    global GameProcess
    global selected_game
    def _ImageIncreazeModal(s,app_data,user_data):
        SelectedGameOBJ = user_data
        with dpg.popup(parent="Thumbnail", modal=True, mousebutton=dpg.mvMouseButton_Left,no_move=True, tag="_PopupImage"):
            dpg.add_text(f"Touhou {SelectedGameOBJ.title} Cover art.\nThis cover art features the character/s '{SelectedGameOBJ.character}'.")
            dpg.add_separator()
            dpg.add_image(tex,tag="ThumbnailModal",width=500,height=500,)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Close", width=275,indent=100, callback=lambda: dpg.delete_item(item="_PopupImage"))

    def add_online_image(Link,SelectedGameOBJ, **kwargs):
        global tex
        with requests.get(Link) as res:
            img = Image.open(io.BytesIO(res.content)).convert("RGBA")
            imgdata = []
            for r,g,b,a in img.getdata():
                    imgdata.append(r/255)
                    imgdata.append(g/255)
                    imgdata.append(b/255)
                    imgdata.append(a/255)
            tex = dpg.add_static_texture(img.width, img.height, imgdata, parent="texreg")
            dpg.configure_item(item=tex,width=(img.width)/6,height=(img.height)/6)
            return dpg.add_image_button(tex,parent="CoverArt",callback=_ImageIncreazeModal,tag="Thumbnail",user_data=SelectedGameOBJ, **kwargs)

    global SelectedGameOBJ
    print(f"Selected Library: {SelectedLibraryOBJ}\tSelected Game: {a}")
    for game in SelectedLibraryOBJ.games:
        if game.title == a:
            SelectedGameOBJ = game
            dpg.set_value(item="NameGame",value=SelectedGameOBJ.title)
            dpg.set_value(item="AbbreviationGame",value=SelectedGameOBJ.abbreviation)
            dpg.set_value(item="Developer",value=SelectedGameOBJ.developer)
            dpg.set_value(item="Publisher",value=SelectedGameOBJ.publisher)
            dpg.set_value(item="Released",value=SelectedGameOBJ.released)
            dpg.set_value(item="Genre",value=SelectedGameOBJ.genre)
            dpg.set_value(item="Description",value=SelectedGameOBJ.desc)
            
            dpg.set_value(item="GamePath",value=SelectedGameOBJ.unpatched_file)
            dpg.set_value(item="IsPathValid",value="")

            dpg.configure_item(item="LocalizeGame",user_data=SelectedGameOBJ.title)

            if SelectedGameOBJ.installed == True:
                dpg.set_value(item="GameInstalledTextVAR",value="Yes")
                dpg.configure_item(item="GameInstalledTextVAR",color=[0,255,0])
            elif SelectedGameOBJ.installed == False:
                dpg.set_value(item="GameInstalledTextVAR",value="No")
                dpg.configure_item(item="GameInstalledTextVAR",color=[255,0,0])
            if SelectedGameOBJ.patched == True:
                dpg.set_value(item="GamePatchedTextVAR",value="Yes")
                dpg.configure_item(item="GamePatchedTextVAR",color=[0,255,0])
                dpg.configure_item(item="CheckBoxStartWithThCrap",default_value=True)
            elif SelectedGameOBJ.patched == False:
                dpg.set_value(item="GamePatchedTextVAR",value="No")
                dpg.configure_item(item="GamePatchedTextVAR",color=[255,0,0])
                dpg.configure_item(item="CheckBoxStartWithThCrap",default_value=False)

            if SelectedGameOBJ.path_valid == False:
                dpg.set_value(item="IsPathValid",value="Your game path is not valid")
                dpg.configure_item(item="IsPathValid",color=[255,0,0])

            #add_online_image(SelectedGameOBJ.cover,SelectedGameOBJ)


    # WE START THE GAME HERE.
    # The user can start the game with the unpatched original file.
    # Can start with the patched one that always comes from moriyashrine.org
    # Or it can start with any patched he has selected.

    game_folder = os.path.dirname(SelectedGameOBJ.unpatched_file)  # Get the game folder path
    thcrap_loader_path = os.path.join(game_folder, "thcrap", "thcrap_loader.exe")  # Construct the thcrap_loader.exe path
    selected_game = os.path.splitext(os.path.basename(SelectedGameOBJ.unpatched_file))[0]  # Get the base name of the unpatched file
    
    # Get the list of patches for the selected game
    patches = find_patches(game_folder)

    if patches:
        patches.insert(0, "None")

    dpg.configure_item(item="TouhouJSCombo",items=patches)
    dpg.set_value(item="TouhouJSCombo",value=None)
    print("Patches:", patches)

    if s == "StartGameButton":
        os.chdir(game_folder)
        if dpg.get_value("CheckboxStartWithCustompath") == True:
            print("-------CUSTOM--------")
            print("Playing:", SelectedGameOBJ.title)
            print("starting file:", dpg.get_value("CustomTempPath"))
            print("selected_game:", selected_game)
            print("----------------------")
            GameProcess = subprocess.Popen([dpg.get_value("CustomTempPath")])
        else:
            try:
                if dpg.get_value(item="CheckBoxStartWithThCrap") == False and dpg.get_value("CheckBoxStartWithEmulator") == False:
                    # Start with the unpatched original file
                    print("-------UNPATCHED--------")
                    print("Playing:", SelectedGameOBJ.title)
                    print("starting file:", SelectedGameOBJ.patched_file)
                    print("selected_game:", selected_game)
                    print("selected_patch:", SelectedPatch)
                    print("game_folder:", game_folder)
                    print("thcrap_loader_path:", thcrap_loader_path)
                    print("----------------------")
                    GameProcess = subprocess.Popen([SelectedGameOBJ.unpatched_file])
                elif dpg.get_value(item="CheckBoxStartWithThCrap") == True:
                    # Start with the patched file from moriyashrine.org
                    print("---------PATCHED--------")
                    print("Playing:", SelectedGameOBJ.title)
                    print("starting file:", SelectedGameOBJ.patched_file)
                    print("selected_game:", selected_game)
                    print("selected_patch:", SelectedPatch)
                    print("game_folder:", game_folder)
                    print("thcrap_loader_path:", thcrap_loader_path)
                    print("----------------------")
                    if SelectedPatch != None:
                        GameProcess = subprocess.Popen([thcrap_loader_path,SelectedPatch+".js", selected_game])
                    else:
                        GameProcess = subprocess.Popen([SelectedGameOBJ.patched_file])
                elif dpg.get_value("CheckBoxStartWithEmulator") == True and dpg.get_value(item="CheckBoxStartWithThCrap") == False:
                    print("---------PC-98----------")
                    print("Playing:", SelectedGameOBJ.title)
                    print("starting file:", SelectedGameOBJ.patched_file)
                    print("selected_game:", selected_game)
                    print("selected_patch:", SelectedPatch)
                    print("game_folder:", game_folder)
                    print("thcrap_loader_path:", thcrap_loader_path)
                    print("----------------------")
                    EmulatorConfigINI.set('NekoProject21', 'HDfolder', SelectedGameOBJ.unpatched_file)
                    with open(EmulatorPath+'\\np21nt.ini', 'w') as EmulatorConfig:
                        EmulatorConfigINI.write(EmulatorConfig)
                    EmulatorConfigINI.set('NekoProject21', 'HDD1FILE', SelectedGameOBJ.unpatched_file)
                    with open(EmulatorPath+'\\np21nt.ini', 'w') as EmulatorConfig:
                        EmulatorConfigINI.write(EmulatorConfig)
                    GameProcess = subprocess.Popen([EmulatorPath+"\\np21nt.exe"])
            except FileNotFoundError as error:ErrorHandlingPopup(error)
            except TypeError as error:ErrorHandlingPopup(error)
            except OSError as error: ErrorHandlingPopup(error)
            else:
                updateLaunchedGameInfo()
                dpg.configure_item(item="MenuBarPlayingGame",default_value=f"Currently Playing: {SelectedGameOBJ.title}",color=[0,255,0])

def SaveSelectedLibrary(s,a,u):
    if u == "Temporal Library":
        with dpg.window(label="Error",tag="ErrorPopup",pos=(int(dpg.get_viewport_width())/2, int(dpg.get_viewport_height())/2),on_close=True,no_resize=True,no_collapse=True,width=300,height=150):
            dpg.add_text("You can't modify nor save 'Temporal Libraly'")
            dpg.add_text(u,color=[255,0,0])
            dpg.add_text("Only change it games inside.")
            dpg.add_separator()
            dpg.add_button(label="Close",callback=lambda:dpg.delete_item("ErrorPopup"))
        dpg.bind_item_theme("ErrorPopup",Red_TitleBgActive)
    else:
        found_library = (manager.search_libraries(u))[0]
        found_library.save(f"{executable_dir}\\libraries\\{found_library.name}.json")
        Log(f"Library '{u}' saved to '{executable_dir}\\libraries\\{found_library.name}.json'")

def CreateNewLibrary():
    print(dpg.get_value(item="LibraryNameInput"))
    NewLibraryName = str(dpg.get_value(item="LibraryNameInput"))
    NewLibraryName = Library(NewLibraryName)
    manager.add_library(NewLibraryName)
    refresh_libraries()
    Log(f"New library created called '{NewLibraryName.name}'")
    dpg.set_value("LibraryCreationStatus",f"Library {NewLibraryName.name} has been created!\nYou can now add games to this library.")

def AddGame():
    print("--------------------------\n")
    GameTitleCG = dpg.get_value("GameTitleInput")
    GameInstalledCG = dpg.get_value("GameInstalledCheckbox")
    GameInstalledPathCG = dpg.get_value("GamePathInput")
    GamePatchedCG = dpg.get_value("GamePatchedCheckbox")
    GamePatchedPathCG = dpg.get_value("GamePatchedPathInput")
    GameDescCG = dpg.get_value("GameDescriptionInput")
    GameDevCG = dpg.get_value("GameDeveloperInput")
    GamePublCG = dpg.get_value("GamePublisherInput")
    GameReleasedCG = dpg.get_value("GameReleasedInput")
    GameGenreCG = dpg.get_value("GameGenreInput")
    GameAbbrCG = dpg.get_value("GameAbbreviationInput")
    ComboLibrariesCG = dpg.get_value("ComboLibraries")
    dpg.set_value("GameCreationStatus","Game '"+GameTitleCG+"' added to "+ComboLibrariesCG)
    if GamePatchedPathCG == "" or GamePatchedPathCG == " " or GamePatchedPathCG == None:
        GamePatchedPathCG = None
    if GamePatchedCG == "" or GamePatchedCG == " " or GamePatchedCG == None:
        GamePatchedCG == False
    try:found_library = (manager.search_libraries(ComboLibrariesCG))[0]
    except:found_library = None
    else:found_library = (manager.search_libraries(ComboLibrariesCG))[0]
    if found_library == None or found_library == "" or found_library == " ":
        GameObject = Game(GameTitleCG,GameInstalledCG,GameInstalledPathCG,GamePatchedCG,GamePatchedPathCG,GameDescCG,GameDevCG,GamePublCG,GameReleasedCG,GameGenreCG,None,None,GameAbbrCG,None)
        print(GameObject,"\nAdded to",Temporal_Library.name)
        Temporal_Library.add_game(GameObject)
        dpg.set_value("GameCreationStatus","Game '"+GameTitleCG+"' added to "+Temporal_Library.name)
        Log(f"Game '{GameTitleCG}' has been created and assigned to library '{Temporal_Library.name}'")
    else:
        GameObject = Game(GameTitleCG,GameInstalledCG,GameInstalledPathCG,GamePatchedCG,GamePatchedPathCG,GameDescCG,GameDevCG,GamePublCG,GameReleasedCG,GameGenreCG,None,None,GameAbbrCG,None)
        print(GameObject,"\nAdded to",found_library.name)
        found_library.add_game(GameObject)
        dpg.set_value("GameCreationStatus","Game '"+GameTitleCG+"' added to "+found_library.name)
        Log(f"Game '{GameTitleCG}' has been created and assigned to library '{found_library.name}'")
    refresh_libraries()

def PresetsGame(s,a,u):
    print(s,a,u)
    if u == 1:
        dpg.set_value("GameTitleInput","Touhou Puppet Dance Performance - Shard of Dreams")
        dpg.set_value("GameInstalledCheckbox",False)
        dpg.set_value("GamePatchedCheckbox",False)
        dpg.set_value("GamePatchedPathInput","")
        dpg.set_value("GameDescriptionInput","Touhou Puppet Dance Performance: Shard of Dreams is an expansion of the Touhou fangame which includes new areas, a new puppet type called Warped, and features Touhou characters from 14.5 and 15. The game follows a story where the player character is transported to Gensokyo and discovers a strange incident involving puppets shaped like Touhou characters. The player must use these puppets to help solve the incident and return home. The game is similar to Pokemon, with visible stat values and customizable moves and stats, and evolutions are handled through style changes that can only be reversed through reincarnation.")
        dpg.set_value("GameDeveloperInput","FocasLens")
        dpg.set_value("GamePublisherInput","FocasLens")
        dpg.set_value("GameReleasedInput","December 30, 2015")
        dpg.set_value("GameGenreInput","RPG")
        dpg.set_value("GameAbbreviationInput","TPDP")
    elif u == 2:
        dpg.set_value("GameTitleInput","Touhou Luna Nights")
        dpg.set_value("GameInstalledCheckbox",False)
        dpg.set_value("GamePatchedCheckbox",False)
        dpg.set_value("GamePatchedPathInput","")
        dpg.set_value("GameDescriptionInput","Touhou Luna Nights is a Metroidvania title with a heavy emphasis on exploration and action.Developed by Team Ladybug, creators of multiple fantastic action games thus far.")
        dpg.set_value("GameDeveloperInput","Vaka Game Magazine, Team Ladybug")
        dpg.set_value("GamePublisherInput","Why so serious?, PLAYISM")
        dpg.set_value("GameReleasedInput","26 Feb, 2019")
        dpg.set_value("GameGenreInput","2D Action/Platform")
        dpg.set_value("GameAbbreviationInput","TNL")
    elif u == 3:
        dpg.set_value("GameTitleInput","Labyrinth of Touhou - Gensoukyo and the Heaven-piercing Tree")
        dpg.set_value("GameInstalledCheckbox",False)
        dpg.set_value("GamePatchedCheckbox",False)
        dpg.set_value("GamePatchedPathInput","")
        dpg.set_value("GameDescriptionInput","Challenge the Great Tree with a team of 12 maidens from Touhou Project, and uncover the mastermind behind recent incidents. The game offers over 50 characters to choose from, with customizable skills, equipment, and subclasses. Conquer more than 100 tricky boss battles in a randomly generated labyrinth that spans over 40 floors. Enjoy the revised character graphics, adorable chibi avatars, and the increased movement speed and consecutive battle bonus. Spend money to increase status or build your team the way you want. Choose your tactics and characters wisely for a beautiful and daunting battle experience.")
        dpg.set_value("GameDeveloperInput","Nise Eikoku Shinshidan, CUBETYPE")
        dpg.set_value("GamePublisherInput","CUBETYPE")
        dpg.set_value("GameReleasedInput","August 12, 2013")
        dpg.set_value("GameGenreInput","Old-School RPG")
        dpg.set_value("GameAbbreviationInput","LoT")
    elif u == 4:
        dpg.set_value("GameTitleInput","Fantasy Maiden Wars")
        dpg.set_value("GameInstalledCheckbox",False)
        dpg.set_value("GamePatchedCheckbox",False)
        dpg.set_value("GamePatchedPathInput","")
        dpg.set_value("GameDescriptionInput","A compilation of the four Gensou Shoujo Wars games, some sprites and CG might have been remade and some extras might have been included.")
        dpg.set_value("GameDeveloperInput","さんぼん堂")
        dpg.set_value("GamePublisherInput","さんぼん堂")
        dpg.set_value("GameReleasedInput","August 12, 2019")
        dpg.set_value("GameGenreInput","SRPG")
        dpg.set_value("GameAbbreviationInput","FMW")
    elif u == 5:
        dpg.set_value("GameTitleInput","Touhou Sky Arena Matsuri Climax")
        dpg.set_value("GameInstalledCheckbox",False)
        dpg.set_value("GamePatchedCheckbox",False)
        dpg.set_value("GamePatchedPathInput","")
        dpg.set_value("GameDescriptionInput","The game includes characters such as Reimu, Marisa, and Sakuya, and stages like the Forest of Magic and Scarlet Devil Mansion. The game modes include Arcade, Vs, Survival, and Network, which allows for online play. The game also features a tension meter that affects gameplay and abilities, with different levels of tension unlocking different abilities for the characters.")
        dpg.set_value("GameDeveloperInput","領域ZERO")
        dpg.set_value("GamePublisherInput","領域ZERO")
        dpg.set_value("GameReleasedInput","March 13, 2011")
        dpg.set_value("GameGenreInput","3D Arena Shooter")
        dpg.set_value("GameAbbreviationInput","SAMC")

def refresh_libraries():
    global Libraries
    Libraries = set()
    for library in manager.list_libraries():
        if library.name == "Temporal Library":print("No")
        else:
            found_library = (manager.search_libraries(library.name))[0]
            Libraries.add(found_library.name)
            found_library.save(f"{executable_dir}\\libraries\\{found_library.name}.json")
    Libraries.add(Temporal_Library.name)
    Libraries = list(Libraries)
    manager.order_libraries_by_name()
    print("LIBRARIES FOUND\n---------------------")
    manager.print_libraries()
    try:
        dpg.configure_item(item="LibrariesCombo",items=Libraries)
    except Exception as Error:pass
    if dpg.does_item_exist("EditLibraryWindow") == True:
            ListAllLibraries()
            ListAllGames()
            EditGameInfo()
    else:pass
    Log(f"Libraries has been refreshed!")
refresh_libraries()

with dpg.window(label="Launcher Main Menu",tag="MainWindow",width=ViewPortWidth,height=ViewPortHeight,no_close=True,no_collapse=True,no_move=True,no_open_over_existing_popup=True,no_focus_on_appearing=True,no_bring_to_front_on_focus=True,no_resize=True,no_title_bar=True):
    with dpg.menu_bar(parent="MainWindow"):
        with dpg.menu(label="Menu",tag="Menu001"):
            dpg.add_text(f"Build: {CURRENTBUILD[1]} {CURRENTBUILD[0]} Release Date:{CURRENTBUILD[2]}")
            dpg.add_menu_item(label="Changelog",callback=lambda:dpg.configure_item(item="ChangelogWindow",show=True))
            #with dpg.group(horizontal=True,tag="Group005"):
            #    dpg.add_text("Current folder path:")
            #    dpg.add_text(default_value=f"",color=[255,255,0])
                #if BoolFolderDoesntExists == True:
                #    dpg.add_text(default_value="This folder doesn't exists! Change it to the folder were all the touhou games are.",parent="Menu001",color=[255,0,0])
            #dpg.add_menu_item(label="Change Touhou games folder")
            dpg.add_menu_item(label="Disclaimer",callback=lambda:dpg.configure_item(item="DisclaimerWindow",show=True))
            dpg.add_menu_item(label="Close launcher",callback=lambda:dpg.stop_dearpygui())
        with dpg.menu(label="Tools&Options"):
            dpg.add_menu_item(label="DearPyGui about.", callback=dpg.show_about)
            dpg.add_menu_item(label="Mugen-kai about.",callback=lambda:dpg.configure_item(item="launcherInfoWindow",show=True))
            #dpg.add_menu_item(label="Show Metrics", callback=lambda:dpg.show_tool(dpg.mvTool_Metrics))
            #dpg.add_menu_item(label="Show Touhou Launcher Documentation", callback=lambda:dpg.show_tool(dpg.mvTool_Doc))
            #dpg.add_menu_item(label="Show Touhou mods", callback=lambda:dpg.configure_item(item="TouhouModsWindow",show=True))
            dpg.add_menu_item(label="Show games status in launcher", callback=lambda:dpg.configure_item(item="GamesStatusWindow",show=True))
            #dpg.add_menu_item(label="Show Style Editor", callback=lambda:dpg.show_tool(dpg.mvTool_Style))
            #dpg.add_menu_item(label="Show Font Manager", callback=lambda:dpg.show_tool(dpg.mvTool_Font))
            #dpg.add_menu_item(label="Show Item Registry", callback=lambda:dpg.show_tool(dpg.mvTool_ItemRegistry))
            dpg.add_menu_item(label="Touhou Games folder",callback=lambda:dpg.configure_item(item="ThGamesFolderWindow",show=True))
            dpg.add_menu_item(label="Toggle Fullscreen", callback=lambda:dpg.toggle_viewport_fullscreen())
            #with dpg.group(tag="Group004"):
            #    dpg.add_button(label="Clear FilePathTH",tag="ClearFilePathMENUITEM")
        #with dpg.menu(label="Thcrap loader"):
        #    dpg.add_button(tag="LocalizeThcrap",label="Locate Thcrap folder.")
        #    dpg.add_input_text(label="Global Thcrap path",tag="ThcrapFolderPath",enabled=True)
        #    dpg.add_text(tag="IsPathValidTHCRAP",label="")
        with dpg.menu(label="troubleshooting"):
            dpg.add_text("The launcher can't find th_crap but the folder exists inside the all-touhou game folder!")
            dpg.add_text("To solve that check if your game has the correct-folder name.",color=[255,255,0],indent=30)
            with dpg.tree_node(label="Game titles",tag="TGameTitles",indent=30):
                j = 0
                dpg.add_text(default_value="Click any title to copy it's name and correct any bad written folders!")
                while True:
                    j = j + 1
                    dpg.add_button(label=str(TouhouGames[j]['Title']),user_data=str(TouhouGames[j]['Title']),callback=_Clipboard,parent="TGameTitles")
                    if j > 30:break
            dpg.add_text("We recommend to put all your touhou games inside the same folder to avoid any errors.",color=[255,255,0],indent=30)
            dpg.add_text("The launcher for some reason finds games that are installed but not parched even tho thcrap exists in the game's folder.")
            dpg.add_text("We recommend to restart the launcher just in that case.",color=[255,255,0],indent=30)
            dpg.add_separator()
            dpg.add_text("When i start a game with a patch it says 'Some patches in your configuration could not be found' some paths and then\n'Please reconfigure your patch stack - either by running the configuration tool, or by simply editing your run configuration file' and then the patch path.")
            dpg.add_text("That could mean that you changed your game location along side it's thcrap inside of it, because it uses absolute paths it didn't change, you can click on\n 'Fix patches' on the user config in a selected game to make them work again.",color=[255,255,0],indent=30)
        with dpg.menu(label="Emulator"):
            dpg.add_text("To play Touhou PC-98 era games on modern windows OS, it needs an emulator to run.")
            dpg.add_text("Tested emulators to use are: np2fmgen")
            dpg.add_separator()
            dpg.add_text("Introduce the emulator folder")
            dpg.add_input_text(label="Path",tag="EmulatorFolderPath")
            with dpg.group(horizontal=True):
                dpg.add_text("Current path: ")
                dpg.add_text(default_value=EmulatorPath,color=[255,255,0])
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save",callback=EmulatorSave)
                dpg.add_text(default_value="",tag="EmulatorPathStatus")
        with dpg.menu(label=f"Game Info"):
            dpg.add_text("Here you can see what game is playing and some info about it.")
            dpg.add_text(tag="StatusGameInfo",default_value="Checking for launched games...")
            dpg.add_separator()
            dpg.add_text(tag="GameLaunched",default_value="Game launched: ")
            dpg.add_text(tag="PIDtext",default_value="PID: ")
            dpg.add_text(tag="LibraryLaunched",default_value="Launched from library: ")
            dpg.add_text(tag="ElapsedTimeGame",default_value="Elapsed time: ")
            dpg.add_text(tag="CurrentGameStatus",default_value="Status: ")
        dpg.add_text(f"Currently playing: Nothing",tag="MenuBarPlayingGame")

    # BREAK
    # MAIN WINDOW
    with dpg.group(horizontal=True,parent="MainWindow"):
        with dpg.child_window(autosize_x=False,height=-1,width=350,tag="GamesWindowList"):
            with dpg.group(horizontal=True):
                dpg.add_combo(items=Libraries,tag="LibrariesCombo",default_value="Official Games",callback=LibrarySelected,width=200)
                SelectedLibraryOBJ = (manager.search_libraries("Official Games"))[0]
                dpg.add_button(label="Edit libraries",callback=EditMenu)
                help("The Drop-down menu displays a list of Touhou games, including both official games made by ZUN and fan-made games.\nOfficial games and Fangames libraries are auto-generated by the launcher.\nYou can select any game from the list to start playing.\n\nThe 'Edit' button allows you to edit the library itself, adding new games or removing games.\n\nThe 'New' button allows you to create an entire new library by the found games.")
            with dpg.group(horizontal=True):
                First_Library = (manager.search_libraries(dpg.get_value("LibrariesCombo")))[0]
                print(First_Library.list_int_games())
                dpg.add_listbox((First_Library.list_games()),width=350,callback=SelectedGame,num_items=First_Library.list_int_games()+3,tag="GameList")
        with dpg.child_window(autosize_x=True):
            with dpg.group(show=True):
                with dpg.group(horizontal=True):
                    dpg.add_text("Name game: ")
                    dpg.add_text(tag="NameGame",default_value="Select a game")
                with dpg.group(horizontal=True):
                    dpg.add_text("Abbreviation: ")
                    dpg.add_text(tag="AbbreviationGame",default_value="")
                with dpg.theme(tag="_StartButtonTheme"+str(3)):
                    with dpg.theme_component(dpg.mvButton):
                        dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(3/9.0, 0.6, 0.6))
                        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hsv_to_rgb(3/10.0, 0.9, 0.9))
                        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hsv_to_rgb(3/7.0, 0.7, 0.7))
                        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3*1)
                        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3*3, 3*3)

                with dpg.group(horizontal=True,tag="StartButton"):
                    dpg.add_button(label="Start",tag="StartGameButton",callback=SelectedGame)
                    dpg.bind_item_theme(dpg.last_item(), "_StartButtonTheme"+str(3))
                    dpg.add_combo(list(("Select a game"," ")),tag="TouhouJSCombo", label="Patches",callback=Selected_Patch)
                    help("You can select any patch avaliable in this list here.\n\nIf you select the first option then it will start thcrap but without any patch.\n\nIf you can't select any patches it means that it didn't found the game/thcrap or it doesn't suppor thcrap.\n\nOn last note, a game may not have thcrap but it may have an un-official english patch, select it to play the english version.")
                dpg.add_separator()
                with dpg.group(horizontal=False):
                    dpg.add_text("Cover art: ")
                    dpg.add_button(label="+")
                    with dpg.group(horizontal=True,tag="CoverArt"):pass
                with dpg.group(horizontal=True):
                    dpg.add_text("Developer: ")
                    dpg.add_text(tag="Developer",default_value="")
                with dpg.group(horizontal=True):
                    dpg.add_text("Publisher: ")
                    dpg.add_text(tag="Publisher",default_value="")
                with dpg.group(horizontal=True):
                    dpg.add_text("Released: ")
                    dpg.add_text(tag="Released",default_value="")
                with dpg.group(horizontal=True):
                    dpg.add_text("Genre: ")
                    dpg.add_text(tag="Genre",default_value="")
                with dpg.group(horizontal=True):
                    dpg.add_text("Description: ")
                    dpg.add_text(tag="Description",default_value="",wrap=430)
                dpg.add_separator()
                with dpg.group(tag="GamesInstalledStatusInfo"):
                    with dpg.group(horizontal=True,tag="GameInstalledStatusInfo"):
                        dpg.add_text("Game installed: ",tag="GameInstalledText")
                        dpg.add_text("",tag="GameInstalledTextVAR")
                    with dpg.group(horizontal=True,tag="GamePatchedStatusInfo"):
                        dpg.add_text("Game patched: ",tag="GamePatchedText")
                        dpg.add_text("",tag="GamePatchedTextVAR")
                with dpg.group(horizontal=True):
                    dpg.add_text("Game directory: ")
                    dpg.add_input_text(tag="GamePath",width=300,enabled=True)
                    dpg.add_button(tag="LocalizeGame",label="Change path",user_data=None,callback=ChangeGamePath)
                    help("This is the game path directory, once you change it it will be saved.")
                dpg.add_text(label="",tag="IsPathValid")
                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_spacing(height=20)
                    dpg.add_spacing(width=-16)
                    dpg.add_checkbox(label="Start with Thcrap",tag="CheckBoxStartWithThCrap",default_value=True)
                    help("If checkbox is checked then the game will start with thcrap whetever you have a patch selected or not.\nIf you de-selected then the patch selecter will be disabled and it will start the game with the original un-translated game.\nIf the option doesn't appear that means that thcrap is not supported or does not exists in the game folder.")
                    dpg.add_checkbox(label="Start with emulator",tag="CheckBoxStartWithEmulator",default_value=False)
                    help("This is for games that need an emulator, typically Touhou 1 to 5 or any game that was made for PC-98 or that can use the emulator.")
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="Use custom path",tag="CheckboxStartWithCustompath",default_value=False,callback=StartWithCustomPath)
                    help("Does your game not work? Or do you want to start from another .exe? You can do it here.\nIf you enable the checkbox the launcher will use this temporal path and ignore the original one\nThe launcher will remember your configuration and you can disable it anytime after fixing your original .exe path\nPartly implemented.")
                    dpg.add_input_text(tag="CustomTempPath",width=300,enabled=False)
                dpg.add_button(label="Fix patches",callback=fix_patches_paths)
                with dpg.window(label="Touhou mods",width=500,height=400,tag="TouhouModsWindow",show=False):
                    with dpg.group(tag="TouhouMods"):
                        dpg.add_text("Mods")

                with dpg.window(label="Games status",width=550,height=450,tag="GamesStatusWindow",show=False):
                    with dpg.group(tag="GamesStatus"):
                        dpg.add_text("In this window you can see all the games without library that the launcher detected.\nYou can see if a path is valid or not here and edit their values.")
                        dpg.add_separator()
                        existing_games_0 = set()
                        for g,game in enumerate(Game.all_games):
                            if game.title not in existing_games_0:
                                with dpg.tree_node(label=game.title):
                                    if game.path_valid == False:
                                        dpg.add_text(f"{game.path_valid} | {game.unpatched_file} | This game path is NOT valid")
                                        dpg.configure_item(item=dpg.last_item(),color=[255,0,0])
                                        dpg.add_text("CHECK IF THE PATH EXISTS IN YOUR COMPUTER.")
                                        dpg.add_text("If it doesn't exists, you can always assing it a new path here.")
                                        dpg.add_input_text(hint="C:\Touhou\...\*.exe",tag=f"InputPath{g}",user_data=g,callback=PathValidator)
                                        dpg.add_text(tag=f"PathValidatorStatus{g}")
                                        dpg.add_button(label="Change path",user_data=g,callback=PathChanger)
                                    elif game.path_valid == True:
                                        dpg.add_text(f"{game.path_valid} | {game.unpatched_file} | This game path is NOT valid")
                                        dpg.configure_item(item=dpg.last_item(),color=[0,255,0])
                                        dpg.add_text("The game exists in your computer.")
                                        dpg.add_input_text(default_value=game.unpatched_file,enabled=False)
                                        folder_path = os.path.dirname(game.unpatched_file)
                                        dpg.add_button(label="Click here to go to it's folder location.",user_data=folder_path,callback=openFolder)
                                    dpg.add_separator()
                                    if game.patched == False:
                                        dpg.add_text(f"{game.path_valid} | This game is NOT patched")
                                        dpg.configure_item(item=dpg.last_item(),color=[255,0,0])
                                    elif game.patched == True:
                                        dpg.add_text(f"{game.path_valid} | This game path is patched")
                                        dpg.configure_item(item=dpg.last_item(),color=[0,255,0])
                            existing_games_0.add(game.title)

                with dpg.window(label="About Touhou Mugen-kai launcher",width=550,height=450,pos=(100, 40),tag="launcherInfoWindow",show=False):
                    dpg.add_text("Developers",color=[155,177,255])
                    with dpg.group(horizontal=True):
                        dpg.add_text(bullet=True)
                        dpg.add_text("Fumo Friday Official#7933(Layout desing, overall structure)",color=[255,204,153])
                        comment("My own comment is that i got help from my wonderful friend and one that persisted with me even if we had too many challenged on the way.\n\nThe fact that he managed to stay with me and not leave and work with me until we finally managed to get our first version out is astonishing.\nThank you so much, i hope we get even more help as time goes on!\n\nOverall i got stuck on a earlier part on this launcher and i asked for his help and he delivered\nat the end we end up releasing the entire launcher as best as we could but we honestly think there still a lot to be done.")
                    with dpg.group(horizontal=True):
                        dpg.add_text(bullet=True)
                        dpg.add_text("Mikoyan#8230(Mainly help in coding and some testing)",color=[153,204,255])
                        comment("I'm no python expert... And i even had to start learning new things but he really helped me(he insisted a lot lol).\nThanks to that i honestly learnt new things in python in general and GUI stuff.\n\nI don't have much to add but it was all fun in the end, hope this little launcher evolves into something better with time.")
                    with dpg.group(horizontal=True):
                        dpg.add_text(bullet=True)
                        dpg.add_text("We are eagerly to look for any type of help <3")
                    hyperlink("Touhou Mugen-kai github","https://github.com/FumoFridayOfficial/TouhouMugenKai")
                    dpg.add_separator()
                    with dpg.group(horizontal=True):
                        dpg.add_text("Python",color=[255,255,0])
                        dpg.add_text("as main programming language")
                    with dpg.group(horizontal=True):
                        dpg.add_text("GUI Launcher made in")
                        dpg.add_text("DearPyGui (DPG)",color=[255,255,0])
                    with dpg.group(horizontal=True):
                        dpg.add_text("You can find it here: ")
                        hyperlink("DearPyGui github","https://github.com/hoffstadt/DearPyGui")
                    dpg.add_separator()
                    dpg.add_text("Testers",color=[255,177,155])
                    dpg.add_text("Beta",color=[205,177,155])
                    with dpg.group(horizontal=True):
                        dpg.add_text(bullet=True)
                        dpg.add_text("You can be here...")
                    dpg.add_separator()

                with dpg.window(label="Touhou Games folder",width=550,height=450,tag="ThGamesFolderWindow",show=False):
                    with dpg.group():
                        dpg.add_text("This window's purpose is to detect all touhou games in a folder and set it on the launcher.")
                        dpg.add_text("For this reason, it is recommended to have all touhou games in the same folder.")
                        dpg.add_separator()
                        dpg.add_input_text(hint="C:\TouhouGames",tag=f"InputPath9999",user_data=9999,callback=PathValidator)
                        dpg.add_text(tag="PathValidatorStatus9999")
                        dpg.add_button(label="Search",callback=SearchTouhouGamesInFolder)
                        dpg.add_text(default_value="",tag="InstalledTHGamesFound")
                        with dpg.group(tag="SaveInfoGames"):pass
                        with dpg.group(tag="OfficialGamesGroup"):
                            pass
                
                with dpg.window(label="DISCLAIMER",width=550,height=620,pos=(150,10),tag="DisclaimerWindow",on_close=DisclaimerReaded,no_close=True,no_collapse=True,no_resize=True,no_move=True,show=False):
                    dpg_markdown.add_text("__DISCLAIMER__")
                    dpg.add_text("Read carefully.")
                    dpg.add_separator()
                    with dpg.child_window(height=400):
                        dpg.add_text("This application is provided for informational and personal use purposes only. By using this application, you acknowledge and agree to the following:",wrap=500)
                        dpg.add_text("1.This application is currently on beta, use at your own risk and report any bugs to the developer in github.\n",wrap=500)
                        dpg.add_text("2.This application is intended for locally installed games and does not guarantee compatibility or safety with online games, games with anti-cheat systems, or games governed by strict terms of service.\n",wrap=500)
                        dpg.add_text("3.You are solely responsible for any consequences that may arise from the use of this application with online games or games with anti-cheat systems, including but not limited to penalties, bans, or account suspensions.\n",wrap=500)
                        dpg.add_text("4.Do not try to launch online with or that have anti-cheat, i haven't tested them yet, read part 6.\n",wrap=500)
                        dpg.add_text("5.This application does not endorse or promote cheating, hacking, or any form of unfair play. It is your responsibility to respect the rules and regulations set forth by game developers and the gaming community.\n",wrap=500)
                        dpg.add_text("6.Launching online games through external tools or scripts, including Python GUI launchers, can potentially trigger anti-cheat systems if they detect unauthorized modifications or tampering with the game process. Even if the launcher itself does not modify the game files or memory, anti-cheat systems may still flag it as suspicious behavior.\n",wrap=500)
                    dpg.add_separator()
                    dpg.add_text("By using this application, you accept and agree to the terms and conditions outlined in this disclaimer. If you do not agree with any of these terms, you should refrain from using this application.",wrap=500)
                    dpg.add_button(label="I readed and accept the disclaimer.",user_data=True,callback=DisclaimerReaded,width=-1)
                    dpg.add_button(label="I don't accept the disclaimer.",user_data=False,callback=DisclaimerReaded,width=-1)
                
                if DisclaimerAcceptedINI == True or DisclaimerAcceptedINI == "True":dpg.configure_item(item="DisclaimerWindow",show=False)
                elif DisclaimerAcceptedINI == False or DisclaimerAcceptedINI == "False":dpg.configure_item(item="DisclaimerWindow",show=True)

                with dpg.window(label="Changelog",width=550,height=620,pos=(150,10),tag="ChangelogWindow",show=False):
                    dpg_markdown.add_text("__Changelog__")
                    dpg.add_text(f"Current build {CURRENTBUILD[1]} {CURRENTBUILD[0]}\nRelease date: {CURRENTBUILD[2]}.")
                    dpg.add_separator()
                    with dpg.child_window(height=400):
                        with dpg.tab_bar():
                            with dpg.tab(label="ChangeLog"):
                                    dpg.add_text("This is the ChangeLog tab!")
                                    dpg.add_text("Changes will be posted here in tabs!")
                                    with dpg.group(horizontal=True):
                                            dpg.add_text("Current version:")
                                            dpg.add_text(f"{CURRENTBUILD[1]} {CURRENTBUILD[0]}",tag="CURRENTBUILD_TEXT",color=(250,255,50))
                                    dpg.add_text(f"Released: {CURRENTBUILD[2]}")
                                    with dpg.group(horizontal=True):
                                            dpg.add_text("Direct contact:")
                                            hyperlink("Fumo Friday Official", "https://twitter.com/friday_fumo")
                            with dpg.tab(label="Beta 1"):
                                    dpg.add_text("Hi and welcome to our first build to github, we decided that it's finally time to release a public version as months of work have gone into this launcher and we are eager to keep working on it!",wrap=500)
                                    dpg.add_text("Launcher for all Touhou related games and fan games",bullet=True,wrap=500)
                                    dpg.add_text("Library system to create, edit, and remove game libraries",bullet=True,wrap=500)
                                    dpg.add_text("Ability to add, edit, and remove games with their information",bullet=True,wrap=500)
                                    dpg.add_text("Start games with or without patches with thcrap small support",bullet=True,wrap=500)
                                    dpg.add_text("Support for launching PC-98 games",bullet=True,wrap=500)
                    dpg.add_separator()
                    dpg.add_button(label="Close",user_data=True,callback=lambda:dpg.configure_item(item="ChangelogWindow",show=False),width=-1)
                    
                with dpg.window(label="Confirm action",width=600,height=250,tag="ConfirmClearPath",show=False):
                    with dpg.group():
                        dpg.add_text("This window's purpose is erase and clear all games path from all libraries\nCreate a backup before any desired change\nOnce you clear the path you can share the libraries, then you can apply your backup again to the libraries folder.")
                        dpg.add_separator()
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Clear all paths",callback=ClearAllGamesPath)
                            dpg.add_button(label="Cancel",callback=lambda:dpg.configure_item(item="ConfirmClearPath",show=False))
    
def GamesCreator():
    with dpg.window(label="Games Creator",tag="AddGames",no_resize=True,pos=(705, 20), width=350, height=425):
        with dpg.menu_bar(parent=dpg.last_item()):
            with dpg.menu(label="Presets"):
                dpg.add_menu_item(label="Touhou Puppet Dance Performance - Shard of Dreams",user_data=1,callback=PresetsGame)
                dpg.add_menu_item(label="Touhou Luna Nights",user_data=2,callback=PresetsGame)
                dpg.add_menu_item(label="Labyrinth Of Touhou - Gensoukyo And The Heaven-piercing Tree",user_data=3,callback=PresetsGame)
                dpg.add_menu_item(label="Fantasy Maiden Wars",user_data=4,callback=PresetsGame)
                dpg.add_menu_item(label="Touhou Sky Arena Matsuri Climax",user_data=5,callback=PresetsGame)
        
        dpg.add_text("Add games:")
        dpg.add_separator()
        dpg.add_text("*Requiered")
        dpg.add_input_text(label="Game title",width=150,tag="GameTitleInput")
        dpg.add_checkbox(label="Is it installed?",tag="GameInstalledCheckbox",callback=lambda sender,app_data: dpg.configure_item(item="GamePathInput",enabled=app_data))
        dpg.add_input_text(label="Game path folder",width=150,tag="GamePathInput",enabled=False)
        dpg.add_separator()
        dpg.add_text("-Optional")
        dpg.add_checkbox(label="Is the game patched?",tag="GamePatchedCheckbox",callback=lambda sender,app_data: dpg.configure_item(item="GamePatchedPathInput",enabled=app_data))
        dpg.add_input_text(label="Game patched path folder",width=150,tag="GamePatchedPathInput",enabled=False)
        dpg.add_input_text(label="Description",multiline=True,tab_input=True,height=30,width=150,tag="GameDescriptionInput")
        dpg.add_input_text(label="Developer",width=150,tag="GameDeveloperInput")
        dpg.add_input_text(label="Publisher",width=150,tag="GamePublisherInput")
        dpg.add_input_text(label="Released",width=150,tag="GameReleasedInput")
        dpg.add_input_text(label="Genre",width=150,tag="GameGenreInput")
    #                 NewGameId = input("Id(assign a number): ") # The NewGameId should be incremental of how many games are in a library but ok.
    #                 NewGameCover = input("Cover art:")
        dpg.add_input_text(label="Abbreviation",width=150,tag="GameAbbreviationInput")
    #                 NewGameNumber = input("Number(Assing a number): ")
        #dpg.add_input_text(label="Character",width=150,tag="GameMCInput")
        dpg.add_combo(items=Libraries,tag="ComboLibraries")
        dpg.add_button(label="Create new game",callback=AddGame)
        dpg.add_text(default_value="",tag="GameCreationStatus")
    dpg.bind_item_theme("AddGames",input_text_Visible)

dpg.set_primary_window("MainWindow",True)

def InfoWindow():
    with dpg.window(label="How the library works",tag="InfoWindow",no_resize=True,pos=(40, 20), width=650, height=425):
        with dpg.tab_bar():
            with dpg.tab(label="Class game"):
                dpg.add_text("class Game")
                dpg.add_separator()
                dpg.add_text(wrap=600,default_value="This is a Python class called 'Game' that helps keep track of information about video games. The class has a few different attributes, like the game's title, whether it's installed on your computer, and the file path to the game's executable file (the '.exe' file).\n\nThere are also some optional attributes that can be added, like a brief description of the game, the developer and publisher of the game, and the genre of the game.,\n\nThere are also some methods included, like one that computes the hash (a unique identifier) of the game's executable file (either the patched or unpatched version), and another that computes the hash of the patched file.")
                dpg.add_separator()
                dpg.add_text("Game example")
                with dpg.table(header_row=True, row_background=False,resizable=True):

                    dpg.add_table_column(label="Class game attributes",width_fixed=True, init_width_or_weight=150)
                    dpg.add_table_column(label="Value")
                    dpg.add_table_column(label="Info",width_fixed=True, init_width_or_weight=100)

                    with dpg.table_row():
                        dpg.add_text("Title")
                        dpg.add_input_text(readonly=True,default_value="Touhou 6 - Embodiment of Scarlet Devil",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("This is the title of the game.")
                    
                    with dpg.table_row():
                        dpg.add_text("Installed")
                        dpg.add_input_text(readonly=True,default_value="True",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("This will be true if the user inputed a location for the .exe\n\nIf it's not installed the it will be false.")
                    
                    with dpg.table_row():
                        dpg.add_text("Patched")
                        dpg.add_input_text(readonly=True,default_value="True",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("Same as last one but this time is about patched games, almost every touhou official games if not all are patched with an english version\nThis patched bool checks if 'thcrap' exists on the game folder or if the english version exists.")

                    with dpg.table_row():
                        dpg.add_text("Library")
                        dpg.add_input_text(readonly=True,default_value="Assigned to Official Games",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("This is not that important but it an identifier whenever there are duplicated games, this way we can see wich game is assigned to wich library.")

                    with dpg.table_row():
                        dpg.add_text("Unpatched file")
                        dpg.add_input_text(readonly=True,default_value="C:\\Games\\Touhou Games\\Touhou 6 - Embodiment of Scarlet Devil\\th06.exe",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("The absolute path for the unpatched .exe file, this usually is the .exe game as many fan games aren't patched or only have 1 exe.\nSo this is far important value than the patched file.\n\nIf this is not filled then the launcher will not start the game.")

                    with dpg.table_row():
                        dpg.add_text("Patched file")
                        dpg.add_input_text(readonly=True,default_value="C:\\Games\\Touhou Games\\Touhou 6 - Embodiment of Scarlet Devil\\th06e.exe",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("The same as above but to launch a patched version, many touhou games have more than one .exe, one is for the original version and the other is a patched english version.")

                    with dpg.table_row():
                        dpg.add_text("Description")
                        dpg.add_input_text(readonly=True,default_value="A thick scarlet mist is covering Gensokyo; it blocks out the sun, which causes affected areas to become cold. Our heroines believe the culprit lives in the newly-materialized Scarlet Devil Mansion, and so they depart with the goal of “questioning” those who live there.",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("This is a description of the game, usually it's about the story.")

                    with dpg.table_row():
                        dpg.add_text("Developer")
                        dpg.add_input_text(readonly=True,default_value="Team Shanghai Alice",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("Displays the developer of the game.")

                    with dpg.table_row():
                        dpg.add_text("Publisher")
                        dpg.add_input_text(readonly=True,default_value="Team Shanghai Alice",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("Displays the publisher of the game.")

                    with dpg.table_row():
                        dpg.add_text("Released")
                        dpg.add_input_text(readonly=True,default_value="September 22, 2002",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("Displays the released time of the game.")

                    with dpg.table_row():
                        dpg.add_text("Genre")
                        dpg.add_input_text(readonly=True,default_value="Bullet Hell",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("Displays the genre of the game.")

                    with dpg.table_row():
                        dpg.add_text("Id")
                        dpg.add_input_text(readonly=True,default_value="6",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("Now, this 'id' thing is more of less useless, i used this in early versions and now i don't need it but i keep it just in case-\nthe purpose was to identify each game without the title but i think there's a better way of doing that with something like '#tags'.")

                    with dpg.table_row():
                        dpg.add_text("Cover")
                        dpg.add_input_text(readonly=True,default_value="th06.jpg",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("This is the .jpg or .png of the cover art image of the game to be displayed inside the GUI.")

                    with dpg.table_row():
                        dpg.add_text("Abbreviation")
                        dpg.add_input_text(readonly=True,default_value="EoSD",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("This is the abbreviation of the game")

                    with dpg.table_row():
                        dpg.add_text("Number")
                        dpg.add_input_text(readonly=True,default_value="6",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("This is similar to the ID value, this time is incremental")

                    with dpg.table_row():
                        dpg.add_text("Character")
                        dpg.add_input_text(readonly=True,default_value="Flandre Scarlet",width=-1)
                        dpg.add_text(default_value="(?)",color=[255,255,0])
                        with dpg.tooltip(dpg.last_item()):dpg.add_text("This goes with the characters in the cover art, it used in the Cover value to know wich characters show in the cover art.")
                dpg.add_text("More can be added, there can be a DLC's, languages ,multiplayer and price attributes.")

with dpg.theme() as input_text:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (35, 35, 35), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 35), category=dpg.mvThemeCat_Core)

with dpg.theme() as input_text_Visible:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (45, 45, 45), category=dpg.mvThemeCat_Core)

with dpg.theme() as Red_TitleBgActive:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (135, 0, 0), category=dpg.mvThemeCat_Core)

#dpg.bind_item_theme("LibraryNameInput",input_text_Visible)

dpg.set_viewport_small_icon(CurrentDirectory+"\\TohoPortalSmall.ico")
dpg.set_viewport_large_icon(CurrentDirectory+"\\TohoPortal.ico")

with dpg.theme(tag="hyperlinkTheme"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 0, 0, 0])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 0, 0, 0])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [29, 151, 236, 25])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [29, 151, 236])

dpg.set_exit_callback(callback=lambda:print("GUI Closed"))
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()