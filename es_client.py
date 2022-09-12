# coding=utf-8
from typing import Optional

from elasticsearch import AsyncElasticsearch
from singleton_decorator import singleton


@singleton
def es_client(
    es_url: str,
) -> AsyncElasticsearch:
    return AsyncElasticsearch(hosts=[es_url])


async def search_latest_message_id(
    es: AsyncElasticsearch,
    index_name: str
) -> Optional[int]:
    if not await es.indices.exists(index=index_name):
        print("Index `{}` doesn't exist, loading full history"
              .format(index_name))
        return None
    await es.indices.flush(index=index_name)
    await es.indices.refresh(index=index_name)
    matches = await es.search(body={
        "sort": [
            {
                "date": {
                    "order": "desc",
                    "missing": "_last"
                },
                "message_id": {
                    "order": "desc",
                    "missing": "_last"
                }
            }
        ]
    }, index=index_name, size=1)
    hits = matches["hits"]["hits"]
    if not hits:
        print("Index `{}` is empty, loading full history"
              .format(index_name))
        return None
    latest_msg = hits[0]["_source"]
    print("Latest message id: {} time: {}".format(
        latest_msg["message_id"], latest_msg["date"]))
    return latest_msg["message_id"]
