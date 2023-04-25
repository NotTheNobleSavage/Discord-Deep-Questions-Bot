import discord
import random

# Create a new bot
bot = discord.Bot()

#Some Basic questions
questions = [
    "What is something you've always wanted to tell me but haven't?",
    "What's the most important lesson you've learned this year?",
    "What's something you're afraid to do but really want to?",
    "When was the last time you felt truly seen by someone?",
    "What do you think is your biggest strength, and how has it helped you in your life?",
    "What's one thing you're currently struggling with that you'd like some support on?",
    "When was the last time you took a risk, and how did it turn out?",
    "What's something you've been meaning to do for a long time, but haven't yet?",
    "What's one thing you're grateful for right now, and why?",
    "What's something you've done in the past that you're proud of?"
]

anon_mode = False

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

#Create the Model Dialog
class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        #Add a long text input for the answer
        self.add_item(discord.ui.InputText(label="Answer", style=discord.InputTextStyle.long))

    #On submit send the answer
    async def callback(self, interaction: discord.Interaction):

        #Allows for anon mode so that the user's name is not shown
        embed = discord.Embed(title="Answer",description=self.children[0].value)
        if anon_mode == False:
            embed.set_footer(text=str(interaction.user), icon_url=interaction.user.avatar.url)
        else:
            embed.set_footer(text="Anonymous")
        #Send the answer
        await interaction.response.send_message(embeds=[embed])

#Creates the Answer button
class MyView(discord.ui.View):
    @discord.ui.button(label="Answer!", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        #Calls the Modal
        modal = MyModal(title="We're not really strangers.")
        await interaction.response.send_modal(modal)

#Slash Command
@bot.slash_command()
async def deep_question(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="We're not really strangers.",
        description=questions[random.randint(0, len(questions) - 1)])
    await ctx.respond(embed = embed, view=MyView())

bot.run("Token")
