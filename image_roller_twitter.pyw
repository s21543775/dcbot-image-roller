import discord
from discord import app_commands
import os
import random
from dotenv import load_dotenv
load_dotenv()

class aclient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.reactions = True
        super().__init__(intents = intents)
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'we have logged in as {self.user}.')
client = aclient()
tree = app_commands.CommandTree(client)

parent_path = os.getenv("IMAGE_PATH")
thumbnail_path = "./thumbnail.png"

exclude = []

async def finddir(text,path):
    character = text.lower()
    image_dirs = os.listdir(path)
    if character == 'random':
        choosen_dir = await choose_dir(image_dirs,exclude)
        path += f"/{image_dirs[choosen_dir]}"
        return (image_dirs[choosen_dir], path,True)
    elif character != '':
        for image_dir in image_dirs:
            if character in image_dir.lower():
                path += f"/{image_dir}"
                return (image_dir, path,True)
    return ('',path,False)

async def choose_dir(image_dirs,exclude):
    tmp = random.randint(0,len(image_dirs)-1)
    if image_dirs[tmp] in exclude:
        return await choose_dir(image_dirs,exclude)
    return tmp

async def choose_img(path):
    images = [image for image in os.listdir(path) if image[-4:] == '.jpg' or image[-4:] == '.png']
    choosen_image = random.randint(0,len(images)-1)
    path += f"/{images[choosen_image]}"
    tweet_id = await get_tweet_id(images[choosen_image])
    return tweet_id, path

async def make_img_embed(character,img_path, tweet_id):
    embed=discord.Embed(title=f"{character}", color=0xFF00FF)
    embed.set_author(name = '抽圖小幫手')
    embed.add_field(name = f'圖片連結', value = f'https://twitter.com/user/status/{tweet_id}')
    files = [discord.File(thumbnail_path, filename="image.png"),discord.File(img_path, filename="image2.png")]
    embed.set_thumbnail(url='attachment://image.png')
    embed.set_image(url='attachment://image2.png')
    return files, embed

async def get_tweet_id(img):
    if img.find('_') != -1:
        #xxx_0.jpg
        tweet_id = img[:img.find('_')]
        return tweet_id
    else:
        #.jpg
        tweet_id = img[:-4]
        return tweet_id


@tree.command(name="roll", description="roll images!")
async def roll_waifu(interaction: discord.Interaction, text: str = 'random'):
    character, path, havefind = await finddir(text,parent_path)
    if not havefind:
        await interaction.response.send_message(f'{text}不存在蒐藏名單中', ephemeral = True)
    else:
        tweet_id, path = await choose_img(path)
        files, embed = await make_img_embed(character, path, tweet_id)
        await interaction.response.send_message(files = files, embed=embed)

@roll_waifu.autocomplete('text')
async def waifu_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    image_dirs = os.listdir(parent_path)
    return [
        app_commands.Choice(name=image_dir, value=image_dir)
        for image_dir in image_dirs if current.lower() in image_dir.lower() and len(current) >= 2
    ]

@tree.command(name="secret_roll", description="roll images secretly!")
async def secret_roll_waifu(interaction: discord.Interaction, text: str = 'random'):
    character, path, havefind = await finddir(text,parent_path)
    if not havefind:
        await interaction.response.send_message(f'{text}不存在蒐藏名單中', ephemeral = True)
    else:
        tweet_id, path = await choose_img(path)
        files, embed = await make_img_embed(character, path, tweet_id)
        await interaction.response.send_message(files = files, embed=embed, ephemeral = True)

@secret_roll_waifu.autocomplete('text')
async def swaifu_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    image_dirs = os.listdir(parent_path)
    return [
        app_commands.Choice(name=image_dir, value=image_dir)
        for image_dir in image_dirs if current.lower() in image_dir.lower() and len(current) >= 2
    ]


@tree.command(name="info", description = "show you the infomation of this character's collection!")
async def test_dir_info(interaction: discord.Interaction, text: str = 'random'):
    character, path, havefind = await finddir(text,parent_path)
    if text == 'random':
        await interaction.response.send_message(content = '請輸入欲查詢的人物名稱', ephemeral = True)
    elif havefind == False:
        await interaction.response.send_message(content = '請輸入正確的人物名稱', ephemeral = True)
    else:
        images = [image for image in os.listdir(path) if image[-4:] == '.jpg' or image[-4:] == '.png']
        images.sort()
        last_image_path = f'{path}/{images[-1]}'
        tweet_id = await get_tweet_id(images[-1])
        files = [discord.File(thumbnail_path, filename="image.png"),discord.File(last_image_path, filename="image2.png")]
        embed=discord.Embed(title=f"{character}", color=0xFF5733)
        embed.set_author(name = '抽圖小幫手')
        embed.set_thumbnail(url='attachment://image.png')
        embed.add_field(name = f'圖片數量', value = f'{len(images) - 1}張', inline = False)
        embed.add_field(name = f'最新圖片', value = f'https://twitter.com/user/status/{tweet_id}')
        embed.set_image(url='attachment://image2.png')
        await interaction.response.send_message(files = files, embed=embed)

@test_dir_info.autocomplete('text')
async def dir_info_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    image_dirs = os.listdir(parent_path)
    return [
        app_commands.Choice(name=image_dir, value=image_dir)
        for image_dir in image_dirs if current.lower() in image_dir.lower() and len(current) >= 2
    ]

@tree.command(name="all_characters", description = "show you all characters' name!")
async def embedpages(interaction: discord.Interaction):

    await interaction.response.send_message('\u200b')
    page1 = discord.Embed (
        title = '圖片清單',
        description = '請自由透過/roll + 名稱抽取你的老婆瑟圖',
        colour = discord.Colour.orange()
    )
    page2 = discord.Embed (
        title = '圖片清單',
        description = '請自由透過/roll + 名稱抽取指定人物圖片',
        colour = discord.Colour.orange()
    )
    page3 = discord.Embed (
        title = '圖片清單',
        description = '請自由透過/roll + 名稱抽取指定人物圖片',
        colour = discord.Colour.orange()
    )
    page4 = discord.Embed (
        title = '圖片清單',
        description = '請自由透過/roll + 名稱抽取指定人物圖片',
        colour = discord.Colour.orange()
    )
    page5 = discord.Embed (
        title = '圖片清單',
        description = '請自由透過/roll + 名稱抽取指定人物圖片',
        colour = discord.Colour.orange()
    )

    dirs = os.listdir(parent_path)
    pages = [page1, page2, page3, page4, page5]
    if len(dirs) < 100:
        pages = pages[:int(len(dirs) / 20) + 1]
    num_pages = len(pages)
    values = [[] for _ in range(num_pages)]


    for idx, dir in enumerate(dirs):
        values[int(idx / 20)].append(dir)

    for page_idx, page in enumerate(pages):
        page.set_author(name = '抽圖小幫手')
        page.set_thumbnail(url='attachment://image.png')
        page.add_field(name = f'人物名稱', value = '\n'.join(values[page_idx]))
        page.set_footer(text = f'page{page_idx + 1}/{num_pages}')

    channel = interaction.channel
    files = [discord.File(thumbnail_path, filename="image.png")]
    message = await channel.send(files = files, embed = page1)
    
    await message.add_reaction('⏮')
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    await message.add_reaction('⏭')


    i = 0
    reaction = None

    while True:
        if str(reaction) == '⏮':
            i = 0
            await message.edit(embed = pages[i])
        elif str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '▶':
            if i < num_pages - 1:
                i += 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '⏭':
            i = num_pages - 1
            await message.edit(embed = pages[i])
        
        try:
            reaction, user = await client.wait_for('reaction_add',timeout = 300)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()

@tree.command(name="help", description = "show you all commands!")
async def help(interaction: discord.Interaction):
    embed=discord.Embed(title=f"指令清單", color=0x66FF99)
    files = [discord.File(thumbnail_path, filename="image.png")]
    embed.set_author(name = '抽圖小幫手')
    embed.set_thumbnail(url='attachment://image.png')
    embed.add_field(name = f'/roll ("character")', value = '隨機從所有資料夾中抽取一張圖片，也可以在roll後面輸入名字指定角色(可選)', inline = False)
    embed.add_field(name = f'/secret_roll ("character")', value = '同/roll，但抽取到的圖片僅本人可見', inline = False)
    embed.add_field(name = f'/info "character"', value = '展示指定角色的資料夾資訊，包含圖片數量及最新圖片', inline = False)
    embed.add_field(name = f'/all_characters', value = '展示角色名稱清單，可透過表情符號翻頁查找', inline = False)
    await interaction.response.send_message(files = files, embed=embed)

client.run(os.getenv("TOKEN"))