class DatabaseConfigModel:
    def __init__(self, jsonConfig: object):
        self.name = jsonConfig["name"]
        self.createCommand = jsonConfig["createCommand"]
        self.getCommand = jsonConfig["getCommand"]
        self.deleteCommand = jsonConfig["deleteCommand"]
