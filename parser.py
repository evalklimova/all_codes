import csv
import datetime
from time import sleep
from telethon.sync import TelegramClient
from telethon.errors import UsernameInvalidError, ChannelPrivateError
from telethon.tl.functions.messages import GetHistoryRequest

api_id = 25306827
api_hash = '0f76cb4930822c94df8cb9f7410523a6'
phone = '79313156595'

client = TelegramClient(phone, api_id, api_hash)
client.start()

channel_url = "https://t.me/er_molnia"
channel = client.get_entity(channel_url)

offset_id = 0
limit = 100
all_messages = []

start_date = datetime.datetime(2021, 6, 1)
end_date = datetime.datetime(2021, 9, 20)

while True:
    history = client(GetHistoryRequest(
        peer=channel,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0
    ))
    sleep(1)

    if not history.messages:
        break

    messages = history.messages

    for message in messages:
        if hasattr(message, 'message') and message.message:
            msg_date = message.date.replace(tzinfo=None)
            if msg_date < start_date:
                break
            if msg_date <= end_date:
                all_messages.append((message.message.strip(), msg_date))

    if messages[-1].date.replace(tzinfo=None) < start_date:
        break

    offset_id = messages[-1].id

with open("data_new.csv", "w", encoding="utf-8") as our_file:
    writer = csv.writer(our_file, delimiter=",", lineterminator="\n")
    for message in all_messages:
        writer.writerow([message[0], message[1]])

print("Файл сохранён: data_new.csv")


