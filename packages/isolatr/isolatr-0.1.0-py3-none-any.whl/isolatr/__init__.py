from asyncio import sleep
from datetime import datetime
from io import StringIO
from json import dumps
from re import compile, I
from typing import Set, TypeVar

from discord import Member, File
from discord.ext.commands import Cog, Context, Bot, MissingPermissions, command, NotOwner, guild_only


T = TypeVar("T")


class Isolatr(Cog):
    def __init__(self, bot: Bot, plevel: str = "administrator") -> None:
        self.bot = bot
        self.plevel = plevel

    def parse_check(self, check: str) -> tuple:
        if check.startswith("!"):
            return ("not", *self.parse_check(check[1:]))

        if check.startswith("match"):
            check = check[6:]

            if check.startswith("name"):
                return ("regex", "name", check[5:])
            if check.startswith("nick"):
                return ("regex", "nick", check[5:])
            return ("regex", "multi", check)

        if check.startswith("date"):
            check = check[5:]

            if check.startswith("range"):
                check = check[6:]

                if check.startswith("join"):
                    check = check[5:].split()

                    return ("date", "range", "join", int(check[0]), int(check[1]))

                if check.startswith("create"):
                    check = check[7:].split()

                    return ("date", "range", "create", int(check[0]), int(check[1]))

            if check.startswith("around"):
                check = check[7:]

                if check.startswith("join"):
                    check = check[5:].split()

                    return ("date", "around", "join", int(check[0]), int(check[1]))

                if check.startswith("create"):
                    check = check[7:].split()

                    return ("date", "around", "create", int(check[0]), int(check[1]))

        if check.startswith("avatar"):
            return ("avatar", check[7:])

        return None

    async def get_matches(self, _members: Set[Member], parsed: tuple) -> Set[Member]:
        members = {m for m in _members}
        if parsed[0] == "regex":
            if parsed[1] == "name":
                members = await self.find_by_re_match_name(members, parsed[2])
            elif parsed[1] == "nick":
                members = await self.find_by_re_match_nick(members, parsed[2])
            else:
                members = await self.find_by_re_match_name(members, parsed[2]) | await self.find_by_re_match_nick(members, parsed[2])
        elif parsed[0] == "date":
            if parsed[1] == "range":
                if parsed[2] == "join":
                    members = await self.find_by_join_date_range(members, parsed[3], parsed[4])
                else:
                    members = await self.find_by_creation_date_range(members, parsed[3], parsed[4])
            else:
                if parsed[2] == "join":
                    members = await self.find_by_join_date_distance(members, parsed[3], parsed[4])
                else:
                    members = await self.find_by_creation_date_distance(members, parsed[3], parsed[4])
        elif parsed[0] == "avatar":
            members = await self.find_by_avatar_hash(parsed[1])
        return members

    @staticmethod
    async def find(seq: Set[T], pred) -> Set[T]:
        results = []
        for item in seq:
            if pred(item):
                results.append(item)
            await sleep(0)
        return set(results)

    async def _pcheck(self, member: Member) -> None:
        if self.plevel == "owner":
            if not await self.bot.is_owner(member):
                raise NotOwner("You must own the bot to perform this action.")
            return
        if not getattr(member.guild_permissions, self.plevel, None):
            raise MissingPermissions(self.plevel)

    @command(name="isolate", hidden=True)
    @guild_only()
    async def isolate(self, ctx: Context, *, command: str) -> None:
        await self._pcheck(ctx.author)

        checks = command.split("\n")
        ichecks = []
        members = {m for m in ctx.guild.members}

        for check in checks:
            parsed = self.parse_check(check)

            if not parsed:
                continue

            if parsed[0] == "not":
                ichecks.append(parsed[1:])
                continue

            members = await self.get_matches(members, parsed)

        for icheck in ichecks:
            members = members - await self.get_matches(members, icheck)

        compiled = {}

        for member in members:
            compiled[str(member.id)] = {
                "name": member.name,
                "discriminator": member.discriminator,
                "nick": member.nick,
                "avatar": member.avatar,
                "joined": member.joined_at.isoformat(),
                "created": member.created_at.isoformat(),
            }

        await ctx.reply(f"Found {len(members)} matching members:", file=File(StringIO(dumps(compiled, indent=2)), filename="members.json"))

    async def find_by_re_match_name(self, members: Set[Member], pattern: str) -> Set[Member]:
        pattern = compile(pattern, I)

        return await self.find(members, lambda m: pattern.search(m.name))

    async def find_by_re_match_nick(self, members: Set[Member], pattern: str) -> Set[Member]:
        pattern = compile(pattern, I)

        return await self.find(members, lambda m: pattern.search(m.nick) if m.nick else False)

    async def find_by_join_date_range(self, members: Set[Member], d_from: int, d_to: int) -> Set[Member]:
        d_from_date = datetime.fromtimestamp(d_from)
        d_to_date = datetime.fromtimestamp(d_to)
        return await self.find(members, lambda m: d_from_date <= m.joined_at <= d_to_date)

    async def find_by_join_date_distance(self, members: Set[Member], d_around: int, distance: int) -> Set[Member]:
        return await self.find_by_join_date_range(members, d_around - distance, d_around + distance)

    async def find_by_creation_date_range(self, members: Set[Member], d_from: int, d_to: int) -> Set[Member]:
        d_from_date = datetime.fromtimestamp(d_from)
        d_to_date = datetime.fromtimestamp(d_to)
        return await self.find(members, lambda m: d_from_date <= m.created_at <= d_to_date)

    async def find_by_creation_date_distance(self, members: Set[Member], d_around: int, distance: int) -> Set[Member]:
        return await self.find_by_creation_date_range(members, d_around - distance, d_around + distance)

    async def find_by_avatar_hash(self, members: Set[Member], avatar: str) -> Set[Member]:
        return await self.find(members, lambda m: m.avatar == avatar)
