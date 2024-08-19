import json
from Helpers.const import *
from Communication.ActionEnums import *
from datetime import datetime
from version import __version__


class GateEvent:
    def __init__(self) -> None:
        self.Success = False
        self.Error = "Default Model"
        self.Action = 0
        self.ActionType = 0
        self.Body = ""
        self.EventOccuredDate = datetime.now().strftime(JSON_DATE_FORMAT)

    def __init__(self, json_input: str) -> None:
        # Parse the JSON string
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
        self.EventOccuredDate = datetime.now().strftime(JSON_DATE_FORMAT)

        # Update with values from JSON data
        self.Success = data.get("Success", self.Success)
        self.Error = data.get("Error", self.Error)
        self.Action = data.get("Action", self.Action)
        self.ActionType = data.get("ActionType", self.ActionType)
        self.Body = data.get("Body", self.Body)
        self.EventOccuredDate = data.get("EventOccuredDate", self.EventOccuredDate)

    def __repr__(self) -> str:
        return (
            f"ActionResponse("
            f"Success={self.Success}, "
            f"Error='{self.Error}', "
            f"Action='{self.Action}', "
            f"ActionType='{self.ActionType}', "
            f"Body='{self.Body}')"
        )

    def to_dict(self):
        return {
            "Success": self.Success,
            "Error": self.Error,
            "Action": self.Action,
            "ActionType": self.ActionType,
            "Body": self.Body,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class ActionRequested:
    def __init__(self, json=None):
        if json is None:
            try:
                data = json.loads(json)
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSON data") from e
            self.Action = data.get("Action", self.Action)
            self.RequestDate = data.get("RequestDate", self.RequestDate)
        else:
            self.Action = 0
            self.Action = datetime.now().strftime(JSON_DATE_FORMAT)

    def __init__(self, Action):
        self.Action = Action
        self.RequestDate = datetime.now().strftime(JSON_DATE_FORMAT)

    def to_dict(self):
        return {
            "Action": self.Action,
            "RequestDate": self.RequestDate,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class LogMessage:
    def __init__(self, LogType: int, Action: str, Message: str) -> None:
        self.LogType = LogType
        self.Action = Action
        self.Message = Message
        self.Service = "Detector"
        self.Version = str(__version__)

    def to_dict(self):
        return {
            "LogType": self.LogType,
            "Action": self.Action,
            "Message": self.Message,
            "Service": self.Service,
            "Version": self.Version,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


# namespace Logger.Model
# {
#     public class LogMessage
#     {
#         public LogType LogType { get; set; }
#         public string Message { get; set; } = string.Empty;
#         public string Action { get; set; } = string.Empty;
#         public string Version { get; set; } = "0.0.0";
#         public string Service { get; set; } = string.Empty;
#     }

# }
