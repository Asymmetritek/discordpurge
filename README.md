# discordpurge
A tool for purging messages from DM chats in Discord

## Warning
This tool operates as a self-bot, when interacting with the Discord API, as it requires the permission to delete messages in DM chats.

The discord.py documentation for [discord.Client.login](https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.login) notes:
> Warning:
> Logging on with a user token is against the Discord [Terms of Service](https://support.discordapp.com/hc/en-us/articles/115002192352) and doing so might potentially get your account banned.
> **Use this at your own risk.**

**USE DISCORDPURGE AT YOUR OWN RISK!**

## Rationale
* Discord does not provide any mechanism to bulk delete messages in a DM chat and it is very time-consuming to delete even 10s of messages manually in the Discord client.
* Discord does not delete your historical messages if you delete your Discord account and does not provide this as an option at the point of account deletion.
* Even if you could choose to delete your historical messages when deleting your Discord account, it wouldn't allow you to only purge messages in specific DM chats.

#### Note for the Discord development team (if you are reading this):
GDPR provides a [right to erasure](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-erasure/) under [Article 17](https://gdpr-info.eu/art-17-gdpr/)
and it might be more convenient to provide in-client functionality (similar to that provided by this tool) than deal with "requests for erasure" that are submitted verbally or in writing.

Please consider either:
* a) adding better support for users to manage their historical chat data (whether during account deletion or not)
* b) modifying the Discord Terms of Service to allow the use of self-bots in limited use cases

## Usage
As per the docstring in [discordpurge.py](https://github.com/Asymmetritek/discordpurge/blob/master/discordpurge.py):

```
Usage:
    discordpurge.py [-q | --quiet] [--after=<utc_datetime>] [--before=<utc_datetime>] <target>

Options:
    -q --quiet  Disable interactive confirmation check
```
*[note: [docopt](https://github.com/docopt/docopt) is dope!]*

* `<target>`: required `name#discriminator` (e.g. `"example#1234"`) of a target with which you share a DM chat
* `[--after=<utc_datetime>]` optional argument to specify a datetime in order to delete messages after this time. If unspecified, the script will delete messages after May 13th 2015 (the Discord initial release date).
* `[--before=<utc_datetime>]` optional argument to specify a datetime in order to delete messages before this time. If unspecified, the script will delete messages up to the present UTC datetime.
* `[-q | --quiet]` optional - by default, the script will ask the user to interactively confirm the purge with a message that displays the window of time that messages will be purged within. Use this option to disable the interactive check.

### auth_token.txt
`discordpurge` requires the user to provide their authentication token in `auth_token.txt`.

The decision to load the token from a file rather than have it passed as a command-line parameter or request it interactively was made for both ease-of-use (not having to copy-paste the token every time the tool is run) and to prevent the sensitive token being left in the command history.

#### Methodology
1. Open Discord (either the web application or desktop application)
2. Use `CTRL + SHIFT + I` to open Developer Tools
3. Select the `Network` tab and search for `/api`. Reload (with `F5`) if necessary to capture the network requests.
4. Select any of the requests under Name and select `Headers`
5. Find the `authorization` header under `Request Headers`
6. Copy and paste the value for the `authorization` header into `auth_token.txt` (creating it if it doesn't exist in the same directory as `discordpurge.py`)

##### Notes:
* *Do not share your token with anyone who you wouldn't be willing to give full access to your Discord account.*
* *Be very wary to keep your authorization token secret - discordpurge makes no attempt whatsoever to protect this token whilst it is in `auth_token.txt`*:
  * *It would be inadvisable to use this tool from a directory that is accessible by other users*
  * *It would be inadvisable to use this tool in environments (e.g. Windows AD domains) where potentially malicious staff with Administrator privileges may be able to access your user directory*
  * *The token is stored in plaintext in `auth_token.txt` and would therefore be discoverable by any competent adversary performing an inspection of an unencrypted storage medium - seriously consider using full disk encryption all of the time and/or securely erasing `auth_token.txt` after using this tool*
* *Be extremely wary about providing your token to any tool where you can't inspect the source code (e.g. an executable) as it could be a trojan that exfiltrates your token to a malicious adversary*

## Potential Future Work
* Extending discordpurge to support deleting messages in [Private Group Channels](https://discordpy.readthedocs.io/en/latest/api.html#groupchannel)
* Extending discordpruge to support deleting messages in [Guild Text Channels](https://discordpy.readthedocs.io/en/latest/api.html#textchannel)
