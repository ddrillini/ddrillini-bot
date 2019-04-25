We're currently in the midst of the semester, but we'll publish this bot eventually.

Currently, it has two features:
[placeholder1 - map]
[placeholder2 - pattern ref]

# Node.js
```
# install nodejs
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs

# install dependencies
npm install discord.io winston moment

# run bot (probably want to do this inside a tmux window on a server.)
# you could use a proper process manager but /shrug
node bot.js
```
# Python 3.7
```
# install dependencies
python3 -m pip install -U discord.py arrow Pillow

# run bot
python3 bot.py --login_token <YOUR_TOKEN>
```

