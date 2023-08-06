import discord
from .Base import generate_column_types


class EconomyAccount:
    def __init__(self, guild: int, member: int, database, table):
        self.guild = guild
        self.member = member
        self.database = database
        self.table = table

    def __str__(self):
        return f"<Account MEMBER={self.member}, GUILD={self.guild}>"

    def __repr__(self):
        return f"<Account GUILD={self.guild}, MEMBER={self.member}, CURRENCY={self.currency}, BANK={self.bank}>"

    def __lt__(self, other):
        return self.net < other.net

    @property
    def __checks(self):
        return EconomyManager.generate_checks(self.guild, self.member)

    @property
    def currency(self):
        return self.database.select(['currency'], self.table, self.__checks)["currency"]

    @property
    def bank(self):
        return self.database.select(['bank'], self.table, self.__checks)["bank"]

    @property
    def net(self):
        return self.bank + self.currency

    def change_currency(self, amount: int):
        self.database.update({'currency': self.currency + amount}, self.table, self.__checks)

    def change_bank(self, amount: int):
        self.database.update({'bank': self.bank + amount}, self.table, self.__checks)


class EconomyManager:
    def __init__(self, database, table, bot):
        self.database = database
        self.table = table
        self.bot = bot
        self.keys = ['guild', 'member', 'currency', 'bank']

        self.__create_table()

    def __create_table(self):
        types = generate_column_types(['snowflake', 'snowflake', 'snowflake', 'snowflake'], type(self.database.database))
        columns = [{'name': x, 'type': y} for x, y in zip(self.keys, types)] if types else None
        self.database.create_table(self.table, columns, True)

    @staticmethod
    def generate_checks(guild: int, member: int):
        return {'guild': guild, 'member': member}

    def create_account(self, member: discord.Member):
        self.database.insertifnotexists({"guild": member.guild.id,
                                         "member": member.id,
                                         "currency": 0,
                                         "bank": 0
                                         },
                                        self.table, self.generate_checks(member.guild.id, member.id))

    def get_account(self, member: discord.Member):
        member_data = self.database.select([], self.table, self.generate_checks(member.guild.id, member.id), True)

        if member_data:
            return EconomyAccount(member.guild.id, member.id, self.database, self.table)

        return None

    def get_leaderboard(self, guild):
        guild_info = self.database.select([], self.table, {'guild': guild.id}, True)
        members = [EconomyAccount(*list(member_info.values())[:2],
                                  database=self.database,
                                  table=self.table) for member_info in guild_info]

        members.sort()
        return members
