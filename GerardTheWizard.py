import discord
import discord.ext.commands.errors
from discord.ext import commands, tasks
import json
import os
from itertools import cycle

with open('config.json') as f:  # implement over our config variables
    data = json.load(f)
    token = data["TOKEN"]
    prefix = data["PREFIX"]
    ownerid = data["OWNER_ID"]
    jackid = data["JACK"]
    # databases
    mongo = data["MONGO"]
    btmongo = data["BTMONGO"]
    abmongo = data["ABMONGO"]

Gerard = commands.Bot(
    command_prefix=prefix,
    intents=discord.Intents.all()
)  # set bot prefix to what it is in config and instantiate bot and tell it to use custom help command instead of default

Gerard.remove_command("help")  # remove default help command

status = cycle(['-Help', 'Mixing potions', 'I see you!', 'Remember kids Gerard sees all!', 'Fear me!',
                # create list of statuses to be cycled
                'Torturing those in my way!', 'Practicing spells', 'Destroying families', 'Creating chaos!'])


# cog load command that only specific role can use
@Gerard.command()
@commands.has_role('Zeriss 💕😍😎')
async def load(ctx, extension):
    Gerard.load_extension(f'cogs.{extension}')
    await ctx.send(f"{extension} loaded")


@load.error  # if missing role
async def lacking_permission_load(ctx,
                                  error):  # if user does not have designated role this error runs and sends to chat
    if isinstance(error, discord.ext.commands.errors.MissingRole):
        await ctx.send("You do not have the skills to do that chump.")


@Gerard.command()  # unload cog commmand
@commands.has_role('Zeriss 💕😍😎')
async def unload(ctx, extension):
    Gerard.unload_extension(f'cogs.{extension}')
    await ctx.send(f"{extension} unloaded")


@unload.error  # if missing role
async def lacking_permission_unload(ctx,
                                    error):  # if user does not have designated role this error runs and sends to chat
    if isinstance(error, discord.ext.commands.errors.MissingRole):
        await ctx.send("You do not have the skills to do that chump.")


@Gerard.command()  # shut down commmand
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()
    print('shutting down')


@shutdown.error
async def not_master(ctx, error):
    if isinstance(error, discord.ext.commands.NotOwner):
        await ctx.send('You are not my master!')


# get cogs and remove .py from string
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        Gerard.load_extension(f'cogs.{filename[:-3]}')


@tasks.loop(seconds=300)  # create task that changes bot activity every 5 minutes
async def change_status():
    await Gerard.change_presence(activity=discord.Game(next(status)))


@Gerard.event
async def on_ready():  # when bot is ready
    change_status.start()  # start change status task
    print("Gerard Ready to cast.")  # sends to config


@Gerard.event  # if command is not found error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('I cannot cast that spell since it doesnt exist.')


if __name__ == "__main__":
    Gerard.run(token)  # runs bot from token
