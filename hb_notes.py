from hb_dir import Directory

class Notes():
    
    def __init__(self):
        self.notesDir = Directory().get_notes_dir()
        self.mainNotes = self.notesDir + "mnote.x"
        self.sideNotes = self.notesDir + "snote.x"
        
    def getFileContent(self, path):
        content = ""
        with open(path, 'a+') as _file:
            _file.seek(0)
            content = _file.read() 
        return content

    def getMainNotes(self):
        return self.getFileContent(self.mainNotes)
    
    def getSideNotes(self):
        return self.getFileContent(self.sideNotes)

    def saveToFile(self, path, content):
        with open(path, "w+") as _file:
            _file.write(content)

    def saveMainNotes(self, content):
        self.saveToFile(self.mainNotes, content)
    
    def saveSideNotes(self, content):
        self.saveToFile(self.sideNotes, content)
