import discord
import os
from dotenv import load_dotenv as ld
import sql_fn
from datetime import datetime, timedelta, timezone

ld()

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
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

    sql_fn.get_user(message.author.id, message.author.name)

    if message.content == "/mypoint":
        sql_fn.get_point(message.author.id)
        await message.reply(f"{message.author.mention}さんのポイントは{sql_fn.get_point(message.author.id)}です。")
        return

    sql_fn.add_point_on_message_send(message.author.id)


@tree.command(name="give")
async def give_command(interaction: discord.Interaction, to_user: discord.Member, point: int):
    if to_user.bot:
        return
    if interaction.user.bot:
        return
    if point <= 0:
        await interaction.response.send_message("マイナスは使えないよ", ephemeral=True)
        return
    sql_fn.get_user(interaction.user.id, interaction.user.name)
    sql_fn.get_user(to_user.id, to_user.name)
    nowpt = sql_fn.get_point(interaction.user.id)
    if nowpt < point:
        await interaction.response.send_message(f"your point,{nowpt} , is not enough. ", ephemeral=True)
        return
    sql_fn.move_point_on_given(interaction.user.id, to_user.id, point)
    await interaction.response.send_message("your point has been moved.", ephemeral=True)
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
