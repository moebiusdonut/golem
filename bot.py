# Miyagi bot

import discord
import config
import quest
import state
import user
import shlex
import threading
import datetime
import asyncio

client = discord.Client();
gameState = state.GameState();
lastTimedActionTime = datetime.datetime.now();
asyncTimer = None;


class AsyncTimer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()


# Time control ---
async def timedAction():
    global asyncTimer;
    global lastTimedActionTime;

    asyncTimer = AsyncTimer(60 * 5, timedAction);
    now = datetime.datetime.now()

    prev = lastTimedActionTime;
    print("Heartbeat - [" + str(prev.hour) + ":" + str(prev.minute) + "] -> [" + str(now.hour) + ":" + str(now.minute) + "]");

    if now.hour == 13 and now.minute >= 10 and lastTimedActionTime.minute < 10:
        await gameState.finishAllActiveQuests(client, client.get_channel('500630431167807489')); # ugly hack

    lastTimedActionTime = now;




# Parse arguments ---
def parseArguments(p_arguments):
    argumentsMap = { config.SUBCOMMAND_KEY : [] };

    if len(p_arguments) == 0:
        argumentsMap;

    splitted = shlex.split(p_arguments);
    prevArg = "";
    for arg in splitted:
        if arg.startswith(config.PARAM_SYMBOL):
            prevArg = arg;
            continue;

        if prevArg != "":
            argumentsMap[prevArg] = arg;
            prevArg = "";
            continue;

        argumentsMap[config.SUBCOMMAND_KEY].append(arg);

    return argumentsMap;


# Add user if does not exist ---
def addUserIfNotExist(p_user):
    usr = gameState.getUserByID(p_user.id);
    if usr is None:
        gameState.addUser(p_user.id, p_user.name);


#On Message ---
@client.event
async def on_message(message):
    # ignore self
    if message.author == client.user:
        return;

    if not message.content.startswith(config.COMMAND_SYMBOL) or len(message.content) == 1:
        return;

    addUserIfNotExist(message.author); # Because user can join server after bot starts


    splitted = message.content.split(' ', 1);
    command = splitted[0];

    if command == config.COMMAND_SYMBOL: 
        # '>(space)command' scenario
        splitted = splitted[1].split(' ', 1);
        command = splitted[0];
    else:
        # '>command' scenario
        command = command[1:];

    arguments = "";
    if len(splitted) > 1:
        arguments = splitted[1];

    
    usrID  = message.author.id;
    argMap = parseArguments(arguments);
    result = False;

    # Commands factory
    if command == 'quest':
        cmdAction = quest.QestCommandAction(client, message.channel, gameState, usrID);
        result = await cmdAction.execute(argMap);

    elif command == 'say':
        if len(argMap[config.SUBCOMMAND_KEY]) > 0:
            await client.delete_message(message);

            msg = "_" + argMap[config.SUBCOMMAND_KEY][0] + "_";
            await client.send_message(message.channel, msg);
            result = True;
    


    if result == False:
        msg = "Command '" + command + "' failed! *Golem stomps ground with rage*";
        await client.send_message(message.channel, msg);
    else:
        gameState.save();

    

@client.event
async def on_ready():
    print('Ready')
    print(client.user.name)
    print(client.user.id)
    print('------')

    gameState.load();

    for member in client.get_all_members():
        print(member.id + " = " + member.name);
        if member != client.user:
            addUserIfNotExist(member);

    await timedAction();
    

client.run(config.TOKEN)




# eof