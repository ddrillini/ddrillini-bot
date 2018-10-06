var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';
// Initialize Discord Bot
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});
bot.on('ready', function (evt) {
    logger.info('Connected');
    logger.info('Logged in as: ');
    logger.info(bot.username + ' - (' + bot.id + ')');
});
bot.on('message', function (user, userID, channelID, message, evt) {
    var map = message.match(/(\bmap\b|\bmapping\b)/i);
    var beatmap = message.match(/\bbeatmap\b/i);
    if (map != null && userID != bot.id) {
        bot.sendMessage({
            to: channelID,
            message: 'Hello. You seemed to have used the term "map" when you should\'ve really used the term "chart". Please start using "chart" in the future. Thank you.'
        });
    }
    if (beatmap != null && userID != bot.id) {
        bot.sendMessage({
            to: channelID,
            message: 'Hi. We do not condone this kind of language in this server. Please, refrain from using the term "beatmap" and instead say "stepchart". Thank you.'
        });
    }
});
