import argparse
import json
from typing import Any, Dict

import pychat
import clickhouse_connect


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process ClickHouse and YouTube arguments.")
    
    # ClickHouse arguments
    parser.add_argument('--clickhouse_host', required=True, help='ClickHouse host.')
    parser.add_argument('--clickhouse_port', required=True, type=int, help='ClickHouse port.')
    parser.add_argument('--clickhouse_username', required=True, help='ClickHouse username.')
    parser.add_argument('--clickhouse_password', required=True, help='ClickHouse password.')
    
    # YouTube argument
    parser.add_argument('--video-id', required=True, help='YouTube video ID.')
    
    # Name to differentiate streams
    parser.add_argument('--stream_name', required=True, help='The friendly name of the stream.')
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    clickhouse_host = args.clickhouse_host
    clickhouse_port = args.clickhouse_port
    clickhouse_username = args.clickhouse_username
    clickhouse_password = args.clickhouse_password
    stream_name = args.stream_name
    video_id = args.video_id

    client = clickhouse_connect.get_client(
        host=clickhouse_host, 
        port=clickhouse_port, 
        username=clickhouse_username, 
        password=clickhouse_password
    )
    # Create table if not exists.
    with open("create_table.sql", "r") as f:
        query = f.read()
        client.command(query)
    
    chat = pytchat.create(video_id=video_id)
    

    while chat.is_alive():
        for c in chat.get().sync_items():
        print(f"{c.datetime} [{c.author.name}]- {c.message}")

        json_data = c.json()
        data = json.loads(json_data)
        client.insert('messages', data, column_names=[
            "name",
            "type",
            "id",
            "message",
            "messageEx",
            "timestamp",
            "datetime",
            "elapsedTime",
            "amountValue",
            "amountString",
            "currency",
            "bgColor",
            "author",
        ])

