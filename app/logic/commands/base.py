from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


@dataclass(frozen=True)
class BaseCommand(ABC):
    ...

CT = TypeVar(name="CT", bound=BaseCommand)
CR = TypeVar(name="CR", bound=Any)

@dataclass(frozen=True)
class CommandHandler(ABC, Generic[CT, CR]):
    @abstractmethod
    def handler(self, command: CT) -> CR:
        ...
        
    
    