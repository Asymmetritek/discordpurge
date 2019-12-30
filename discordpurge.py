"""discordpurge

Usage:
    discordpurge.py [-q | --quiet] [--after=<utc_datetime>] [--before=<utc_datetime>] <target>

Options:
    -q --quiet  Disable interactive confirmation check
"""
import asyncio
import datetime
import sys
from pathlib import Path

import discord
from docopt import docopt
from dateutil.parser import parse as dt_parse
from dateutil.parser._parser import ParserError


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
        print(f"Deleting messages sent between '{after_dt} UTC' and '{before_dt} UTC'...")
        async for msg in dm_channel.history(limit=None, after=after_dt, before=before_dt):
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
    quiet = True if args["--quiet"] else False

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

    # Parse the after argument, if provided, into a datetime object with dateutil
    after_dts = args["--after"]
    if after_dts:
        try:
            after_dt = dt_parse(after_dts, ignoretz=True)
        except ParserError:
            print(f"Error: could not parse 'after' datetime '{after_dts}'")
            sys.exit(1)
    else:
        # If no after argument provided, purge from Discord initial release date
        after_dt = datetime.datetime(2015, 5, 13)

    # Parse the before argument, if provided, into a datetime object with dateutil
    before_dts = args["--before"]
    if before_dts:
        try:
            before_dt = dt_parse(before_dts, ignoretz=True)
        except ParserError:
            print(f"Error: could not parse 'before' datetime '{before_dts}'")
            sys.exit(1)
    else:
        # If no before argument provided, purge up to present second
        before_dt = datetime.datetime.utcnow().replace(microsecond=0)

    if not quiet:
        i = input(f"Confirm (Y) purge against '{name}#{number}' between '{after_dt} UTC' and '{before_dt} UTC': ")
        if i not in ["y", "Y"]:
            print("Purge rejected.")
            sys.exit(1)

    try:
        client.run(token, bot=False)
    except discord.errors.LoginFailure:
        print(f"Login failure: improper token in '{token_fp.resolve()}'")
