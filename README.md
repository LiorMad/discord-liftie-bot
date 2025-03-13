# discord-liftie-bot
Relying on https://github.com/pirxpilot/liftie, this Discord bot is able to retrieve ski area lift status and display them in Discord with a command.

Very much WIP, and for fun.

The concept is to "cache" https://liftie.info/ on demand to avoid loading their website using `fetch_lift_status_from_liftie.py`.

It downloads information to `data/lifts_status.json`.

Of course, you will need your own `BOT_TOKEN` in some `.env` file, in the following format:
```
BOT_TOKEN=YOUR_TOKEN_FROM_discord.com/developers/applications
```

Then, `liftie-bot.py` simply responds to (slash commands) `/lift <resort>` commands and autocompletes them.

For example:

`/lifts` and start typing `loaf`, the bot will filter all resorts with `loaf`, such as `sugarloaf`. 

There is also a (**outdated**) node.js version of the script.

Also added are test files:
`fetch_lift_status_from_local.py` and `liftie.html`.

It should be easy enough to create a Docker image out of these files and use the image, but it's out of scope for now (though it's tested and it works).
