import discord
from discord.ext import commands
import pyowapi
from pymongo import MongoClient

from GerardTheWizard import btmongo

cluster = MongoClient(btmongo)

battletags = cluster["discord"]["battletags"]


class OverwatchCommmands(commands.Cog):

    def __init__(self, Gerard):
        self.Gerard = Gerard

    @commands.command()
    async def register(self, ctx, *, bt):
        stats = battletags.find_one({"id": ctx.author.id})
        if bt.find("#") == -1:
            await ctx.send("That is not a valid battletag.")
        else:
            if not ctx.message.author.bot:
                if stats is None:
                    newuser = {"id": ctx.author.id, "bt": bt}
                    battletags.insert_one(newuser)
                    await ctx.send(f"I have registered the battletag **{bt}** for user **{ctx.author.name}**.")
                else:
                    bt = stats["bt"]
                    await ctx.send(
                        f"User **{ctx.message.author.name}** is already registered to the battletag **{bt}**.\n please use -unregister to clear your battletag.")

    @commands.command()
    async def unregister(self, ctx):
        stats = battletags.find_one({"id": ctx.author.id})
        if not ctx.message.author.bot:
            if stats is None:
                await ctx.send(
                    "You have yet to register a battletag please use -register to register a battletag to your id.")
            else:
                oldbt = stats["bt"]
                bt = {"bt": oldbt}
                battletags.delete_one(bt)
                await ctx.send(f"I have cleared the battle tag {oldbt} for user **{ctx.author.name}**.")

    @commands.command()
    async def battletag(self, ctx):
        stats = battletags.find_one({"id": ctx.author.id})
        if not ctx.message.author.bot:
            if stats is None:
                await ctx.send(
                    "You have yet to register a battletag please use -register to register a battletag to your id.")
            else:
                bt = stats["bt"]
                await ctx.send(f"User **{ctx.author.name}** is currently registered as **{bt}**")

    @commands.command()
    async def owprofile(self, ctx):
        stats = battletags.find_one({"id": ctx.author.id})
        if stats is None:
            await ctx.send("You are not registered please use -Register to register your battletag.")
        else:
            bt = stats["bt"]
            await ctx.send(f"Gathering statistics for the battletag **{bt}**, this may take a moment.")
            player = await pyowapi.get_player_async(bt)
            if not player.success:
                await ctx.send(f"The battletag **{bt}** does not exist please check your registry.")
            else:
                tanksr = player.competitive_tank
                damageesr = player.competitive_damage
                supportsr = player.competitive_support
                if tanksr <= 0:
                    tankrank = "<:xd:890463620943712316>"
                if 1 <= tanksr <= 1500:  # determine tank emoji
                    tankrank = "<:bronze:913682407331340309>"
                if 1500 <= tanksr <= 1999:
                    tankrank = "<:silver:913682586151313428>"
                if 2000 <= tanksr <= 2499:
                    tankrank = "<:gold:913682604107124746>"
                if 2500 <= tanksr <= 2999:
                    tankrank = "<:platinum:913682637313409054>"
                if 3000 <= tanksr <= 3499:
                    tankrank = "<:diamond:913682620691394581>"
                if 3500 <= tanksr <= 3999:
                    tankrank = "<:master:913682683169746944>"
                if 4000 <= tanksr <= 5000:
                    tankrank = "<:grandmaster:913682804720672788>"

                if damageesr <= 0:
                    damagerank = "<:xd:890463620943712316>"
                if 1 <= damageesr <= 1500:  # determine damage emoji
                    damagerank = "<:bronze:913682407331340309>"
                if 1500 <= damageesr <= 1999:
                    damagerank = "<:silver:913682586151313428>"
                if 2000 <= damageesr <= 2499:
                    damagerank = "<:gold:913682604107124746>"
                if 2500 <= damageesr <= 2999:
                    damagerank = "<:platinum:913682637313409054>"
                if 3000 <= damageesr <= 3499:
                    damagerank = "<:diamond:913682620691394581>"
                if 3500 <= damageesr <= 3999:
                    damagerank = "<:master:913682683169746944>"
                if 4000 <= damageesr <= 5000:
                    damagerank = "<:grandmaster:913682804720672788>"

                if supportsr <= 0:
                    supportrank = "<:xd:890463620943712316>"
                if 1 <= supportsr <= 1500:  # determine support emoji
                    supportrank = "<:bronze:913682407331340309>"
                if 1500 <= supportsr <= 1999:
                    supportrank = "<:silver:913682586151313428>"
                if 2000 <= supportsr <= 2499:
                    supportrank = "<:gold:913682604107124746>"
                if 2500 <= supportsr <= 2999:
                    supportrank = "<:platinum:913682637313409054>"
                if 3000 <= supportsr <= 3499:
                    supportrank = "<:diamond:913682620691394581>"
                if 3500 <= supportsr <= 3999:
                    supportrank = "<:master:913682683169746944>"
                if 4000 <= supportsr <= 5000:
                    supportrank = "<:grandmaster:913682804720672788>"

                em = discord.Embed(title=f"Overwatch Stats For Player: {player.player_name}",
                                   description=f'Level: {player.actual_level}\n  Prestige: {player.prestige}\n'
                                               f'  Private: {player.private}\n  Endorsment: {player.endorsement}\n',
                                   color=ctx.author.color)
                em.set_thumbnail(
                    url="https://external-preview.redd.it/5Ow3RDQQGkwzzFC60j5_PjFPQ2hd11E2etWQIb3WcRE.jpg?auto=webp&s=191b7cfe6531fca11c8c72bd77074c9b7e850946")
                em.add_field(name="SR", value=f"Tank: {player.competitive_tank} {tankrank}\n"
                                              f"Damage: {player.competitive_damage} {damagerank}\n"
                                              f"Support: {player.competitive_support} {supportrank}\n")
                em.add_field(name="Competitive Stats",
                             value=f" Total games played: {player.competitive_games_played}\n Games won: {player.competitive_games_won}\n Cards: {player.competitive_cards}\n"
                                   f"Total medals: {player.competitive_medals}\n Gold medals: {player.competitive_medals_gold}\n"
                                   f"Silver medals: {player.competitive_medals_silver}\n Bronze medals: {player.competitive_medals_bronze}\n")
                em.add_field(name="Quickplay Stats",
                             value=f"Games won: {player.quickplay_games_won}\n Cards: {player.quickplay_cards}\n"
                                   f"Total medals: {player.quickplay_medals}\n Gold medals: {player.quickplay_medals_gold}\n"
                                   f"Silver medals: {player.quickplay_medals_silver}\n Bronze medals: {player.quickplay_medals_bronze}\n")
                await ctx.send(embed=em)


def setup(Gerard):
    Gerard.add_cog(OverwatchCommmands(Gerard))
