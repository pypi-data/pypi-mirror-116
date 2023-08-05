"""
Copyright (c) 2021 Philipp Scheer
"""


import time
from jarvis_sdk import Security


class NLU():
    """NLU helper class to attach NLU event handlers"""

    handlers = {}
    """A dictionary containing all registered handlers"""

    @staticmethod
    def _get(skillNameToGet, intentNameToGet):
        """Get routes from array, else return the default route"""
        endpoints = []
        for (skillName, intentName, id) in NLU.handlers:
            endpoint = NLU.handlers[(skillName, intentName, id)]
            if skillNameToGet == skillName or skillNameToGet == "*":
                if intentNameToGet == intentName or intentNameToGet == "*":
                    endpoints.append(endpoint)
        if len(endpoints) == 0:
            return [NLU.default_endpoint]
        return endpoints


    @staticmethod
    def emit(skill: str, intent: str, *args, **kwargs) -> set:
        """Emit a NLU event with given arguments  
        Returns a tuple with `(True|False, object result)`"""
        start = time.time()
        try:
            endpoints = NLU._get(skill, intent)
            print(endpoints, NLU.handlers)
            result = None
            for endpoint in endpoints:
                try:
                    res = endpoint(*args, **kwargs)
                except Exception as e:
                    res = e
                if res is not None:
                    result = res
            print(result)
            return (True, result)
        except Exception as e:
            return (False, str(e))

    @staticmethod
    def default_endpoint(*args, **kwargs):
        """This is the default endpoint and gets handled if no function was found for NLU event"""
        raise Exception("Endpoint not found")

    @staticmethod
    def on(skill: str, intent: str):
        """Decorator to listen to NLU event  
        [See usage](#NLU)"""
        try:
            def decor(func):
                def wrap(*args, **kwargs):
                    res = func(*args, **kwargs)
                    return res
                id = Security.id(64)
                while (skill, intent, id) in NLU.handlers:
                    id = Security.id(64)
                NLU.handlers[(skill, intent, id)] = wrap
                return wrap
            return decor
        except Exception as e:
            raise e

    @staticmethod
    def get_slot_value(output: dict, slot_name: str, orElse=None, raw=False):
        for slot in output["slots"]:
            if slot["slotName"] == slot_name:
                return slot["rawValue"] if raw else slot["value"]["value"]
        return orElse