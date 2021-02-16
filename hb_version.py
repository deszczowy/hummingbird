class VersionInfo():
    
    dbVersion = 4

    def __init__(self):
        self.appName = "Hummingbird"
        self.appVersion = "0.7"

    def app_name(self):
        return self.appName

    def app_version(self):
        return self.appVersion