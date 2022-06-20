import random

import discord
from discord.ext import commands

from GerardTheWizard import Gerard, jackid


class Commands(commands.Cog):

    def __init__(self, Gerard):
        self.Gerard = Gerard

    # ping command
    @commands.command(
        name='ping', desc="Ping command to check my connection to the server.\n" + "Usage: -ping"
    )
    async def ping(self, ctx):  # latency command to check bot connection
        await ctx.send(f'pong!\nIm currently running at {round(Gerard.latency * 1000)}ms')  # bot replies pong and
        # returns ms ping

    # ask command
    @commands.command(
        name='ask', aliases=['question'], desc="Go on ask me a question.\n" + "Usage: -ask (question)"
    )
    async def ask(self, ctx, *, question):
        replies = ["Yes!", "no.", "maybe.", "maybe so?", "Oh quite so!",  # custom responses
                   "Im a wizard not a therapist.", "don't you think you have any better questions?",

                   "Oh yes certainly!", "I definitely think so my friend!", "Oh most certainly!",
                   "You can definitely think that yes!", "As I think of it, yes.", "probably", "Looks good.",
                   "Yea.", "The magic.. It says yes.",  # positive responses

                   "Hmm, no idea.", "I really do not know.",  # unknown responses
                   "I think you wouldn't like my answer", "I cannot tell you.", "Well uhmm, uhhh, yea?",
                   "That question, is bad.",

                   "Definitely no", "No!", "No.", "My spells say no.",  # bad responses
                   "Im just a wizard stop pestering me.", "Hell no."
                   ]
        await ctx.send(f'Hmm. You ask {question}\n {random.choice(replies)}')

    @ask.error
    async def ask_error(self, ctx, error):  # if bot is provided with no question
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("I need a question in order to answer dummy.")

    # jack command
    @commands.command()
    async def jack(self, ctx, *, msg=None):
        guild = ctx.guild
        jack = await guild.fetch_member(jackid)
        if msg is None:
            await ctx.send('I need a message to send to Jack.')
        else:
            await jack.send(f"Hi Jack you have a message:\n{msg}")
            await ctx.send(f"I have sent Jack your message <:thumbsup:937873042628030494>")

    # anonymous jack system
    @commands.Cog.listener()
    async def on_message(self, message):
        if '-jack' in message.content:
            await message.delete()


def setup(Gerard):
    Gerard.add_cog(Commands(Gerard))
