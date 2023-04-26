import discord
import random
import json

# Create a new bot
bot = discord.Bot()
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
        embed = discord.Embed(
            title="We're not really strangers.",
            description=f"Question: {question} \n Answer: {self.children[0].value}")
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
    with open('questions.json') as fp:
            questions = json.load(fp)

    global question 
    question = questions['questions'][random.randint(0, len(questions['questions']) - 1)]
    embed = discord.Embed(
        title="We're not really strangers.",
        description=question)
    await ctx.respond(embed = embed, view=MyView())
bot.run("Token")
