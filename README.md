# Botress
Botress is a Discord Bot for playing music. 

Botress uses a PySimpleGui interface to play songs from a playlist on shuffle. Playlists can be constructed by putting folders inside the Music Assets directory and mp3 files inside these playlist folders.

Since this bot is primarily for personal use. To use this code a bot id must be registered at https://discord.com/developers/applications and then added to the config.json file like so:

{
"token": "Replace this text, between the quotation marks, with the Bot ID"
}

Make sure to enable permissions and privileged gateway intents for your bot at https://discord.com/developers/applications . Botress shouldn't need many permissions to function but Dicord now requires intents to be enabled.
