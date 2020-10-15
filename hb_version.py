class VersionInfo():
    
    def __init__(self):
        self.appName = "Hummingbird"
        self.appVersion = "0.3"
        self.dbVersion = 1

    def app_name(self):
        return self.appName

    def app_version(self):
        return self.appVersion