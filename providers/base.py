from abc import ABC, abstractmethod


class ProviderBase(ABC):

    @abstractmethod
    def run_all(self) -> dict:
        ...
