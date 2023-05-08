from typing import Callable
from .interfaces.bus_inspector import IBusInspector 
from .interfaces.bus_inspector import ListObjectsOperation, GetOperation

class InspectorBus(IBusInspector):
    def __init__(self) -> None:
        self._handlers = {}
        
    def handler(self, type: str)->Callable:
        def decorator(function):
            if not type in self._handlers:
                self._handlers[type] = [function]
            else:
                self._handlers[type].append(function)
            return function
        return decorator
    
    def handle(self, obj: ListObjectsOperation | GetOperation = None):
        otype = obj.__class__.__name__ if obj else 'ListBucketsOperation'
        returns = []
        for handler_def in self._handlers.get(otype, []):
            if not obj:
                results = handler_def()
            else:
                results = handler_def(obj)
            if results:
                returns.append(results)
        return returns