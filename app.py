import json
class App:
    reading = False
    char = ""
    text = ""
    other_text = ""
    lang = "english"
    old_text = ""
    def __init__(self, ignore_fingers_path, bind_map_path):
        self.ignore_fingers = json.load(open(ignore_fingers_path))
        self.bind_map = json.load(open(ignore_fingers_path))
        