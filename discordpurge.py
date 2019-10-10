import datetime
import sys
from pathlib import Path

import discord


recipient_name = input("Target (username): ")
after_date = datetime.datetime(2017, 9, 1)

client = discord.Client()


@client.event
async def on_ready():
    try:
        counter = 0
        print(f"Logged in as '{client.user}'")
        # Get DM channels
        print("Acquiring DM channels...")
        dm_channels = (c for c in client.private_channels if isinstance(c, discord.DMChannel))
        # Get specific DM channel by recipient name
        print(f"Finding specific DM channel with recipient '{recipient_name}'...")
        dm_channel = list(c for c in dm_channels if c.recipient.name == recipient_name)[0]
        # Acquire message history from after specified date
        print(f"Deleting messages in history after {after_date}...")
        async for msg in dm_channel.history(limit=None, after=after_date):
            # If the message was written by me and is not a system message
            if msg.author == client.user and msg.type == discord.MessageType.default:
                counter += 1
                print("*", end="", flush=True)
                await msg.delete()
        print(f"\n{counter} messages deleted... Ctrl-C to quit!")
    except Exception as e:
        print(f"{str(e)}... Ctrl-C to quit!")


token = None
token_fp = Path(__file__).parent / Path("bot.token")
with token_fp.open("r", encoding="utf-8") as f:
    token = f.read()
    token = token.replace("\n", "")

try:
    client.run(token, bot=False)
except KeyboardInterrupt:
    print("Program quit by interrupt")
