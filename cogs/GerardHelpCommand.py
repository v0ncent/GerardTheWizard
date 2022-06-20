import discord
from discord.ext import commands


class HelpCommand(commands.Cog):

    def __init__(self, Gerard):
        self.Gerard = Gerard

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title="List of Spells", description="Use -help (command) for more information on usage.",
                           color=ctx.author.color)
        em.set_thumbnail(url=ctx.author.avatar_url)
        em.add_field(name="Moderation", value="`clear`,`ban`,`kick`,`unban`,`mute`,`unmute`,`announcement`")
        em.add_field(name="Commands", value="`ask`,`ping`, `rank`, `leaderboard`, `jack`")
        em.add_field(name="Overwatch Commands", value="`register`, `unregister`,`battletag`, `owprofile`")
        em.add_field(name="Apex Commands", value="`addbug`, `buglist`, `patched`")

        await ctx.send(embed=em)

    @help.command()
    async def ask(self, ctx):
        em = discord.Embed(title="Ask", description="Go one ask me a question.", color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Ask (question)")

        await ctx.send(embed=em)

    @help.command()
    async def ping(self, ctx):
        em = discord.Embed(title="Ping", description="Checks my connection to the server.", color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Ping")

        await ctx.send(embed=em)

    @help.command()
    async def ban(self, ctx):
        em = discord.Embed(title="Ban", description="Bans a user from the server.", color=ctx.author.color)

        em.add_field(name="**Usage**",
                     value="-Ban (@member) (reason) note: if no reason is specified it uses default reason")

        await ctx.send(embed=em)

    @help.command()
    async def clear(self, ctx):
        em = discord.Embed(Title="Clear",
                           description="Clears the given number of messages in the channel command is executed in",
                           color=ctx.author.color)

        em.add_field(name="**Usage**",
                     value="-Clear (amount) note: if no amount is given bot clears the last 5 messages")

        await ctx.send(embed=em)

    @help.command()
    async def kick(self, ctx):
        em = discord.Embed(title="Kick", description="Kicks a user from the server.", color=ctx.author.color)

        em.add_field(name="**Usage**",
                     value="-Kick (@member) (reason) note: if no reason is specified it uses default reason")

        await ctx.send(embed=em)

    @help.command()
    async def unban(self, ctx):
        em = discord.Embed(title="Unban", description="Unbans a member from the server", color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Unban (@member) (reason)")

        await ctx.send(embed=em)

    @help.command()
    async def rank(self, ctx):
        em = discord.Embed(title="Rank", description="Shows you your current XP and progress towards leveling up",
                           color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Rank")

        await ctx.send(embed=em)

    @help.command()
    async def leaderboard(self, ctx):
        em = discord.Embed(title="Leaderboard", description="Shows my top ranked subjects", color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Leaderboard")

        await ctx.send(embed=em)

    @help.command()
    async def register(self, ctx):
        em = discord.Embed(title="Register",
                           description="Registers your battletag to your discord id for using overwatch commands",
                           color=ctx.author.color)

        em.add_field(name="**Usage**",
                     value="-Register (Battletag) **important: Must be case sensitive copy battletag is best.**")

        await ctx.send(embed=em)

    @help.command()
    async def unregister(self, ctx):
        em = discord.Embed(title="Unregister",
                           description="Unregisters the current battletag registered to your discord id",
                           color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Unregister")

        await ctx.send(embed=em)

    @help.command()
    async def battletag(self, ctx):
        em = discord.Embed(title="Battletag", description="Shows the currently registered battletag to your discord id",
                           color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Battletag")

        await ctx.send(embed=em)

    @help.command()
    async def owprofile(self, ctx):
        em = discord.Embed(title="Owprofile", description="Shows overwatch statistics to your registered battletag",
                           color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Owprofile")

        await ctx.send(embed=em)

    @help.command()
    async def mute(self, ctx):
        em = discord.Embed(Title="Mute", description="Mutes a member", color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Mute (@member) (reason)")

        await ctx.send(embed=em)

    @help.command()
    async def unmute(self, ctx):
        em = discord.Embed(Title="Unmute", description="Unmuted a unmuted member", color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Unmute (@member)")

        await ctx.send(embed=em)

    @help.command()
    async def jack(self, ctx):
        em = discord.Embed(Title="Jack", description="Send Jack a dm!", color=ctx.author.color)

        em.add_field(name="**Usage**", value="-Jack (message)")

        await ctx.send(embed=em)

    @help.command()
    async def addbug(self, ctx):
        em = discord.Embed(Title="Addbug",
                           description="Report a apex bug to be added to a ongoing list of unpatched bugs",
                           color=ctx.author.color)

        em.add_field(name="**Usage**",
                     value="-addbug (Bug Title) (Link To Video) (Description) **Important:** Title must be one word")

        await ctx.send(embed=em)

    @help.command()
    async def buglist(self, ctx):
        em = discord.Embed(Title="Buglist", description="Shows the list of currently unpatched Apex Bugs",
                           color=ctx.author.color)

        em.add_field(name="**Usage**", value="-buglist")

        await ctx.send(embed=em)

    @help.command()
    async def patched(self, ctx):
        em = discord.Embed(Title="Patched", description="Removes a bug from the bug list for it has been patched",
                           color=ctx.author.color)

        em.add_field(name="**Usage**", value="-patched (bug title)")

        await ctx.send(embed=em)

    @help.command()
    async def announcement(self, ctx):
        em = discord.Embed(Title="Announcement", description="Create an announcement and send it to a specific channel",
                           color=ctx.author.color)

        em.add_field(name="**Usage**",
                     value="-announcement event title $ event date (m/d/y) $ event start time (time am/pm) $ event description $ channel name to send to(must be exact)")

        await ctx.send(embed=em)


def setup(Gerard):
    Gerard.add_cog(HelpCommand(Gerard))
