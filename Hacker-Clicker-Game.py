from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget


formatting = """
<MyScreenManager>:
    StartScreen:
    CreateNewCharacterScreen:
    MainGameScreen:
    
<StartScreen>:
    name: 'start'
    BoxLayout:
        orientation: 'vertical'
        Label:
            color: [218, 10, 17, 1]
            text: root.instructions  
            font_size: 30 
        TextInput:
            id: save_code
            font_size: 28
        Button:
            text: 'Press me to go to the Game Screen'
            on_press: root.load_or_start_new(save_code.text)

<CreateNewCharacterScreen>:
    name: 'character'
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: instr
            size: self.texture_size
            text: root.instructions  
        TextInput:
            id: name
            font_size: 28
        Button:
            text: 'Enter a name for your character'
            on_press: root.create_character(name.text)

<MainGameScreen>:
    name: 'game'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            Label:
                id: stuff_we_own
                text: root.owned
            Label:
                id: display
                text: root.display
            BoxLayout:
                id: infoboxes
                orientation: 'vertical'
                BoxLayout:
                    id: infobox_1
                    orientation: 'horizontal'
                    Label:
                        text: "Top Owned"
                    Button:
                        text: "Button Top"
                BoxLayout:
                    id: infobox_2
                    orientation: 'horizontal'                   
                    Label:
                        text: "Middle Owned"
                    Button:
                        text: "Button Middle"   
                BoxLayout:
                    id: infobox_4
                    orientation: 'horizontal'                   
                    Label:
                        text: "Middle2 Owned"
                    Button:
                        text: "Button Middle2"               
                BoxLayout:
                    id: infobox_3
                    orientation: 'horizontal'    
                    Label:
                        text: "Bottom Owned"   
                    Button:
                        text: "Button Bottom"    
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Hacks'
                on_press: root.hacks()
                on_press: root.add_time(15)   
            Button:
                text: 'Phishing'
                on_press: root.phishing() 
                on_press: root.add_time(50)  
            Button:
                text: 'Sell information' 
                on_press: root.sellHacks()
                on_press: root.add_time(5)             
"""
Builder.load_string(formatting)


class PlayerStatistics:
    def __init__(self, phishing=0, hacks=0, time=0, ascension=0, liquidfunds=0, percent=0):
        self.tracker = percent
        self.wallet = liquidfunds
        self.ascension = ascension
        self.time: int = time
        self.name: str = ""
        self.phishing: int = phishing
        self.hacks: int = hacks
        self.attributeDict = {"PHI": self.phishing, "HAK": self.hacks}

    def set_name(self, username):
        self.name = username

    def increment_phishing(self, amount=1):
        self.phishing = self.phishing + amount

    def increment(self, parameter, amount=1):
        if self.attributeDict.__contains__(parameter):
            self.attributeDict[parameter] = self.attributeDict[parameter] + amount
        else:
            print("That Parameter does not exist")

    def create_from_save(self):
        pass

    def increment_hacks(self, amount=1):
        self.hacks = self.hacks + amount

        pass

    def __str__(self):
        return str(
            "Name: " + self.name + " | " + "time: " + str(self.time)
            + "\n" + "Phishing: " + str(self.phishing)
            + "\n" + "Hacks: " + str(self.hacks)
            + "\n" + "$" + str(self.wallet)
            + "\n" + "Police Tracker: " + str(self.tracker)
        )

    def sellHacks(self, amount=-1, add=10):
        self.hacks = self.hacks + amount
        self.wallet = self.wallet + add

    pass

    def increment_time(self, amount=1):
        self.time = self.time + amount

    pass

    # End Game hopefully
    def policeTracker(self, amount=5):
        # This checks if Phishing is equal to 10 then the police tracker starts
        if self.phishing == 10:
            self.tracker = self.tracker + amount
        else:
            # If Phishing does not equal 10 the police tracker stays zero
            self.tracker = 0


# Create the screen manager = sm
class MyScreenManager(ScreenManager, Widget):
    data = ObjectProperty(PlayerStatistics)


class StartScreen(Screen):
    instructions = StringProperty(str('''
    Welcome to this fun game!
    If you're new to the game or you want to start from the beginning just press the button!
    Otherwise, first paste in your save code, and then press the button to load the game.
    '''))

    def load_or_start_new(self, savedata=''):
        # For now we always start a new game
        if savedata != '':
            self.load_game()
        else:
            self.start_new_game()
        pass

    # Right now load and new do the same thing, but that might change in the future
    def load_game(self):
        self.manager.current = 'character'
        pass

    def start_new_game(self):
        self.manager.current = 'character'
        pass

    pass


class CreateNewCharacterScreen(Screen):
    instructions = StringProperty(str('''
        This world is unlike any world you've known before. Great Things await. But first, you'll need a name...
        '''))
    fail_instructions = StringProperty(str('''
        This world is unlike any world you've known before. Great Things await. But first, you'll need a name...
        FOOLISH MORTAL!!! ENTER A NAME FIRST BEFORE YOU CLICK THE BUTTON. 
        '''))
    data_stats: PlayerStatistics = ObjectProperty(PlayerStatistics)

    def create_character(self, username):
        if username != '':
            self.data_stats = PlayerStatistics()
            self.data_stats.set_name(username)
            self.manager.get_screen('game').display = str(self.data_stats)
            self.manager.current = 'game'
        else:
            self.instructions = self.fail_instructions
        pass

    pass


class MainGameScreen(Screen):
    def get_data(self) -> PlayerStatistics:
        return self.manager.get_screen('character').data_stats

    display = StringProperty()
    owned = StringProperty()
    ads = StringProperty("WRONG ads")
    ads_price = StringProperty("WRONG price")

    # StringProperty("Name: " + "Dummy" + "\n" + "Strength: " + str(Strength))

    def phishing(self):
        stats: PlayerStatistics = self.get_data()
        stats.increment_phishing(1)
        self.display = str(stats)

    def hacks(self):
        stats: PlayerStatistics = self.get_data()
        stats.increment_hacks(1)
        self.display = str(stats)

    def add_time(self, amount):
        stats: PlayerStatistics = self.get_data()
        stats.increment_time(amount)
        self.display = str(stats)

    # Decreases number of Hacks
    def sellHacks(self):
        stats: PlayerStatistics = self.get_data()
        stats.sellHacks()
        self.display = str(stats)


class Dataimporter:
    def __init__(self, string):
        self.data = self.convertStringtoDict(string)

    @staticmethod
    def convertStringtoDict(string: str) -> list:
        """
        I am given a string that contains text hen a colon, then text then a colon then text.
        I want to turn that into a dictionary
        """
        string = string.replace("{", "")
        string = string.replace("}", "")
        string = string.replace("'", "")
        List = string.split(',')
        Dict = []
        for element in List:
            (key, value) = element.split(';')
            Dict[key] = value
        print(Dict)
        return Dict

    @staticmethod
    def convertDicttoString(data: dict) -> str:
        """
        I am given a Dictionary that I want to covert into a String that contains text the a colon,then text then a
        colon then text.
        where the text i a key and the number is the key's value
        """
        return str(data)


class PlayerData:
    # Init normal values, as well as tracker variables for hose values
    def __init__(self, savedatadict: dict = None):
        if savedatadict is not None:
            print(str(savedatadict))
            # Things I want to save?
            self.hacks: int = 0
            self.phishing: int = 0
            self.name: str = ""
        else:
            self.hacks = savedatadict.get('hacks')
            self.phishing = savedatadict.get('phishing')
            self.name = savedatadict.get('name')

    def SaveCurrentData(self):
        data = {'hacks': self.hacks, 'phishing': self.phishing, 'name': self.name}
        print(data)
        return data

    def setName(self, username):
        pass


class WelcomeScreen(Screen):
    instructions = StringProperty(str(''' Welcome to the Android's Hacker Clicker Clone! Hope you have a nice time
     If it's your first time playing, press the button below to continue.
     If you wish to loas a save, type your save code and continue'''))

    # def SaveCurrentData(self):
    #     data = {'hacks': self.hacks, 'phishing': self.phishing, 'name': self.name}
    #     return data
    # Unfinished: Later issue
    def load_or_start_new(self, savedata=''):
        # For now we always start a new game
        if savedata != '':
            self.loadSave(savedata)
        else:
            self.createNewSave()
        pass

    # Right now load and new do the same thing, but that might change in the future
    def loadSave(self, data_string: str):
        dataDict = Dataimporter.convertStringtoDict(data_string)
        # Load in save info
        self.manager.LoadData(dataDict)
        self.manager.current = 'game'
        pass

    def createNewSave(self):
        self.manager.current = 'load'
        pass

    pass


# Save game area
class LoadSaveScreen(Screen):
    defaultText = StringProperty(str('''
        Type in a name for yourself
        '''))
    failText = StringProperty(str('''
        Give yourself a name to continue to play you fast reader. Stop trying to cheat this game
        '''))
    data_stats: PlayerData = ObjectProperty(PlayerData)

    # Load SaveData here
    def LoadData(self, data: dict):
        self.data_stats = PlayerData(data)
        self.manager.get_screen('game').display = str(self.data_stats)


pass


# Create a new save data if text field isn't blank
def createSaveData(self, username):
    if username != '':
        self.data_stats = PlayerData()
        self.data_stats.setName(username)
        self.manager.get_screen('game').display = str(self.data_stats)
        self.manager.current = 'game'
    # Display failText until textbox is no longer empty
    else:
        self.defaultText = self.failText
    pass


pass


def build():
    return MyScreenManager()


class GUIApp(App):

    def build(self):
        return MyScreenManager()


# Entry point into the game
if __name__ == '__main__':
    GUIApp().run()
