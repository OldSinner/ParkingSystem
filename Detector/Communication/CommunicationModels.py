import json
from Helpers.const import *
from Communication.ActionEnums import *
class GateEvent:
    def __init__(self) -> None:
        self.Success = False
        self.Error = "Default Model"
        self.Action = 0
        self.ActionType = 0
        self.Body = ""
    def __init__(self, json_input: str) -> None:
        # Parse the JSON string
        print(json_input)
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON data") from e

        # Set default values
        self.Success = False
        self.Error = "Empty Initrialized"
        self.Action = 0
        self.ActionType = 0
        self.Body = ""


        # Update with values from JSON data
        self.Success = data.get('Success', self.Success)
        self.Error = data.get('Error', self.Error)
        self.Action = data.get('Action', self.Action)
        self.ActionType = data.get('ActionType', self.ActionType)
        self.Body = data.get('Body', self.Body)


    def __repr__(self) -> str:
        return (f"ActionResponse("
                f"Success={self.Success}, "
                f"Error='{self.Error}', "
                f"Action='{self.Action}', "
                f"ActionType='{self.ActionType}', "
                f"Body='{self.Body}')")
    
    def to_dict(self):
        return {
            'Success': self.Success,
            'Error': self.Error,
            'Action': self.Action,
            'ActionType': self.ActionType,
            'Body': self.Body,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

class ActionRequested:
    def __init__(self, json = None):
        if json is None:
            try:
                data = json.loads(json)
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSON data") from e
            self.Action = data.get('Action', self.Action)
        else:
            self.Action =0
        
    def __init__(self, Action):
        self.Action = Action

    def to_dict(self):
        return {
            'Action': self.Action,
        }
    def to_json(self):
        return json.dumps(self.to_dict())