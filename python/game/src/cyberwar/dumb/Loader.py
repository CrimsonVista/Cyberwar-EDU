from ..core.PickleLoader import PickleLoader, pickle
from ..controlplane.objectdefinitions import ControlPlaneObjectAttribute, Tangible
from ..controlplane.objectdefinitions import ControlPlaneObject

class dumbObjectEnabled(ControlPlaneObjectAttribute):
    REQUIRED = [Tangible]

    def __init__(self, dumbObjectIdentifier):
        super().__init__("dumbObject_enabled")
        self._dumbObjectIdentifier = dumbObjectIdentifier

    def dumbObjectIdentifier(self):
        return self._dumbObjectIdentifier

class dumbObjectLoader(PickleLoader):
    OBJECT_TYPE = "dumb_object"

    @classmethod
    def TableName(cls):
        return "cyberwar_dumb_object_loader"

    DUMBID_TO_OBJECT = {}

    @classmethod
    def GetObjectByDumbID(cls, dumbId):
        return cls.DUMBID_TO_OBJECT.get(dumbId, None)

    def load(self, row):
        objId, objData = row
        object = pickle.loads(objData)
        ControlPlaneObject.OBJECT_ID = max(object.numericIdentifier(), ControlPlaneObject.OBJECT_ID)
        dumbAttr = object.getAttribute(dumbObjectEnabled)
        
        self.DUMBID_TO_OBJECT[dumbAttr.dumbObjectIdentifier()] = object
        ControlPlaneObject.OBJECT_LOOKUP[object.numericIdentifier()] = object

        return object

Loader = dumbObjectLoader

