from Model.user_model import User
from Model.tag_mark_model import TagMark

from Model.model_interface import ModelInterface

class DatabaseConfigModel:
    def __init__(self, jsonConfig: object):
        self.name = jsonConfig["name"]
        self.createCommand = jsonConfig["createCommand"]
        self.model: ModelInterface = from_string_get_model(self.name)


def from_string_get_model(model_str) -> ModelInterface: 
    if model_str == "Users":
        return User
    if model_str == "TagMarks":
        return TagMark
    return None