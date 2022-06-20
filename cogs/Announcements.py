import datetime

import discord
from discord.ext import commands


class Announcements(commands.Cog):
    def __init__(self, Gerard):
        self.Gerard = Gerard

    @commands.Cog.listener()
    async def on_ready(self):
        print('announcement system ready')

    @commands.command()
    @commands.has_any_role('Disciples of Zeriss', 'Parliment-of-Turkey')
    async def announcement(self, ctx, *, announcement=None):

        if announcement is None:
            await ctx.send('How do you expect me to make an announcement if you did not type anything!')

        # create string variables that are necessary for creating announcement

        event_title = str()
        event_date = str()
        event_start_time = str()
        event_description = str()
        channel = None

        # boolean variable to check if formatting was successful
        is_formatted = False

        # announcement will be split to -> event_title, event_date, event_start_time, event_description, channel

        params_from_message = announcement.split("$")
        try:
            event_title = params_from_message[0]
            event_date = params_from_message[1]
            event_start_time = params_from_message[2]
            event_description = params_from_message[3]
            channel = discord.utils.get(ctx.guild.channels, name=params_from_message[4].strip())
            is_formatted = True
        except Exception as e:
            print(e)
            await ctx.send('You are missing a parameter!')
            await ctx.send(
                'proper syntax is ``-announcement event title $ event date (m/d/y) $ event start time (time am/pm) $ event description $ channel name to send to(must be exact)``')

        if is_formatted:
            embed = discord.Embed(title=event_title, description="Click on reactions to RSVP!",
                                  color=ctx.author.color)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="Event Description", value=event_description)
            embed.add_field(name="When:", value=event_date)
            embed.add_field(name="Starts at:", value=event_start_time)
            embed.set_footer(text=f'Created on {datetime.datetime.now().strftime("%b %d, %Y")} at {datetime.datetime.now().strftime("%H:%M")}')
            await channel.send(f'@here {ctx.message.author.name} has created an announcement')
            msg = await channel.send(embed=embed)
            await msg.add_reaction('\U0001F44D')
            await msg.add_reaction('\U0001F44E')


def setup(Gerard):
    Gerard.add_cog(Announcements(Gerard))
