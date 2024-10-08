from abc import ABC, abstractmethod
from enum import Enum

class BasePlugin(ABC):
    @property
    @abstractmethod
    def command_key(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass
    
    @property
    @abstractmethod
    def plugin_type(self) -> Enum:
        pass

    @abstractmethod
    def execute(self, api):
        pass
