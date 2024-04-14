from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(LogicException):
    event_type: type
    
    @property
    def message(self):
        return f"Handlers for {self.event_type} not found"
    
@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type
    
    @property
    def message(self):
        return f"Handlers for {self.command_type} not found"