#!/usr/bin/env bash

set -e

for i in "$@"; do
  case $i in
    -f=*|--dialog-ids-file=*)
      INPUT_FILE="${i#*=}"
      shift # past argument=value
      ;;
    -e=*|--elasticsearch=*)
      ELASTIC="${i#*=}"
      shift # past argument=value
      ;;
    -i=*|--index-prefix=*)
      INDEX_PREFIX="${i#*=}"
      shift # past argument=value
      ;;
    -ai=*|--api-id=*)
      API_ID="${i#*=}"
      shift # past argument=value
      ;;
    -ah=*|--api-hash=*)
      API_HASH="${i#*=}"
      shift # past argument=value
      ;;
    -*|--*)
      echo "Unknown option $i"
      exit 1
      ;;
    *)
      ;;
  esac
done

if [ "${INPUT_FILE}" = "" ]; then
    echo "Input file argument is required: [-f=file] [--dialog-ids-file=file]"
    exit 1
fi

if [ "${ELASTIC}" = "" ]; then
    echo "Elasticsearch argument is required: [-e=https://elastic.com] [--elasticsearch=https://user:password@elastic.com]"
    exit 1
fi

if [ "${INDEX_PREFIX}" = "" ]; then
    echo "Index prefix argument is required: [-i=tg-history-] [--index-prefix=tg-history-]"
    exit 1
fi

if [ "${API_ID}" = "" ]; then
    echo "Api id argument is required: [-ai=123456789] [--api-id=123456789]"
    exit 1
fi

if [ "${API_HASH}" = "" ]; then
    echo "Api hash argument is required: [-ah=0123456789abcdef] [--api-hash=0123456789abcdef]"
    exit 1
fi

echo "INPUT_FILE    = ${INPUT_FILE}"
echo "ELASTIC       = ${ELASTIC}"
echo "INDEX_PREFIX  = ${INDEX_PREFIX}"
echo "API_ID        = ${API_ID}"
echo "API_HASH      = ${API_HASH}"

grep -v '^#' "${INPUT_FILE}" | while read -r line; do
    dialog_id="$line"
    echo "Dumping dialog - ${dialog_id}"
    python3 ./dump_history.py --api-id="${API_ID}" --api-hash="${API_HASH}" --chat-id="${dialog_id}" --es-url="${ELASTIC}" --es-index-prefix="${INDEX_PREFIX}"
done