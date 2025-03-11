# discord-liftie-bot
Relying on https://github.com/pirxpilot/liftie, this Discord bot is able to retrieve ski area lift status and display them in Discord with a command.

Very much WIP, and for fun.

The concept is to "cache" https://liftie.info/ on demand to avoid loading their website using `fetch_lift_status_from_liftie.py`.

It downloads information to `lifts_status.json`.

Of course, you will need your own `BOT_TOKEN` in some `.env` file, in the following format:
```
BOT_TOKEN=YOUR_TOKEN_FROM_discord.com/developers/applications
```

Then, `liftie-bot.py` simply responds to `!lift <resort>` commands.

For example:

`!lifts killington`.

There is also a node.js version of the script.

Also added are test files:
`fetch_lift_status_from_local.py` and `liftie.html`.