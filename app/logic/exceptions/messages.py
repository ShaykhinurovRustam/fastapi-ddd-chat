from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class DublicateChatTitleException(LogicException):
    title: str
    
    @property
    def message(self):
        return f'Chat with "{self.title}" title already exists'