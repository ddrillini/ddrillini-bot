var Discord = require('discord.io');
var logger = require('winston');
var moment = require('moment');
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
// Configure timing
moment.relativeTimeThreshold('ss', 1);
var time_lastmatch = null;
// Generate insults
function produce_message(bad_word, good_word) {
    var responses = [
        `Hello. You seemed to have used the term "${bad_word}" when you should\'ve really used the term "${good_word}". Please start using "${good_word}" in the future. Thank you.`,
        `Hi. We do not condone this kind of language in this server. Please, refrain from using the term "${bad_word}" and instead say "${good_word}". Thank you.`
    ];
    var rnum = Math.floor(Math.random() * responses.length);
    return responses[rnum % responses.length];
}
const patterns = [
    [/(\bmap\b|\bmaps\b|\bmapping\b)/i, 'map', 'chart'],
    [/(\bbeatmap\b|\bbeatmaps\b)/i, 'beatmap', 'stepchart'],
]
bot.on('ready', function (evt) {
    logger.info('Connected');
    logger.info('Logged in as: ');
    logger.info(bot.username + ' - (' + bot.id + ')');
});
bot.on('message', function (user, userID, channelID, message, evt) {
    if (userID !== bot.id) {
        var output_messages = [];
        output_messages.length = 0;
        for (var i = 0; i < patterns.length; i++) {
            var pattern = patterns[i][0];
            var bad_word = patterns[i][1];
            var good_word = patterns[i][2];
            if (message.match(pattern)) {
                output_messages.push(produce_message(bad_word, good_word));
            }
        }
        if (output_messages.length > 0) {
            if (time_lastmatch !== null) {
                var time_diff = time_lastmatch.fromNow();
                output_messages.push(`\nThe last incident happened ${time_diff}.`)
            }
            time_lastmatch = moment();
            bot.sendMessage({
                to: channelID,
                message: output_messages.join('\n')
            });
        }
    }
});
