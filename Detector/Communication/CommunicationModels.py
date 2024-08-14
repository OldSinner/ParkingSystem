import json
from typing import Optional, Union
from Helpers.const import *
class BrokerModel:
    def __init__(self) -> None:
        self.Response = False;
        self.ActionResponse = ""
        self.Status = "Success"
        self.Body = ""
    def __init__(self, json_input: str) -> None:
        # Parse the JSON string
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON data") from e

        # Set default values
        self.Response = False
        self.ActionResponse = ""
        self.Status = "Success"
        self.Body = ""

        # Update with values from JSON data
        self.Response = data.get('Response', self.Response)
        self.ActionResponse = data.get('ActionResponse', self.ActionResponse)
        self.Status = data.get('Status', self.Status)
        self.Body = data.get('Body', self.Body)
    def __repr__(self) -> str:
        return (f"BrokerModel(Response={self.Response}, "
                f"ActionResponse='{self.ActionResponse}', "
                f"Status='{self.Status}', "
                f"Body='{self.Body}')")
    
class GateSignal:
    def __init__(self, GateNumber, Type):
        self.GateNumber = GateNumber
        self.Action = GATE_OPENCLOSE_ACTION
        self.Type = Type
    def to_dict(self):
        return {
            'GateNumber': self.GateNumber,
            'Action': self.Action,
            'Type': self.Type,
        }

    def to_json(self):
        return json.dumps(self.to_dict())
