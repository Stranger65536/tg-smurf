# coding=utf-8
from argparse import ArgumentParser
from asyncio import run
from dataclasses import asdict
from typing import Optional

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_streaming_bulk
from tqdm.asyncio import tqdm

from es_client import es_client, search_latest_message_id
from tg_client import tg_client
from utils import message_to_doc, EsDoc


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
    parser.add_argument(
        "-c", "--chat-id", type=int,
        required=True,
        metavar="chat_id", dest="chat_id",
        help="Id of chat / group / channel to dump"
    )
    parser.add_argument(
        "-e", "--es-url", type=str,
        required=True,
        metavar="es_url", dest="es_url",
        help="Url to elasticsearch with embedded credentials if needed"
    )
    parser.add_argument(
        "-ei", "--es-index-prefix", type=str,
        required=True,
        metavar="es_index_prefix", dest="es_index_prefix",
        help="Es index prefix to use"
    )
    args = parser.parse_args()
    client = tg_client("anon", args.api_id, args.api_hash)
    await client.start()
    dialogs = await client.get_dialogs()
    chat_id = args.chat_id
    es_index_prefix = args.es_index_prefix
    es_url = args.es_url
    target_dialog = [i for i in dialogs if i.id == chat_id]
    index_name = "{}{}".format(es_index_prefix, chat_id)

    if not target_dialog:
        raise ValueError("Chat with id {} not found!".format(chat_id))
    target_dialog = target_dialog[0]

    es: AsyncElasticsearch = es_client(es_url)
    if not await es.ping():
        raise ValueError("Es ping unsuccessful!")

    min_id: Optional[int] = \
        await search_latest_message_id(es, index_name) or 0

    async def generator():
        async for message in tqdm(client.iter_messages(target_dialog,
                                                       reverse=True,
                                                       min_id=min_id)):
            es_doc: EsDoc = message_to_doc(message)
            if pbar is not None:
                pbar.desc = str(es_doc.date)
            yield {
                "_index": index_name,
                "_source": asdict(es_doc),
            }

    progress = async_streaming_bulk(
        es, generator(),
        chunk_size=500,
        max_chunk_bytes=104857600,
        raise_on_error=True,
        raise_on_exception=True,
        yield_ok=True,
    )

    pbar = tqdm(progress)
    async for ok, item in pbar:
        if not ok:
            print("Item index failed: {}".format(item))

    await es.indices.flush(index=index_name)
    await es.indices.refresh(index=index_name)

    await client.disconnect()
    await es.close()


run(main())
