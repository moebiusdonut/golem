# Miyagi bot

import discord
import config
import quest
import state
import user
import shlex

client = discord.Client();
gameState = state.GameState();


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
    

client.run(config.TOKEN)




# eof