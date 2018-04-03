from ..core.messages import Request, Response
from ..core.Board import InitializeObjectRequest
from ..core.Layer import Layer as LayerBase

from ..controlplane.objectdefinitions import ControlPlaneObject
from ..controlplane.Layer import ObjectDamagedByMinesEvent

#from .connection import DumbObjectConnectionProtocol
from .Loader import Loader, dumbObjectEnabled

import random


class CreateDumbObjectRequest(Request):
    def __init__(self, sender, *attributes):
        super().__init__(sender, DumbObjectInterfaceLayer.LAYER_NAME,
                         Attributes=attributes)

class CreateDumbObjectResponse(Response):
    pass

class DumbObjectInterfaceLayer(LayerBase):
    LAYER_NAME = "dumbobjectinterface"

    def __init__(self, lowerLayer):
        super().__init__(self.LAYER_NAME, lowerLayer)
        self._objectToID = {}
        self._idToObject = {}

    def getObjectByIdentifier(self, identifier):
        return Loader.GetObjectByDumbID(identifier)

    def _handleRequest(self, req):
        if isinstance(req, CreateDumbObjectRequest):
            dumbObjectIdentifier = random.randint(1, 2**32)
            dumbObjectAttr = dumbObjectEnabled(dumbObjectIdentifier)
            object = ControlPlaneObject(dumbObjectAttr, *req.Attributes)

            Loader.DUMBID_TO_OBJECT[dumbObjectIdentifier] = object

            r = self._lowerLayer.send(InitializeObjectRequest(self._name,
                                                              object,
                                                              Loader.OBJECT_TYPE))
            if not r:
                return r
            return self._requestAcknowledged(req, object, ackType=CreateDumbObjectResponse)

        else:
            return self._requestFailed(req, "Unknown Request")
'''
    def _handleEvent(self, event):
        if isinstance(event, ObjectDamagedByMinesEvent):
            DumbObjectConnectionProtocol.HandleEvent(event.Object, event)
'''

Layer = DumbObjectInterfaceLayer