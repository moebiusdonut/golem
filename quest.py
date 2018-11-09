# quest command

import discord
import config


# ---------------------
#    QuestPlaceData
# ---------------------
class QuestPlaceData:
	_id   = "";
	_name = "";
	_desc = "";
	_eta  = "";

	# Ctor ---
	def __init__(self, p_id, p_name, p_eta, p_description):
		print("QuestPlaceData: ctor (" + p_id + ", " + p_name + ", " + p_eta + ");");
		self._id   = p_id;
		self._name = p_name;
		self._desc = p_description;
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

globalPlaces.append(QuestPlaceData("annka", "Annka", "20min", "Best salads in town!"));
globalPlaces.append(QuestPlaceData("jfc", "Johanas Fish & Chips", "50min+", ""));
globalPlaces.append(QuestPlaceData("mcdo", "McDonald's", "20min", ""));
globalPlaces.append(QuestPlaceData("b321", "Burger 321 (or whatever the numbers are)", "35min", "Great American burgers"));
globalPlaces.append(QuestPlaceData("bento", "52^2m Bento", "35min", ""));
globalPlaces.append(QuestPlaceData("bistro", "Bistropolitain", "30-40min", "French cousine"));
globalPlaces.append(QuestPlaceData("burrito", "Chippotle", "30-40min", "Tacos / Burritos"));



# ---------------------
#   QestCommandAction
# ---------------------

class QestCommandAction:
	_user = object;


	# Execute command ---
	async def execute(self, p_discordClient, p_channel, p_argMap):
		if len(p_argMap[config.SUBCOMMAND_KEY]) == 0:
			print ("QestCommandAction: no actions defined");
			return False;

		action = p_argMap[config.SUBCOMMAND_KEY][0];
		if (action == "post"):
			pid = p_argMap.get("-pid");
			if (pid is None):
				await p_discordClient.send_message(p_channel, "No place id specified. Use -pid.");
				return False;

			placeData = None;
			for place in globalPlaces:
				if (place._id == pid):
					placeData = place;
					break;

			if (placeData is None):
				await p_discordClient.send_message(p_channel, "Specified place id not found.");
				return False;

			questName = p_argMap.get("-n");
			if (questName is None):
				await p_discordClient.send_message(p_channel, "No quest name specified. Use -n");
				return False;

			newQuest = QuestData(questName, placeData);
			globalQuests.append(newQuest);

			await self.postQuestToChat(p_discordClient, p_channel, newQuest);
			return True;

		if action == "place":
			if len(p_argMap[config.SUBCOMMAND_KEY]) < 2:
				await p_discordClient.send_message(p_channel, "_Place? This is a place, yes. Me sure quest can be somewhere in this place too_");
				return False;

			term = p_argMap[config.SUBCOMMAND_KEY][1];
			if term == "list":
				msg = "_Me remember those:\n\n";

				for place in globalPlaces:
					msg += "**" + place._name + "** (pid: **" + place._id + "**)\n";

				msg += "_";
				await p_discordClient.send_message(p_channel, msg);
				return True;

		return False;


	# Post quest to chat ---
	async def postQuestToChat(self, p_discordClient, p_channel, p_quest):
		placeData = p_quest._placeData;
		msg = "_New Quest Available: **" + p_quest._name + "**\n";
		msg += "at: **" + placeData._name + "** (" + placeData._id + ")\n";

		if placeData._desc != "":
			msg += placeData._desc + "\n";

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


