from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @property
    @abstractmethod
    def command_key(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, api):
        pass
