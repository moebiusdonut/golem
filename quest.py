# quest command

import discord
import config
import state


# ---------------------
#    QuestPlaceData
# ---------------------
class QuestPlaceData:
	_id   = "";
	_name = "";
	_desc = "";
	_eta  = "";

	# Ctor ---
	def __init__(self, p_id, p_name, p_eta, p_description=""):
		print("QuestPlaceData: ctor (" + p_id + ", " + p_name + ", " + p_eta + ");");
		self._id   = p_id;
		self._name = p_name;
		self._desc = p_description;
		self._eta  = p_eta;

	# Init from json ---
	def fromJSON(self, p_data):
		self._id   = p_data['id'];
		self._name = p_data['name'];
		self._desc = p_data['desc'];
		self._eta  = p_data['eta'];

	# Serialize to json ---
	def toJSON(self):
		data         = {};
		data['id']   = self._id;
		data['name'] = self._name;
		data['desc'] = self._desc;
		data['eta']  = self._eta;
		return data;


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
#   QestCommandAction
# ---------------------

class QestCommandAction:
	_discordClient = None;
	_discordChannel = None;
	_gameState = None;


	# Ctor ---
	def __init__(self, p_discordClient, p_discordChannel, p_gameState):
		self._discordClient  = p_discordClient;
		self._discordChannel = p_discordChannel;
		self._gameState 	 = p_gameState;


	# Execute command ---
	async def execute(self, p_argMap):
		if len(p_argMap[config.SUBCOMMAND_KEY]) == 0:
			print ("QuestCommandAction: no actions defined");
			return False;

		action = p_argMap[config.SUBCOMMAND_KEY][0];
		if (action == "post"):
			pid = p_argMap.get("-pid");
			if (pid is None):
				await self._discordClient.send_message(self._discordChannel, "No place id specified. Use -pid.");
				return False;

			placeData = None;
			for place in self._gameState._questPlaces:
				if (place._id == pid):
					placeData = place;
					break;

			if (placeData is None):
				await self._discordClient.send_message(self._discordChannel, "Specified place id not found.");
				return False;

			questName = p_argMap.get("-n");
			if (questName is None):
				await self._discordClient.send_message(self._discordChannel, "No quest name specified. Use -n");
				return False;

			newQuest = QuestData(questName, placeData);
			#globalQuests.append(newQuest);

			await self.postQuestToChat(newQuest);
			return True;

		if action == "place":
			if len(p_argMap[config.SUBCOMMAND_KEY]) < 2:
				msg = "_Place? This is a place, yes. Me sure quest can be somewhere in this place too_";
				await self._discordClient.send_message(self._discordChannel, msg);
				return False;

			term = p_argMap[config.SUBCOMMAND_KEY][1];
			if term == "list":
				msg = "_Me remember those:\n\n";

				for place in self._gameState._questPlaces:
					msg += "**" + place._name + "** (pid: **" + place._id + "**)\n";

				msg += "_";
				await self._discordClient.send_message(self._discordChannel, msg);
				return True;

		return False;


	# Post quest to chat ---
	async def postQuestToChat(self, p_quest):
		placeData = p_quest._placeData;
		msg = "_New Quest Available: **" + p_quest._name + "**\n";
		msg += "at: **" + placeData._name + "** (" + placeData._id + ")\n";

		if placeData._desc != "":
			msg += placeData._desc + "\n";

		msg += "ETA: **" + placeData._eta + "**\n";
		msg += "**[ > quest accept " + placeData._id + " ]** to participate._";
		await self._discordClient.send_message(self._discordChannel, msg);


	# Print usage ---
	async def printUsage(self, p_action):
		#msg = "Something went wrong";
		#await p_discordClient.send_message(self._discordChannel, msg);
		pass;



