from datetime import datetime
import pytest

from domain.events.messages import NewMessageRecievedEvent
from domain.exceptions.messages import TextTooLongException
from domain.values.messages import Text, Title
from domain.entities.messages import Chat, Message


def test_create_message_success_short_text():
    text = Text('Hello world')
    message = Message(text=text)
    
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()
    
def test_create_message_success_long_text():
    text = Text('A' * 400)
    message = Message(text=text)
    
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()
    
def test_create_chat_success():
    title = Title("Title")
    chat = Chat(title=title)
    
    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()
    
def test_create_chat_title_too_long():
    with pytest.raises(TextTooLongException):
        title = Title("Title" * 400)
        
def test_add_message_to_chat():
    text = Text('Hello world')
    message = Message(text=text)
    
    title = Title("Title")
    chat = Chat(title=title)
    
    chat.add_message(message=message)
    
    assert message in chat.messages
    
def test_new_message_events():
    text = Text('Hello world')
    message = Message(text=text)
    
    title = Title("Title")
    chat = Chat(title=title)
    
    chat.add_message(message=message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()
    
    
    assert not pulled_events
    assert len(events) == 1, events
    
    new_event = events[0]
    
    assert isinstance(new_event, NewMessageRecievedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_oid == chat.oid
    
    
    