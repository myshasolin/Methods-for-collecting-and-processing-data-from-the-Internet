from telethon import TelegramClient
from dotenv import load_dotenv, find_dotenv
import time
import os

load_dotenv(find_dotenv())
api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')

client = TelegramClient('test_tg', api_id, api_hash)


async def main():
    # me = await client.get_me()
    dialogs = await client.get_dialogs()
    print('название всех групп: ')
    for dialog in dialogs:
        print(dialog.name)
    group_name = input('\n\nсюда название группы или чата: ')
    for dialog in dialogs:
        # это писать сообщения и медиа качать
        if dialog.title == group_name:
            # # написать сообщение в группу или чат:
            # await dialog.send_message('ляляля')

            # вывести переписку:
            async for message in client.iter_messages(dialog):
                # скачать медиа:
                if message.media:
                    await message.download_media('media')
                print(f'{message.date}: {message.text}')
                time.sleep(1)

    #     # посмотреть список участников группы
    #     if dialog.title == group_name:
    #         members = await client.get_participants(dialog)
    # for num, user in enumerate(members):
    #     print(f'{num+1}) {user.first_name} {user.last_name}')


with client:
    client.loop.run_until_complete(main())
