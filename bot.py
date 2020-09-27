import asyncio

import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from database_api import DatabaseAPI
from parserGSM.parser import ParseGSM

# logging level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# db connection init
db = DatabaseAPI('db.db')

# parser init
parser = ParseGSM('last_title.txt')


# activate subscription
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if db.subscriber_exists(message.from_user.id, True):
        await message.answer("You've already subscribed!")

    elif not db.subscriber_exists(message.from_user.id, True) \
            and not db.subscriber_exists(message.from_user.id, False):
        db.add_subscriber(message.from_user.id, True)
        await message.answer("You subscription is activated. Wait for new reviews!")
    else:
        db.update_subscriptions(message.from_user.id, True)
        await message.answer("You subscription is activated again. Wait for new reviews!")


# deactivate subscription
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if db.subscriber_exists(message.from_user.id, False):
        await message.answer("You weren't subscribed yet.")

    elif db.subscriber_exists(message.from_user.id, True):
        db.update_subscriptions(message.from_user.id, False)
        await message.answer("You subscription is deactivated.")


async def create_post_if_new_review_is_added(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        if parser.new_review_exists():
            # TODO define last review peer number of article, not a title
            parser.update_last_title('last_title.txt')
            new_review = parser.combine_review_info()
            subscriptions = db.get_subscriptions()

            with open(parser.download_image(), 'rb') as photo:
                for s in subscriptions:
                    await bot.send_photo(
                        s[1],
                        photo,
                        caption=new_review['title'] + "\n\n" + new_review['link'],
                        disable_notification=True
                    )


if __name__ == '__main__':
    asyncio.get_event_loop().create_task(create_post_if_new_review_is_added(50))  # 100 sec
    executor.start_polling(dp, skip_updates=True)
