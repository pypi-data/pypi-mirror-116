import json


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            print(obj)
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)
