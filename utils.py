# coding=utf-8
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, Literal

from telethon.tl.patched import MessageService
from telethon.tl.types import Channel, User, Message, Chat


@dataclass
class UserSender(object):
    type: Literal["User"]
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]


@dataclass
class ChannelSender(object):
    type: Literal["Channel"]
    id: int
    channel_name: Optional[str]


def parse_sender(
    sender: Union[User, Channel]
) -> Union[UserSender, ChannelSender, None]:
    if isinstance(sender, User):
        return UserSender(
            type="User",
            id=sender.id,
            username=sender.username,
            first_name=sender.first_name,
            last_name=sender.last_name,
            phone=sender.phone
        )
    elif isinstance(sender, Channel):
        return ChannelSender(
            type="Channel",
            id=sender.id,
            channel_name=sender.username,
        )
    elif sender is None:
        return None
    else:
        raise ValueError("Unknown sender info! {}".format(sender))


def parse_chat_name(
    chat: Union[User, Chat, Channel]
) -> Optional[str]:
    if isinstance(chat, User):
        return " ".join(
            [i for i in
             [
                 chat.username,
                 chat.first_name,
                 chat.last_name,
                 chat.phone
             ] if i is not None])
    elif isinstance(chat, Channel):
        return chat.title
    if isinstance(chat, Chat):
        return chat.title
    elif chat is None:
        return None
    else:
        raise ValueError("Unknown chat info! {}".format(chat))


@dataclass
class EsDoc(object):
    message_id: int
    chat_id: int
    chat_name: Optional[str]
    date: datetime
    day_of_week: int
    sender: Union[UserSender, ChannelSender, None]
    reply_to_id: Optional[int]
    message: Optional[str]
    grouped_id: Optional[int]

    is_service_message: bool

    has_media: bool
    has_audio: bool
    has_contact: bool
    has_document: bool
    has_file: bool
    has_geo: bool
    has_gif: bool
    has_photo: bool
    has_poll: bool
    has_sticker: bool
    has_video: bool
    has_voice: bool
    has_forward: bool


def message_to_doc(message: Union[MessageService, Message]) -> EsDoc:
    return EsDoc(
        message_id=message.id,
        chat_id=message.chat_id,
        chat_name=parse_chat_name(message.chat),
        date=message.date,
        day_of_week=message.date.weekday() + 1,
        sender=parse_sender(message.sender),
        reply_to_id=message.reply_to_msg_id,
        message=message.text,
        grouped_id=message.grouped_id,
        is_service_message=isinstance(message, MessageService),
        has_media=message.media is not None,
        has_audio=message.audio is not None,
        has_contact=message.contact is not None,
        has_document=message.document is not None,
        has_file=message.file is not None,
        has_geo=message.geo is not None,
        has_gif=message.gif is not None,
        has_photo=message.photo is not None,
        has_poll=message.poll is not None,
        has_sticker=message.sticker is not None,
        has_video=message.video is not None,
        has_voice=message.voice is not None,
        has_forward=message.forward is not None
    )
