class ModelInterface:
    def getCollectionName(self) -> str:
        pass

    def getModelObject(self) -> dict[str, object]:
        pass

    def setModelObject(self, model_gen_object: dict[str, object]):
        pass