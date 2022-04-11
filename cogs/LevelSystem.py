import discord
from discord.ext import commands
from pymongo import MongoClient

import GerardTheWizard
from GerardTheWizard import mongo

no_xp_channels = [767319326763515904, 767326283729207317, 775292474154680350, 772367700466073628, 767320898965340181,
                  899796663818936370, 524032705080590360]

no_send_channels = [707255270354714676]
cluster = MongoClient(mongo)

leveling = cluster["discord"]["leveling"]


class LevelSystem(commands.Cog):

    def __init__(self, Gerard):
        self.Gerard = Gerard

    @commands.Cog.listener()
    async def on_ready(self):
        print("level system ready.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.channel.id in no_xp_channels:
            stats = leveling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "xp": 100}
                    leveling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    leveling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                            break
                        lvl += 1
                    xp -= ((50 * (lvl - 1) ** 2) + (50 * (lvl - 1)))
                    if xp == 0:
                        if not message.channel.id in no_send_channels:
                            await message.channel.send(f"Im impressed {message.author.mention}")
                            embed = discord.Embed(description=f"{message.author.mention}")
                            embed.add_field(name=f"You are now level:", value=f"{lvl}")
                            embed.set_thumbnail(url=message.author.avatar_url)
                            await message.channel.send(embed=embed)
                            # send to fathers instead
                        else:
                            channel = GerardTheWizard.Gerard.get_channel(385577225145155594)
                            await channel.send(f"Im impressed {message.author.mention}")
                            embed = discord.Embed(description=f"{message.author.mention}")
                            embed.add_field(name=f"You are now level:", value=f"{lvl}")
                            embed.set_thumbnail(url=message.author.avatar_url)
                            await channel.send(embed=embed)

    @commands.command()
    async def rank(self, ctx):
        stats = leveling.find_one({"id": ctx.author.id})
        if stats is None:
            embed = discord.Embed(description="Hmph you have not talked yet, so no levels yet!", color=ctx.author.color)
            await ctx.channel.send(embed=embed)
        else:
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                    break
                lvl += 1
            xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
            boxes = int((xp / (200 * ((1 / 2) * lvl))) * 20)
            rankings = leveling.find().sort("xp", -1)
            for x in rankings:
                rank += 1
                if stats["id"] == x["id"]:
                    break
            embed = discord.Embed(title="{}'s level stats".format(ctx.author.name), color=ctx.author.color)
            embed.add_field(name="Name", value=ctx.author.mention, inline=True)
            embed.add_field(name="Xp", value=f"{xp}/{int(200 * ((1 / 2) * lvl))}", inline=True)
            embed.add_field(name="Rank", value=f"{lvl}")
            embed.add_field(name="Progress", value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:",
                            inline=False)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        rankings = leveling.find().sort("xp", -1)
        i = 1
        embed = discord.Embed(title="My top subjects:")
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                tempxp = x["xp"]
                embed.add_field(name=f"{i}: {temp.name}", value=f"Total Xp: {tempxp}", inline=False)
                i += 1
            except:
                pass
            if i == 11:
                break
        await ctx.channel.send(embed=embed)


def setup(Gerard):
    Gerard.add_cog(LevelSystem(Gerard))
