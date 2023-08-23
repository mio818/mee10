import discord
import os
from dotenv import load_dotenv as ld
import sql_fn
from datetime import datetime, timedelta, timezone

ld()

TOKEN = os.environ["DISCORD_BOT_TOKEN"]

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print("起動しました")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    sql_fn.get_user(message.author.id, message.author.name)

    if message.content == "/mypoint":
        sql_fn.get_point(message.author.id)
        await message.reply(f"{message.author.mention}さんのポイントは{sql_fn.get_point(message.author.id)}です。")
        return

    sql_fn.add_point_on_message_send(message.author.id)


@client.event
async def on_raw_reaction_add(RawReactionActionEvent):
    """
    リアクションが付与されたときに実行される
    """
    sql_fn.get_user(RawReactionActionEvent.user_id, RawReactionActionEvent.user_name)

    channel = client.get_channel(RawReactionActionEvent.channel_id)

    message_detail = await channel.fetch_message(RawReactionActionEvent.message_id)

    timenow = datetime.now() - timedelta(hours=9)

    timenow_utc = timenow.replace(tzinfo=timezone.utc)

    if timenow_utc - message_detail.created_at <= timedelta(days=3):
        sql_fn.add_point_on_reaction(RawReactionActionEvent.user_id)
    else:
        return


@client.event
async def on_raw_reaction_remove(RawReactionActionEvent):
    sql_fn.get_user(RawReactionActionEvent.user_id, RawReactionActionEvent.user_name)
    sql_fn.sub_point_on_reaction(RawReactionActionEvent.user_id)


client.run(TOKEN)
