# Dcbot Image Roller
## Abstract
* It can randomly roll a image from all directories or one specific directory.
* It can be used with my another project [Dcbot-Image-Downloader](https://github.com/s21543775/dcbot-image-downloader)
* If images are named as tweet ids (like Dcbot-Image-Downloader), it can attach the original tweet's link on the embed's infomation when rolling an image.

![](https://i.imgur.com/8Ab4fzc.png)
## How to use
### Install these python packages
```
discord
dotenv
```
### Setup .env
```
IMAGE_PATH = where you save images
TOKEN = your discord bot token
```
* Discord bot token can get from next step
### Create a new application and add a bot in Discord Developer Portal
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **new application**
3. Setup application infomation, then add a bot in this application
4. Get token from Settings - bot - Build-A-Bot - Token
5. Set Privileged Gateway Intents like this:
![](https://i.imgur.com/GHwrbId.png)
6. Go to Settings - OAuth2
7. Get invite link of your bot:
![](https://i.imgur.com/01RDAq9.png)
![](https://i.imgur.com/7QReonS.png)
### Run the dcbot program
* If you use [Dcbot-Image-Downloader](https://github.com/s21543775/dcbot-image-downloader) to download images or save images by their tweet ids, use **image_roller_twitter.pyw**
> It will attach original tweet's link on the embed.

* If you didn't save images by their tweet ids, use **image_roller.pyw**
### Done!
## Command Intro
### /roll + (directory name)
* Roll an image in the specific directory.
* If you don't specify the directory, it will roll an image from all directories under IMAGE_PATH.
![](https://i.imgur.com/MLXqPnT.png)

### /secret_roll + (directory name)
* Like /roll, but only the user send this command can see the image from the bot.
![](https://i.imgur.com/697Hc7n.png)

### /info + directory name
* Show user the info of specific directory.
* Info include number of image under this directory and the newest image (sort by tweet id).
![](https://i.imgur.com/aLXCHNz.png)

### /all_characters
* Show all directories' name under IMAGE_PATH.
* If number of directories' more than 20, user can use reactions to turn the pages of embed.
![](https://i.imgur.com/ShRQfnQ.png)
