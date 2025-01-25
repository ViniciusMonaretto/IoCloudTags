from abc import ABC, abstractmethod

class ModelInterface(ABC):
    _id: int

    @abstractmethod
    def getCollectionName(self) -> str:
        pass

    @abstractmethod
    def getModelObject(self) -> dict[str, object]:
        pass

    @abstractmethod
    def setModelObject(self, model_gen_object: dict[str, object]):
        pass

    @abstractmethod
    def toStr(self) -> str:
        pass
    
    def __str__(self):
        return self.toStr()