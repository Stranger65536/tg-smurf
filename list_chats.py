# coding=utf-8
from argparse import ArgumentParser
from asyncio import run

from tg_client import tg_client


async def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "-i", "--api-id", type=int,
        required=True,
        metavar="api_id", dest="api_id",
        help="App api id from https://my.telegram.org"
    )
    parser.add_argument(
        "-hs", "--api-hash", type=str,
        required=True,
        metavar="api_hash", dest="api_hash",
        help="App api hash from https://my.telegram.org"
    )
    args = parser.parse_args()
    client = tg_client("anon", args.api_id, args.api_hash)
    await client.start()
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        print("Id: {0: <15} Name: '{1}' Title: '{2}'".format(
            dialog.id, dialog.name, dialog.title))

    await client.disconnect()


run(main())
