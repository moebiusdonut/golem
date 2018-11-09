# Miyagi bot

import discord
import config
import quest

client = discord.Client()


# Parse arguments ---
def parseArguments(p_arguments):
    argumentsMap = { config.SUBCOMMAND_KEY : [] };

    if len(p_arguments) == 0:
        argumentsMap;

    splitted = p_arguments.split(' ');

    prevArg = "";
    for arg in splitted:
        if arg.startswith(config.PARAM_SYMBOL):
            prevArg = arg;
            continue;

        if prevArg != "":
            argumentsMap[prevArg] = arg;
            continue;

        argumentsMap[config.SUBCOMMAND_KEY].append(arg);

    return argumentsMap;


#On Message ---
@client.event
async def on_message(message):
    # ignore self
    if message.author == client.user:
        return;

    if not message.content.startswith(config.COMMAND_SYMBOL) or len(message.content) == 1:
        return;

    splitted = message.content.split(' ', 1);
    command = splitted[0];

    if command == config.COMMAND_SYMBOL: 
        # '>(space)command' scenario
        splitted = splitted.split(' ', 1);
        command = splitted[0];
    else:
        # '>command' scenario
        command = command[1:];

    arguments = "";
    if len(splitted) > 1:
        arguments = splitted[1];

    
    argMap = parseArguments(arguments);
    
    #msg = "command = " + command + str(argMap);
    #print(message.channel);
    #await client.send_message(message.channel, msg);

    # Commands factory
    if command == 'quest':
        cmdAction = quest.QestCommandAction(client, message.channel, argMap);
        await cmdAction.execute(client, message.channel, argMap);
    

    





@client.event
async def on_ready():
    print('Ready')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(config.TOKEN)