from .model_interface import ModelInterface
    
class Location(ModelInterface):
    _name: str
    _block: int
    _sector: int
    _gateway_uuid: str
    _admin_user_id: int

    def __init__(self):
        self._name = ""
        self._block = None
        self._sector = None
        self._gateway_uuid = None
        self._admin_user_id = None

    def initialize(self, name: str, block: int, sector: int, uuid: str = None, user_admin_id: int = None):
        self._name = name
        self._block = block
        self._sector = sector
        self._gateway_uuid = uuid
        self._admin_user_id = user_admin_id
    
    def getCollectionName(self) -> str:
        return "Locations"

    def getModelObject(self) -> dict[str, object]:
        model = {}
        model["Name"] = self._name 
        model["Block"] = self._block 
        model["Sector"] = self._sector 
        model["GatewayUuid"] = self._gateway_uuid 
        model["AdminUserId"] = self._admin_user_id 

        return model
    
    def setGatewayUuid(self, uuid: str):
        self._gateway_uuid = uuid

    def setModelObject(self, model_gen_object: dict[str, object]):
        self._id = model_gen_object["id"] if "id" in model_gen_object else self._sector
        self._name = model_gen_object["Name"] if "Name" in model_gen_object else self._name
        self._block = model_gen_object["Block"] if "Block" in model_gen_object else self._block
        self._sector = model_gen_object["Sector"] if "Sector" in model_gen_object else self._sector
        self._gateway_uuid = model_gen_object["GatewayUuid"] if "GatewayUuid" in model_gen_object else self._gateway_uuid
        self._gateway_uuid = model_gen_object["AdminUserId"] if "AdminUserId" in model_gen_object else self._admin_user_id
    
    def toStr(self) -> str:
        json = {
            "id": self._id,
            "Name": self._name,
            "Block": self._block,
            "Sector": self._sector,
            "GatewayUuid": self._gateway_uuid,
            "AdminUserId": self._admin_user_id
        }

        return str(json)
    
    def __str__(self):
        return self.toStr()