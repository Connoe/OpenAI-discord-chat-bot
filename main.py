import openai
import discord

member_class_list = list()
sys_sets = [
    "You are a helpful assistant",
    "You are a helpful assistant, who makes every response like a biblical verse in the style of the king james bible",
]


class Players:
    def __init__(self, member):
        self.system_set = 0
        self.int_chat_log = [
            {"role": "system", "content": sys_sets[self.system_set]},
        ]
        self.member = member


def ask(question, member):
    chats = member.int_chat_log
    chats.append({"role": "user", "content": question})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chats,
        temperature=0.7,
        max_tokens=250
    )
    m = completion.choices[0].message.content
    chats.append({"role": "assistant", "content": m})
    # m = "Prompt: " + question + " \nResponse: " + m
    return m


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        for guild in client.guilds:
            for member in guild.members:
                member_class_list.append(Players(member))

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        if message.author != client.user:
            if message.content.startswith("$Talk") or message.content.startswith("$talk"):
                m = message.content

                new_message = m.replace(m[:6], "")
                response = "You probably messed up"

                for i in member_class_list:
                    if i.member == message.author:
                        if m == "$Talk Chat Log" or m == "$Talk Chat log":
                            for a in i.int_chat_log:
                                message.channel.send(a)
                            return
                        print(i.member)
                        print(i.int_chat_log)
                        response = ask(new_message, i)

                await message.channel.send(response)

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            member_class_list.append(Players(member))


# openai
openai.organization = "openai org"
openai.api_key = "open ai api key"

# discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)

client.run('Discord Api key')
