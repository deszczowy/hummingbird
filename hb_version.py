class VersionInfo():
    
    dbVersion = 5

    def __init__(self):
        self.appName = "Hummingbird"
        self.appVersion = "0.8"

    def app_name(self):
        return self.appName

    def app_version(self):
        return self.appVersion