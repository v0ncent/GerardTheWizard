import discord
from discord.ext import commands
from GerardTheWizard import abmongo
from pymongo import MongoClient

cluster = MongoClient(abmongo)

bugs = cluster["discord"]["bugs"]


class ApexCommands(commands.Cog):
    def __init__(self, Gerard):
        self.Gerard = Gerard

    @commands.Cog.listener()
    async def on_ready(self):
        print("Apex system ready.")

    @commands.command()
    async def addbug(self, ctx, bug_title=None, example_video=None, *, bug_description=None):
        if bug_title is None or bug_description is None:
            await ctx.send("I need a title or description to add to the list.")
        else:
            if not ctx.message.author.bot:
                bug_title = bug_title
                bug_description = bug_description
                example_video = example_video
                buglist = {"Bug Title": bug_title, "Bug Description": bug_description, "Example Video": example_video}
                bugs.insert_one(buglist)
                await ctx.send(
                    f"Thanks for reporting a bug! I have registered **{bug_title}** with the description **{bug_description}** with the link {example_video}")

    @commands.command()
    async def buglist(self, ctx):
        buglist = bugs.find().sort("Bug Title", -1)
        i = 1
        embed = discord.Embed(title="List of Unpatched Apex Bugs")
        for x in buglist:
            try:
                bugtitle = x["Bug Title"]
                bugdescription = x["Bug Description"]
                bugvideo = x["Example Video"]
                embed.add_field(name=f"{i}. {bugtitle}", value=f"{bugdescription}\nLink: {bugvideo}", inline=True)
                i += 1
                if bugtitle is None:
                    await ctx.channel.send("There are no bugs yet!")
            except:
                pass
        embed.set_footer(text=f"There are currently {i - 1} unpatched bugs in Apex Legends Lets go Respawn!")
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def patched(self, ctx, title=None):
        stats = bugs.find_one({"Bug Title": title})
        if title is None:
            await ctx.channel.send('Please provide a bug title to report as patched')
        else:
            title = stats["Bug Title"]
            patched_bug = {"Bug Title": title}
            bugs.delete_one(patched_bug)
            await ctx.channel.send(f"Thanks for reporting **{title}** as patched it has been removed from the list")


def setup(Gerard):
    Gerard.add_cog(ApexCommands(Gerard))
