import json
from Helpers.const import *
class ActionResponse:
    def __init__(self) -> None:
        self.ReplyTo = ""
        self.Success = False
        self.Error = "Default Model"
        self.Action = ""
        self.Body = ""
    def __init__(self, json_input: str) -> None:
        # Parse the JSON string
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON data") from e

        # Set default values
        self.ReplyTo = ""
        self.Success = False
        self.Error = "Empty Initrialized"
        self.Action = ""
        self.Body = ""


        # Update with values from JSON data
        self.ReplyTo = data.get('ReplyTo', self.ReplyTo)
        self.Success = data.get('Success', self.Response)
        self.Error = data.get('Error', self.Status)
        self.Action = data.get('Action', self.Status)
        self.Body = data.get('Body', self.Body)

    def __repr__(self) -> str:
        return (f"ActionResponse(ReplyTo='{self.ReplyTo}', "
                f"Success={self.Success}, "
                f"Error='{self.Error}', "
                f"Action='{self.Action}', "
                f"Body='{self.Body}')")
    
    def to_dict(self):
        return {
            'ReplyTo': self.ReplyTo,
            'Success': self.Success,
            'Error': self.Error,
            'Action': self.Action,
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
            self.Action = 0
            self.ReplyTo = ""
            self.Action = data.get('Action', self.Action)
            self.ReplyTo = data.get('ReplyTo', self.ReplyTo)
        else:
            self.Action =0
            self.ReplyTo = ""
        
    def __init__(self, Action, ReplyTo : None | str = None):
        self.Action = Action

        if ReplyTo is None:
            self.ReplyTo = APP_NAME
        else:
            self.ReplyTo = ""

    def to_dict(self):
        return {
            'Action': self.Action,
            'ReplyTo': self.ReplyTo,
        }
    def to_json(self):
        return json.dumps(self.to_dict())