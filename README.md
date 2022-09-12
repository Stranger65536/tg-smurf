# Telegram message indexer to Elasticsearch

## Prerequisites

### Upload an index pattern to your elasticsearch

```
PUT _index_template/tg-history
# content of es-index-template.json
```

### install dependencies

```
pip3 install -r requirements.txt
```

## List all the dialogs with their IDs

```
usage: python3 list_chats.py [-h] -i api_id -hs api_hash

optional arguments:
  -h, --help            show this help message and exit
  -i api_id, --api-id api_id
                        App api id from https://my.telegram.org
  -hs api_hash, --api-hash api_hash
                        App api hash from https://my.telegram.org
```

## Dump history of a specific dialog id

```
usage: python3 dump_history.py [-h] -i api_id -hs api_hash -c chat_id -e es_url -ei es_index_prefix

optional arguments:
  -h, --help            show this help message and exit
  -i api_id, --api-id api_id
                        App api id from https://my.telegram.org
  -hs api_hash, --api-hash api_hash
                        App api hash from https://my.telegram.org
  -c chat_id, --chat-id chat_id
                        Id of chat / group / channel to dump
  -e es_url, --es-url es_url
                        Url to elasticsearch with embedded credentials if needed
  -ei es_index_prefix, --es-index-prefix es_index_prefix
                        Es index prefix to use

```