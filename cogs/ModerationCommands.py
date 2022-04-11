import discord
from discord.ext import commands


class ModCommands(commands.Cog):

    def __init__(self, Gerard):
        self.Gerard = Gerard

    # clear command
    @commands.command(
        name='clear',
        desc="A command that clears the given number of messages\n" + "If none is given it will clear the default amount of 5\n" + "Usage: -clear (amount)"
    )
    @commands.has_any_role('Disciples of Zeriss', 'Parliment-of-Turkey')
    async def clear(self, ctx, amount=5):  # clear command
        await ctx.channel.purge(limit=amount)  # if no amount is specified it clears the last 5 messages or whatever
        # amount is equal to

    @clear.error
    async def lacking_permission_clear(self, ctx,
                                       error):  # if user does not have designated role this error runs and sends to chat
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You do not have the skills to do that chump.")

    # kick command
    @commands.command(
        name='kick', desc="Kicks the mentioned user from the server.\n" + "Usage: -kick (member) (reason)"
    )
    @commands.has_any_role('Disciples of Zeriss', 'Parliment-of-Turkey')
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member is None:
            await ctx.send("Please mention someone to kick")
        if reason is None:
            reason = "Reason was not specified"
        await ctx.send(f'{member.mention} has been kicked.')
        await ctx.guild.kick(member,
                             reason=reason)  # could use ctx.guild.ban(member, reason=reason) here, works the same way though.

    @kick.error
    async def lacking_permission_kick(self, ctx,
                                      error):  # if user does not have designated role this error runs and sends to chat
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You do not have the skills to do that chump.")

    # ban command
    @commands.command(
        name='ban', desc="Bans the mentioned user from the server\n" + "Usage: -ban (member) (reason)")
    @commands.has_any_role('Disciples of Zeriss', 'Parliment-of-Turkey')
    async def ban(self, ctx, *, member: discord.Member = None, reason=None):
        if member is None:
            await ctx.send("Please mention someone to ban")
        if reason is None:
            reason = "Reason was not specified"
        await ctx.send(f'{member.mention} is banned.')
        await ctx.guild.ban(member,
                            reason=reason)  # could use ctx.guild.ban(member, reason=reason) here, works the same way though.

    @ban.error
    async def lacking_permission_ban(self, ctx,
                                     error):  # if user does not have designated role this error runs and sends to chat
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You do not have the skills to do that chump.")

    # unban command
    @commands.command(
        name='unban', desc="Unbans the specified user from the server\n" + "Usage: -unban (username+id)"
    )
    @commands.has_any_role('Disciples of Zeriss', 'Parliment-of-Turkey')
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name}#{user.discriminator} has been unbanned')
                return

    # mute command
    @commands.command()
    @commands.has_any_role('Disciples of Zeriss', 'Parliment-of-Turkey')
    async def mute(self, ctx, member: discord.Member, reason=None):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name='SILENCED')
        if not role:
            role = await guild.create_role(name='SILENCED')

            for channel in guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False
                                              )
        await member.add_roles(role, reason=reason)
        await ctx.send(f'{member} has been silenced for {reason}')
        await member.send(f"You have been silenced in {guild.name} for {reason}.\nPlease do better.")

    @mute.error
    async def mute_lacking_permission(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You do not have the skills to do that chump.")

    # unmute command
    @commands.command()
    @commands.has_any_role('Disciples of Zeriss', 'Parliment-of-Turkey')
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name='SILENCED')

        await member.remove_roles(role)
        await ctx.send(f"{member.mention} has been unsilenced.")
        await member.send(f"You are no longer silenced in {ctx.guild.name}")

    @unmute.error
    async def unmute_lacking_permission(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRole):
            await ctx.send("You do not have the skills to do that chump.")


def setup(Gerard):
    Gerard.add_cog(ModCommands(Gerard))
