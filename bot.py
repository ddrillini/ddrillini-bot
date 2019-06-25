# note: requrise python 3.6
import discord
import random
import re
import argparse
import arrow
from PIL import Image
import io, os
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()
time_lastmatch = None;

def bold(word):
    return f"**{word}**"

def produce_message(bad_word, good_word):
    bold_bad_word = bold(bad_word)
    bold_good_word = bold(good_word)
    responses = [
        f"Hello. You seemed to have used the term {bold_bad_word} when you should\'ve really used the term {bold_good_word}. Please start using {bold_good_word} in the future. Thank you.",
        f"Hi. We do not condone this kind of language in this server. Please, refrain from using the term {bold_bad_word} and instead say {bold_good_word}. Thank you.",
        f"I\'d just like to interject for a moment. What you\'re referring to as {bold_bad_word}, is in fact, {bold_good_word}.",
        f"Please avoid the term {bold_bad_word}. People around here seem to favor the term {bold_good_word}. I don\'t want anybody to get upset.",
        f"A kitten dies every time someone writes {bold_bad_word}. Make the world a better place, write {bold_good_word} instead.",
        f"What\'s that? Did I just hear someone say {bold_bad_word}? I better not have heard someone say {bold_bad_word}. That better be {bold_good_word} before I get around the corner or so help me...",
        f"Type {bold_bad_word} again and I will physically manifest in your house and make you type {bold_good_word} until you forget the word {bold_bad_word} exists.",
        f"You\'re gonna want to replace that {bold_bad_word} with {bold_good_word}, trust me. I\'m fairly merciful about this but Ian takes no prisoners.",
        f"I see you are of the cult of {bold_bad_word}. Here at DDRIllini, we exclusively follow the cult of {bold_good_word}, and we ask that you please do the same.",
        f"Ya ever just accidentally type {bold_bad_word} instead of {bold_good_word}? You must have\; it\'s not like you could have intentionally typed {bold_bad_word}, cuz if so we\'d have to [REDACTED], and trust me nobody wants that.",
        f"It seems your rampant keysmashing accidentally generated the word {bold_bad_word}. In the future, please quality check your nonsense and replace any instances of {bold_bad_word} with {bold_good_word}.",
        f"The term {bold_good_word} is unquestionably superior to the term {bold_bad_word}. Seriously. Please use the appropriate word."
    ]
    return random.choice(responses)

@client.event
async def on_ready():
    print("Connected.")
    print("Logged in as:")
    print(f"{client.user} - ({client.user.id})")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!pattern "):
        # TODO see if you can escape things?
        pattern = re.findall(r"(?<=^!pattern )[LRUD() ]*", message.content, re.I)[0]
        cropflag = 0
        crop = 0
        patternlength = 0
        characterlength = 0
        for c in pattern:
            if(patternlength <= 25):
                if(c == "("):
                    cropflag = 1 #mark jumps
                elif(c == ")"):
                    cropflag = 0 #end of jump
                if(cropflag == 1):
                    crop += 1
                else:
                    patternlength += 1
                characterlength += 1
        pattern = pattern[:characterlength] #limit of 25 lines
        img = Image.new('RGB', (32*4, (len(pattern)-crop)*32), color="black")

        red_arrow = Image.open("R.png")
        blue_arrow = Image.open("B.png")
        arrows = [red_arrow, blue_arrow]

        mine_file_name = "Mine.png"
               
        jump = 0
        blank = 0

        count = 0
        for c in pattern:
            file_name = arrows[count % 2] # grab red or blue arrow
            if(c == "l"): #LDUR
                paste_me = file_name.rotate(270)
                x = 0
            elif(c == "r"):
                paste_me = file_name.rotate(90)
                x = 32*3
            elif(c == "u"):
                paste_me = file_name.rotate(180)
                x = 32*2
            elif(c == "d"):
                paste_me = file_name
                x = 32
            elif(c == "L"): #mines
                paste_me = Image.open(mine_file_name).rotate(270)
                x = 0
            elif(c == "R"):
                paste_me = Image.open(mine_file_name).rotate(90)
                x = 32*3
            elif(c == "U"):
                paste_me = Image.open(mine_file_name).rotate(180)
                x = 32*2
            elif(c == "D"):
                paste_me = Image.open(mine_file_name)
                x = 32
            elif(c == "("):
                jump = 1
                blank = 1
            elif(c == ")"):
                jump = 0
                blank = 1
            elif(c == " "):
                blank = 1
            if(blank == 0):
                img.paste(paste_me, (x,count*32))
            blank = 0
            if(jump == 0): #skip count increment if jumping
                count += 1
        byte_array = io.BytesIO()
        img.save("pattern.png", format='PNG')
        await message.channel.send(file=discord.File("pattern.png"))



    elif (message.guild.name == "DDRIllini"):

        patterns = [
        [r"(\bmap\b|\bmaps\b|\bmapping\b)", 'map', 'chart'],
        [r"(\bbeatmap\b|\bbeatmaps\b)", 'beatmap', 'stepchart'],
        ]
        output_messages = []

        for pattern in patterns:
            if re.findall(pattern[0], message.content, re.I):
                output_messages.append(produce_message(pattern[1], pattern[2]))

        if len(output_messages) > 0:
            global time_lastmatch
            if time_lastmatch != None:
                output_messages.append(f"\nThe last incident happened {time_lastmatch.humanize()}.")
            time_lastmatch = arrow.utcnow()
            separator = '\n'
            await message.channel.send(separator.join(output_messages))
    


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--login_token', type=str, required=True)
    args = ap.parse_args()

    client.run(args.login_token)

if __name__ == "__main__":
    main()
