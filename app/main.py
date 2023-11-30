import discord
import os
from dotenv import load_dotenv as ld
import sql_fn
from datetime import datetime, timedelta, timezone
from db.db_manager import User, Point
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.db_manager import engine
from db.db_manager import User, Point


engine = create_engine("mysql://root:TpHSWotUTKhL22@db:3306/happyDB")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


ld()


TOKEN = os.environ["DISCORD_BOT_TOKEN"]
TARGET_GUILD_ID = os.environ["TARGET_GUILD_ID"]
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("起動しました")
    await tree.sync()


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.guild:
        return

    # user = User(user_discord_id=message.author.id, user_name=message.author.name)
    # point = Point(user_id=message.author.id)

    # if user.exists():
    #     print("ユーザーが存在します")

    # SessionClass = sessionmaker(engine)  # セッションを作るクラスを作成
    # session = SessionClass()

    # session.add(user)
    # session.commit()

    # if "毛利" in message.content:
    #     await message.reply("毛利監視中")
    #     return

    if message.content == "/mypoint":
        sql_fn.get_point(message.author.id)
        await message.reply(f"{message.author.mention}さんのポイントは{sql_fn.get_point(message.author.id)}です。")
        return

    sql_fn.add_point_on_message_send(message.author.id)


@tree.command(name="mypoint")
async def mypoint_command(interaction: discord.interactions.Interaction):
    user = User(user_discord_id=interaction.user.id, user_name=interaction.user.name)

    if user.exists_or_create():
        await interaction.response.send_message(f"{user.user_name}", ephemeral=False)
    else:
        pass


@tree.command(name="health")
async def give_command(
    interaction: discord.Interaction,
):
    await interaction.response.send_message(f"Health : OK", ephemeral=False)
    return


@client.event
async def on_raw_reaction_add(RawReactionActionEvent):
    """
    リアクションが付与されたときに実行される
    """

    user = await client.fetch_user(RawReactionActionEvent.user_id)
    user_name = user.name

    sql_fn.get_user(RawReactionActionEvent.user_id, user_name)

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
    user = await client.fetch_user(RawReactionActionEvent.user_id)
    user_name = user.name
    sql_fn.get_user(RawReactionActionEvent.user_id, user_name)
    sql_fn.sub_point_on_reaction(RawReactionActionEvent.user_id)


client.run(TOKEN)
