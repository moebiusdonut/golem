# state.py

import json
import quest as Quest
import user as User

# ---------------------
#      GameState
# ---------------------
class GameState:
	_users        = [];
	_questPlaces  = [];
	_activeQuests = [];


	# Load game state from save file ---
	def load(self):
		with open('save.json') as file:
			data = json.load(file);

		users = data["users"];
		for userData in users:
			usr = User.UserData();
			usr.fromJSON(userData);
			self._users.append(usr);

		places = data['places'];
		for placeData in places:
			place = Quest.QuestPlaceData('', '', '');
			place.fromJSON(placeData);
			self._questPlaces.append(place);


	# Save game state from save file ---
	def save(self):
		data = {};

		usersDataArray = [];
		for usr in self._users:
			userData = usr.toJSON();
			usersDataArray.append(userData);

		data['users'] = usersDataArray;

		placesDataArray = [];
		for place in self._questPlaces:
			placeData = place.toJSON();
			placesDataArray.append(placeData);

		data['places'] = placesDataArray;

		with open('save.json', 'w') as outfile:
			json.dump(data, outfile);


	# Get user by id ---
	def getUserByID(self, p_id):
		for usr in self._users:
			if usr._id == p_id:
				return usr;

		return None;


	# Add user ---
	def addUser(self, p_id, p_name):
		if self.getUserByID(p_id) is not None:
			print("ERROR: trying to add existing user " + p_pid);
			return;

		newUser = User.UserData();
		newUser._id = p_id;
		newUser._name = p_name;
		self._users.append(newUser);


	# Add quest place ---
	def addQuestPlace(self, p_questPlaceData):
		self._questPlaces.append(p_questPlaceData);


	# Add quest ---
	def addQuest(self, p_quest):
		print("adding quest...")
		self._activeQuests.append(p_quest);


	# Get active quest by id ---
	def getQuestByID(self, p_placeID):
		for quest in self._activeQuests:
			if quest._placeData._id == p_placeID:
				return quest;

		return None;


	# Finish all active quests ---
	async def finishAllActiveQuests(self, p_discordClient, p_channel):
		print("finishing quests...");
		print("channel is: " + str(p_channel));
		for questData in self._activeQuests:
			msg = "---------\n";
			usersJoined = len(questData._users);
			print("Quest = " + questData._name + ", " + str(questData) + ", users = " + str(questData._users));
			
			if usersJoined == 0:
				msg += "_Quest **" + questData._name + "** failed. Princess in another castle._";
				await p_discordClient.send_message(p_channel, msg);
				continue;

			creditsPerUser = 12 * usersJoined;

			msg += "_Quest **" + questData._name + "** complete!\n";
			for usr in questData._users:
				msg += "**" + usr.getNameRepresentation() + "**, ";
				usr._credits += creditsPerUser;

			msg += "are getting **" + str(creditsPerUser) + "** credits each.\n";
			msg += "Me proud of you meatbags!";
			await p_discordClient.send_message(p_channel, msg);

		print(str(len(self._activeQuests)) + " finished");
		self._activeQuests = [];


# eof

