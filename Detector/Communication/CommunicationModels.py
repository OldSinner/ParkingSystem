import json
from Helpers.const import *
# class BrokerModel:
#     def __init__(self) -> None:
#         self.Response = False;
#         self.ReplyTo = ""
#         self.Status = "Success"
#         self.Body = ""
#     def __init__(self, Response : bool, ReplyTo: str, Status : str, body: str) -> None:
#         self.Response = Response;
#         self.ReplyTo = ReplyTo
#         self.Status = Status
#         self.Body = body
        
#     def __init__(self, json_input: str) -> None:
#         # Parse the JSON string
#         try:
#             data = json.loads(json_input)
#         except json.JSONDecodeError as e:
#             raise ValueError("Invalid JSON data") from e

#         # Set default values
#         self.Response = False
#         self.ReplyTo = ""
#         self.Status = "Success"
#         self.Body = ""

#         # Update with values from JSON data
#         self.Response = data.get('Response', self.Response)
#         self.ReplyTo = data.get('ReplyTo', self.ReplyTo)
#         self.Status = data.get('Status', self.Status)
#         self.Body = data.get('Body', self.Body)
#     def __repr__(self) -> str:
#         return (f"BrokerModel(Response={self.Response}, "
#                 f"ActionResponse='{self.ReplyTo}', "
#                 f"Status='{self.Status}', "
#                 f"Body='{self.Body}')")
#     def to_dict(self):
#         return {
#             'Response': self.Response,
#             'ActionResponse': self.ReplyTo,
#             'Status': self.Status,
#             'Body': self.Body,
#         }

#     def to_json(self):
#         return json.dumps(self.to_dict())
    

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