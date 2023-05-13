import discord
from discord import app_commands
import openai
import os
import qrcode
import io
import random
import aiohttp


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id=1087765025105662042)) #ur server id
            self.synced = True
        print(f"We have logged in as {self.user}.")
        await self.change_presence(activity=discord.Game(name="Serving Father Mido"))


client = aclient()
tree = app_commands.CommandTree(client)
guild_id = 1087765025105662042 #ur server ID
openai.api_key = "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" #use ur own OPENAI API KEY

heart_img_link = "https://i.pinimg.com/736x/fd/e5/43/fde5431c6ba41dd0d8ec01f063e00ee3.jpg"
heart_broken_img_link = "https://th.bing.com/th/id/OIP.ajSTcbxe1C2sLL87qKsxMwHaHL?pid=ImgDet&rs=1"

# Ask GPT Command
@tree.command(guild=discord.Object(id=guild_id), name='system', description='Ask an AI a question')
async def ask_gpt(interaction: discord.Interaction, *, question: str):
    await interaction.response.defer()  # Defer the response
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{question}\nAnswer:",
            temperature=0.5,
            max_tokens=500,  # Change this value to 500
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
)

        

        answer = response.choices[0].text.strip()
        await interaction.followup.send(answer)  # Send the answer as a follow-up message

    except Exception as e:
        await interaction.followup.send(f"An error occurred while processing your request: {e}")  # Send the error as a follow-up message


async def generate_image(prompt: str):
    response = openai.Image.create(
        model="image-alpha-001",
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="url",
    )

    image_url = response['data'][0]['url']

    return image_url

# image generation command
@tree.command(guild=discord.Object(id=guild_id), name='generate_image', description='Generate an image based on the input description')
async def generate_image_command(interaction: discord.Interaction, description: str):
    try:
        # Acknowledge the interaction
        await interaction.response.defer()
        
        image_url = await generate_image(description)

        embed = discord.Embed(title="Generated Image", description=f"Based on: {description}", color=0x00ff00)
        embed.set_image(url=image_url)
        
        # Use interaction channel to send the message
        await interaction.channel.send(embed=embed)
    except Exception as e:
        # Use interaction channel to send the error message
        await interaction.channel.send(f"An error occurred while generating the image: {e}")


# Ship Command 
@tree.command(guild=discord.Object(id=guild_id), name='ship', description='Rate the ship between two people')
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    shipname = user1.display_name + user2.display_name
    rating = abs(hash(shipname)) % 101
    
    if rating >= 90:
        description = "Absolutely perfect match!"
        img_link = heart_img_link
    elif rating >= 80:
        description = "Extremely compatible!"
        img_link = heart_img_link
    elif rating >= 70:
        description = "Very compatible!"
        img_link = heart_img_link
    elif rating >= 60:
        description = "Compatible!"
        img_link = heart_img_link
    elif rating >= 50:
        description = "Somewhat compatible!"
        img_link = heart_img_link
    elif rating >= 40:
        description = "Not very compatible!"
        img_link = heart_broken_img_link
    elif rating >= 30:
        description = "Not compatible!"
        img_link = heart_broken_img_link
    elif rating >= 20:
        description = "Absolutely not compatible!"
        img_link = heart_broken_img_link
    else:
        description = "Worst match ever!"
        img_link = heart_broken_img_link
        
    embed = discord.Embed(title=f"Ship Rating: {rating}", description=description, color=0xff69b4)
    embed.set_author(name=f"{user1.display_name} x {user2.display_name}")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(img_link) as resp:
            if resp.status != 200:
                return await interaction.response.send_message("Could not fetch the image.")
            data = io.BytesIO(await resp.read())
            file = discord.File(data, filename="image.png")
            await interaction.response.send_message(embed=embed, file=file)


# Help command
@tree.command(guild=discord.Object(id=guild_id), name='help', description='Show available commands')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(color=0xffffff)
    embed.set_author(name="Help Commands", icon_url="https://i.pinimg.com/originals/37/95/0f/37950fbffd580d320de2947ec574227b.jpg")
    pastelink = "https://pastebin.com/raw/3TNYqTSv"
    embed.add_field(name="Commands:", value=pastelink, inline=False)
    await interaction.response.send_message(embed=embed)

# Info commmand 
@tree.command(guild = discord.Object(id=guild_id), name = 'info', description='information about the bot')
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"I was made by my father Mido#1337")

# QR code command 
@tree.command(guild=discord.Object(id=guild_id), name='qr', description='Generates a QR code from the input text')
async def qr(interaction: discord.Interaction, text: str):
    img = qrcode.make(text)

    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await interaction.response.send_message("QR code generated!", file=discord.File(fp=image_binary, filename="qrcode.png"))

# Ping command
@tree.command(guild=discord.Object(id=guild_id), name='ping', description='Check the bot\'s latency')
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f":hourglass: Bot HTTP Ping is {round(client.latency * 1000)}ms",
        color=discord.Colour.red())
    await interaction.response.send_message(embed=embed)

# Coin Flip Command
@tree.command(guild=discord.Object(id=guild_id), name='coinflip', description='Flip a coin')
async def coinflip(interaction: discord.Interaction):
    outcomes = ['heads', 'tails']
    result = random.choice(outcomes)

    if result == 'heads':
        emoji = '🌕'
    else:
        emoji = '🌑'
        
    await interaction.response.send_message(f"The coin landed on {result}! {emoji}")


# Custom Truth or Dare Command
@tree.command(guild=discord.Object(id=guild_id), name='custom_tod', description='Send a custom Truth or Dare challenge to another user')
async def custom_truth_or_dare(interaction: discord.Interaction, user: discord.Member, choice: str, *, custom_text: str):
    if choice.lower() == "truth":
        await interaction.response.send_message(f"{user.mention}, you have been asked a truth: {custom_text}")
    elif choice.lower() == "dare":
        await interaction.response.send_message(f"{user.mention}, you have been dared: {custom_text}")
    else:
        await interaction.response.send_message("Invalid choice. Please choose either 'truth' or 'dare'.")

# Anonymous Truth or Dare Command
@tree.command(guild=discord.Object(id=guild_id), name='anon_tod', description='Submit a Truth or Dare question anonymously to another user.')
async def anon_tod(interaction: discord.Interaction, user: discord.Member, choice: str, *, custom_text: str):
    if choice.lower() == "truth":
        message = f"{user.mention}, you have been asked a truth: {custom_text}"
    elif choice.lower() == "dare":
        message = f"{user.mention}, you have been dared: {custom_text}"
    else:
        message = "Invalid choice. Please choose either 'truth' or 'dare'."

    # Send the anonymous message to the channel
    channel = interaction.channel
    anon_name = f'Anonymous-'
    await channel.send(f"{user.mention}, {anon_name} has sent you a {choice}: {custom_text}")

    # Let the user know the message has been sent
    await interaction.response.send_message("Your message has been sent anonymously.", ephemeral=True)

# Makes a GET request to the specified URL and returns the questions as a list
async def fetch_questions(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            questions = content.splitlines()
    return questions
  
# Filters the list of questions to only include those that start with the specified category, then returns a random question from that list
async def get_random_question(questions, category):
    filtered_questions = [q for q in questions if q.startswith(f"{category}:")]
    return random.choice(filtered_questions) if filtered_questions else None

# Truth Command
@tree.command(guild=discord.Object(id=guild_id), name='tod-truth', description='Randomly selects a truth question.')
async def TOD_Truth(interaction: discord.Interaction):
    category = "Truth"

    url = "https://pastebin.com/raw/TNMJKa2R"
    questions = await fetch_questions(url)
    question = await get_random_question(questions, category)

    if question:
        await interaction.response.send_message(question)
    else:
        await interaction.response.send_message("No questions found for the given category.")

# Dare Command
@tree.command(guild=discord.Object(id=guild_id), name='tod-dare', description='Randomly selects a dare question.')
async def TOD_Dare(interaction: discord.Interaction):
    category = "Dare"

    url = "https://pastebin.com/raw/TNMJKa2R"
    questions = await fetch_questions(url)
    question = await get_random_question(questions, category)

    if question:
        await interaction.response.send_message(question)
    else:
        await interaction.response.send_message("No questions found for the given category.")

# Guild Command
@tree.command(guild=discord.Object(id=guild_id), name='guild', description='Show guild id')
async def guild_id(interaction: discord.Interaction):
    await interaction.response.send_message(f"The ID of this guild is {interaction.guild.id}.")



token = os.getenv("token") #token is the bots discord token
client.run(token) #client is the bots discord client
