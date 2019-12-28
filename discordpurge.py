"""discordpurge

Usage:
    discordpurge.py <target> <after_date>
"""
import datetime
import sys
from pathlib import Path

import discord
from docopt import docopt


client = discord.Client()


@client.event
async def on_ready():
    try:
        counter = 0
        print(f"Logged in as '{client.user}'")
        # Get DM channels
        print("Acquiring DM channels...")
        dm_channels = (c for c in client.private_channels if isinstance(c, discord.DMChannel))
        # Get specific DM channel by recipient name#number
        print(f"Finding specific DM channel with recipient '{name}#{number}'...")
        dm_channel = list(c for c in dm_channels if c.recipient.name == name and c.recipient.discriminator == number)[0]
        # Acquire message history from after specified date
        print(f"Deleting messages sent after {after_date}...")
        async for msg in dm_channel.history(limit=None, after=after_date):
            # If the message was written by me and is not a system message
            if msg.author == client.user and msg.type == discord.MessageType.default:
                counter += 1
                print("*", end="", flush=True)
                await msg.delete()
        print(f"\n{counter} messages deleted.")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await client.close()


if __name__ == '__main__':
    args = docopt(__doc__)

    # Load the authentication token from auth_token.txt
    token_fp = Path(__file__).parent / Path("auth_token.txt")
    if token_fp.exists():
        print(f"Loading token from '{token_fp.resolve()}'...")
        with token_fp.open("r", encoding="utf-8") as f:
            data = f.read()
            token = data.replace("\n", "")
    else:
        print(f"Error: no 'auth_token.txt' file found in '{token_fp.parent.resolve()}'")
        sys.exit(1)

    # Parse the target argument into name and number variables
    try:
        name, number = args["<target>"].split("#")
    except ValueError:
        print("Error: target must be supplied as 'name#number'")
        sys.exit(1)

    # Parse the after_date argument into a datetime object
    try:
        after_date = datetime.datetime.strptime(args["<after_date>"], "%Y-%m-%d")
    except ValueError:
        print("Error: date required in yyyy-mm-dd (e.g. 2017-09-01) format")
        sys.exit(1)

    try:
        client.run(token, bot=False)
    except KeyboardInterrupt:
        print("Program quit by interrupt")
