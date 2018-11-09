# quest command

import discord
import config


# ---------------------
#    QuestPlaceData
# ---------------------
class QuestPlaceData:
	_id   = "";
	_name = "";
	_eta  = "";

	def __init__(self, p_id, p_name, p_eta):
		print("QuestPlaceData: ctor (" + p_id + ", " + p_name + ", " + p_eta + ");");
		self._id   = p_id;
		self._name = p_name;
		self._eta  = p_eta;


# ---------------------
#      QuestData
# ---------------------
class QuestData:
	_name      = "";
	_placeData = object;

	def __init__(self, p_name, p_placeData):
		self._name      = p_name;
		self._placeData = p_placeData;


# ---------------------
#   Temporary Globals
# ---------------------

globalPlaces = [];
globalQuests = [];

globalPlaces.append(QuestPlaceData("jfc", "Johanas Fish & Chips", "40min+"));
globalPlaces.append(QuestPlaceData("mcdo", "McDonald's", "20min"));



# ---------------------
#   QestCommandAction
# ---------------------

class QestCommandAction:
	_user = object;


	# Execute command ---
	async def execute(self, p_discordClient, p_channel, p_argMap):
		if len(p_argMap[config.SUBCOMMAND_KEY]) == 0:
			print ("QestCommandAction: no actions defined");
			return;

		action = p_argMap[config.SUBCOMMAND_KEY][0];
		if (action == "post"):
			pid = p_argMap.get("-pid");
			if (pid is None):
				await p_discordClient.send_message(p_channel, "No place id specified. Use -pid.");
				return;

			placeData = None;
			for place in globalPlaces:
				print ("Comparing " + pid + "  with " + place._id);
				if (place._id == pid):
					placeData = place;
					break;

			if (placeData is None):
				await p_discordClient.send_message(p_channel, "Specified place id not found.");
				return;

			questName = p_argMap.get("-n");
			if (questName is None):
				await p_discordClient.send_message(p_channel, "No quest name specified. Use -n");
				return;

			newQuest = QuestData(questName, placeData);
			globalQuests.append(newQuest);

			await self.postQuestToChat(p_discordClient, p_channel, newQuest);
			return;

		if action == "list":
			msg = "No quests available :(";
			print(msg);
			await p_discordClient.send_message(p_channel, msg);

		return;


	# Post quest to chat ---
	async def postQuestToChat(self, p_discordClient, p_channel, p_quest):
		placeData = p_quest._placeData;
		msg = "_New Quest Available: **" + p_quest._name + "**\n";
		msg += "at: **" + placeData._name + "** (" + placeData._id + ")\n";
		msg += "ETA: **" + placeData._eta + "**\n";
		msg += "**[ > quest accept " + placeData._id + " ]** to participate._";
		await p_discordClient.send_message(p_channel, msg);


	# Print usage ---
	async def printUsage(self, p_action):
		#msg = "Something went wrong";
		#await p_discordClient.send_message(p_channel, msg);
		pass;


	# Ctor ---
	def __init__(self, p_discordClient, p_channel, p_argMap):
		pass;


