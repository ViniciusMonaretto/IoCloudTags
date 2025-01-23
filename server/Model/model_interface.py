class ModelInterface:
    _id: int
    def getCollectionName(self) -> str:
        pass

    def getModelObject(self) -> dict[str, object]:
        pass

    def setModelObject(self, model_gen_object: dict[str, object]):
        pass

    def toStr(self) -> str:
        pass
    
    def __str__(self):
        return self.toStr()