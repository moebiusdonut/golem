# quest command

import discord
import config
import state
import random


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
	_discordClient  = None;
	_discordChannel = None;
	_gameState      = None;


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
		if action == "post":
			return await self._process_quest_post_cmd(p_argMap);

		if action == "place":
			return await self._process_quest_place_cmd(p_argMap);

		if action == "help":
			return await self._process_quest_help_cmd(p_argMap);

		return False;


	# Process "quest post ..." command ---
	async def _process_quest_post_cmd(self, p_argMap):
		if len(p_argMap[config.SUBCOMMAND_KEY]) > 1:
			term = p_argMap[config.SUBCOMMAND_KEY][1];
			if term == "random":
				name      = self._getRandomQuestName();
				places    = self._gameState._questPlaces;
				placeData = places[random.randint(0, len(places)-1)];
				newQuest  = QuestData(name, placeData);

				await self.postQuestToChat(newQuest);
				return True;


		pid = p_argMap.get("-pid");
		if pid is None:
			await self._discordClient.send_message(self._discordChannel, "No place id specified. Use -pid.");
			return False;

		placeData = None;
		for place in self._gameState._questPlaces:
			if place._id == pid:
				placeData = place;
				break;

		if placeData is None:
			await self._discordClient.send_message(self._discordChannel, "Specified place id not found.");
			return False;

		questName = p_argMap.get("-n");
		if questName is None:
			await self._discordClient.send_message(self._discordChannel, "No quest name specified. Use -n");
			return False;

		newQuest = QuestData(questName, placeData);
		#globalQuests.append(newQuest);

		await self.postQuestToChat(newQuest);
		return True;


	# Process "quest place ..." command ---
	async def _process_quest_place_cmd(self, p_argMap):
		if len(p_argMap[config.SUBCOMMAND_KEY]) < 2:
			msg = "_Place? This is a place, yes. Me sure quest can be somewhere in this place too_";
			await self._discordClient.send_message(self._discordChannel, msg);
			return False;

		term = p_argMap[config.SUBCOMMAND_KEY][1];
		if term == "list":
			# >quest place list
			msg = "_Me remember those:\n\n";

			for place in self._gameState._questPlaces:
				msg += "**" + place._name + "** (pid: **" + place._id + "**)\n";

			msg += "_";
			await self._discordClient.send_message(self._discordChannel, msg);
			return True;

		if term == "add":
			# >quest place add -n "Johana The Fish" -pid jfc -eta "50min+" [-desc "Some kind of description"]
			placeName = p_argMap.get("-n");
			placeID   = p_argMap.get("-pid");
			placeETA  = p_argMap.get("-eta");
			placeDesc = p_argMap.get("-desc", "");

			if placeName is None or placeID is None or placeETA is None:
				msg = "_Me not understand you, human. What is this new place you talk to me about ?_";
				await self._discordClient.send_message(self._discordChannel, msg);
				return False;

			newPlace = QuestPlaceData(placeID, placeName, placeETA, placeDesc);
			self._gameState.addQuestPlace(newPlace);

			msg = "_Ok, human. I will remember that. Golems known for good memory... i guess._";
			await self._discordClient.send_message(self._discordChannel, msg);
			return True;


	# Process "quest place ..." command ---
	async def _process_quest_help_cmd(self, p_argMap):
		msg = "_Oh, me got this paper here but me not know what this means_ \n```";
		msg += "Quests are based on places: \n\n";
		msg += ">quest place list \n";
		msg += '>quest place add -n "Place Name" -pid place_id -eta "Estimated time" [-desc "Optional description"]\n\n';
		msg += "Once desired place is known you can post a quest for it:\n\n"
		msg += '>quest post -n "New Quest Name" -pid existing_pid```';
		await self._discordClient.send_message(self._discordChannel, msg);
		return True;


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


	# Returns random quest name ---
	def _getRandomQuestName(self):
		pool = [\
		"Wzooooom!",\
		"No shame in what we do",\
		"Food. Mouth. You dig?",\
		"Gimme two!",\
		"Vodka not included",\
		"Hello, Fat",\
		"Munch Munch",\
		"Essentials"\
		];
		return pool[random.randint(0, len(pool)-1)];




# eof
