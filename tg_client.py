# coding=utf-8
from singleton_decorator import singleton
from telethon import TelegramClient


@singleton
def tg_client(
    session_name: str,
    api_id: int,
    api_hash: str,
) -> TelegramClient:
    if any([1 for i in [session_name, api_id, api_hash] if i is None]):
        raise ValueError("Telegram client is not initialized!")
    return TelegramClient(session_name, api_id, api_hash)
