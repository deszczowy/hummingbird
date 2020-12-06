class VersionInfo():
    
    dbVersion = 3

    def __init__(self):
        self.appName = "Hummingbird"
        self.appVersion = "0.5"

    def app_name(self):
        return self.appName

    def app_version(self):
        return self.appVersion