class Notes():
    
    def __init__(self):
        self.mainNotesPath = "storage/mnote.x"
        self.sideNotesPath = "storage/snote.x"
    
    def getFileContent(self, path):
        content = ""
        with open(path, 'r') as _file:
            content = _file.read() 
        return content

    def getMainNotes(self):
        return self.getFileContent(self.mainNotesPath)
    
    def getSideNotes(self):
        return self.getFileContent(self.sideNotesPath)

    def saveToFile(self, path, content):
        with open(path, "w+") as _file:
            _file.write(content)

    def saveMainNotes(self, content):
        self.saveToFile(self.mainNotesPath, content)
    
    def saveSideNotes(self, content):
        self.saveToFile(self.sideNotesPath, content)
