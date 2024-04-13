from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.entities.base import BaseEntity
from domain.events.messages import NewMessageRecievedEvent
from domain.values.messages import Text, Title


@dataclass
class Message(BaseEntity):
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
    text: Text
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'Message') -> bool:
        return self.oid == __value.oid
    
@dataclass
class Chat(BaseEntity):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True
    )
    
    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, __value: 'Chat') -> bool:
        return self.oid == __value.oid
    
    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(NewMessageRecievedEvent(
            message_text=message.text.as_generic_type(),
            chat_oid=self.oid,
            message_oid=message.oid
        ))