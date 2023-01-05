import dataclasses
import json


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class JsonUtils:
    @staticmethod
    def to_json(input_string: str):
        return json.loads(input_string)
