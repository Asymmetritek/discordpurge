"""discordpurge

Usage:
    discordpurge.py <target> <after>
"""
import asyncio
import datetime
import sys
from pathlib import Path

import discord
from docopt import docopt
from dateutil.parser import parse as dt_parse
from dateutil.parser._parser import ParserError
from dateutil.tz import tzutc, tzlocal


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
        print(f"Identifying DM channel with recipient '{name}#{number}'...")
        try:
            dm_channel = list(c for c in dm_channels
                              if c.recipient.name == name and c.recipient.discriminator == number)[0]
        except IndexError:
            raise Exception(f"No recipient '{name}#{number}' found in DMs")
        # Acquire message history from after specified date
        print(f"Deleting messages sent after {after_dt} UTC...")
        async for msg in dm_channel.history(limit=None, after=after_dt):
            # If the message was written by me and is not a system message
            if msg.author == client.user and msg.type == discord.MessageType.default:
                counter += 1
                print("*", end="", flush=True)
                await msg.delete()
        print(f"\n{counter} messages deleted.")
    except asyncio.CancelledError:
        print(f"\nPurge cancelled after {counter} messages deleted.")
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

    # Parse the after argument into a datetime object with dateutil and convert to UTC
    after_dts = args["<after>"]
    try:
        after_dt = dt_parse(after_dts)
    except ParserError:
        print(f"Error: could not parse <after> datetime '{after_dts}'")
        sys.exit(1)
    # If after_dt doesn't contain timezone info, assume user local timezone
    if not after_dt.tzinfo:
        after_dt = after_dt.replace(tzinfo=tzlocal())
    # Convert the after_dt from local time to UTC time (and make naive again to meet discord.py requirement)
    after_dt = after_dt.astimezone(tzutc()).replace(tzinfo=None)

    client.run(token, bot=False)
