config_file = r'''
token = "bot_token"  # The token for the bot.
owners = []  # List of owner IDs - these people override all permission checks.
dm_uncaught_errors = true  # Whether or not to DM the owners when unhandled errors are encountered.
user_agent = ""  # A custom string to populate Bot.user_agent with.
guild_settings_prefix_column = "prefix"  # Used if multiple bots connect to the same database and need to seperate their prefixes.
ephemeral_error_messages = true  # Whether or not error messages [from slash commands] should be ephemeral.
owners_ignore_check_failures = true  # Whether or not owners ignore check failures on messages.

# These are used with the on_message event. As such, they will likely soon be deprecated.
default_prefix = "!"  # The prefix for the bot's commands.
cached_messages = 1000  # The number of messages to cache within the bot.

# These are used by non-global commands. As such, they may be removed when the message intent becomes privileged.
support_guild_id = 0  # The ID for the support guild - used by `Bot.fetch_support_guild()`.
bot_support_role_id = 0  # The ID used to determine whether or not the user is part of the bot's support team - used for `.checks.is_bot_support()` check.

# Event webhook information - some of the events (noted) will be sent to the specified url.
[event_webhook]
    event_webhook_url = ""
    [event_webhook.events]  # If you use true then your `event_webhook_url` will be used.
        guild_join = false
        guild_remove = false
        shard_connect = false
        shard_disconnect = false
        shard_ready = false
        bot_ready = false
        unhandled_error = true

# The intents that the bot should start with
[intents]
    guilds = true  # Guilds - Used for guild join/remove, channel create/delete/update, Bot.get_channel, Bot.guilds, Bot.get_guild. This is REALLY needed.
    members = false  # Members (privileged intent) - Used for member join/remove/update, Member.roles, Member.nick, User.name, Bot.get_user, Guild.get_member etc.
    bans = false  # Bans - Used for member ban/unban.
    emojis = false  # Emojis - Used for guild emojis update, Bot.get_emoji, Guild.emojis.
    integrations = false  # Integrations - Used for guild integrations update.
    webhooks = false  # Webhooks - Used for guild webhooks update.
    invites = false  # Invites - Used for invite create/delete.
    voice_states = false  # Voice states - Used for voice state update, VoiceChannel.members, Member.voice.
    presences = false  # Presences (privileged intent) - Used for member update (for activities and status), Member.status.
    guild_messages = false  # Guild messages (privileged intent) - Used for message events in guilds.
    dm_messages = false  # DM messages (privileged intent) - Used for message events in DMs.
    guild_reactions = false  # Guild reactions - Used for [raw] reaction add/remove/clear events in guilds.
    dm_reactions = false  # DM reactions - Used for [raw] reaction add/remove/clear events in DMs.
    guild_typing = false  # Guild typing - Used for the typing event in guilds.
    dm_typing = false  # DM typing - Used for the typing event in DMs.

# Data used to send API requests to whatever service. If these are set, vote links will be added via the `/vote` command.
[bot_listing_api_keys]
    topgg_token = ""  # The token used to post data to top.gg.
    discordbotlist_token = ""  # The token used to post data to discordbotlist.com.

# The info command is the slash command equivelant of "help", giving all relevant data.
[bot_info]
    enabled = true
    content = """
        Here you should give a basic description of your bot and what it does.
        Since this content will go directly into an embed, you're able to [link text](https://google.com).
        You're also able to __use__ **standard** *markdown*.
        This will also be `.format`ted with your bot instance, so you can do things like {bot.user.id} and that should come out properly.
    """
    thumbnail = ""  # A url to an image to be added to the embed
    image = ""  # A url to an image to be added to the embed

    # These are added as link buttons the bottom of the message.
    # Your bot invite (if enabled) will always be added as the first button.
    [bot_info.links.Website]
        url = "https://example.com/#your_website_url"
        emoji = "\U0001f517"  # You can give emojis too if you want
    [bot_info.links."Support Server"]  # You CAN have multiple words in a label
        url = "https://example.com/#your_guild_invite"
    [bot_info.links.Git]
        url = "https://example.com/#your_git_link"
    [bot_info.links.Donate]
        url = "https://example.com/#your_donate_link"
    [bot_info.links.Vote]
        url = "https://example.com/#your_vote_link"

# Used to generate the invite link.
[oauth]
    enabled = true  # Whether or not an invite link is enabled via the !invite command.
    response_type = ""  # The response type given to the redirect URI.
    redirect_uri = ""  # Where the user should be redirected to upon authorizing.
    client_id = ""  #  If not set then will use the bot's ID.
    scope = "bot"  # The scope that will be generated with the invite link, space seperated (applications.commands for slash).
    permissions = []  # args here are passed directly to discord.Permissions as True.

# This data is passed directly over to `asyncpg.connect()`.
[database]
    enabled = false
    user = "database_username"
    password = "database_password"
    database = "database_name"
    host = "127.0.0.1"
    port = 5432

# This data is passed directly over to `aioredis.connect()`.
[redis]
    enabled = false
    host = "127.0.0.1"
    port = 6379
    db = 0

[shard_manager]
    enabled = false
    host = "127.0.0.1"
    port = 8888

# The data that gets shoves into custom context for the embed.
[embed]
    enabled = false  # Whether or not to embed messages by default.
    content = ""  # Default content to be added to the embed message.
    colour = 0  # A specific colour for the embed - 0 means random.
    [embed.author]
        enabled = false
        name = "{ctx.bot.user}"
        url = ""  # The url added to the author.
    [[embed.footer]]  # An array of possible footers.
        text = "Add the bot to your server! ({ctx.clean_prefix}invite)"  # Text to appear in the footer.
        amount = 1  # The amount of times this particular text is added to the pool.

# What the bot is playing
[presence]
    activity_type = "playing"  # Should be one of 'playing', 'listening', 'watching', 'competing'
    text = ""
    status = "online"  # Should be one of 'online', 'invisible', 'idle', 'dnd'
    include_shard_id = true  # Whether or not to append "(shard N)" to the presence text; only present if there's more than 1 shard
    [presence.streaming]  # This is used to automatically set the bot's status to your Twitch stream when you go live
        twitch_usernames = []  # The username of your Twitch.tv channel
        twitch_client_id = ""  # Your client ID - https://dev.twitch.tv/console/apps
        twitch_client_secret = ""  # Your client secret

# UpgradeChat API key data - https://upgrade.chat/developers
[upgrade_chat]
    client_id = ""
    client_secret = ""

# Statsd analytics port using the aiodogstatsd package
[statsd]
    host = "127.0.0.1"
    port = 8125  # This is the DataDog default, 9125 is the general statsd default
    constant_tags.service = ""  # Put your bot name here - leave blank to disable stats collection
'''
