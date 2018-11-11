# state.py

import json
import quest
import user

# ---------------------
#      GameState
# ---------------------
class GameState:
	_users        = [];
	_questPlaces  = [];
	_activeQuests = [];

	
	# Ctor ---
	def __init__(self):
		pass;


	# Load game state from save file ---
	def load(self):
		with open('save.json') as file:
			data = json.load(file);

		users = data["users"];
		for userData in users:
			user = user.UserData();
			user.fromJSON(userData);
			self._users.append(user);

		places = data['places'];
		for placeData in places:
			place = quest.QuestPlaceData('', '', '');
			place.fromJSON(placeData);
			self._questPlaces.append(place);


	# Save game state from save file ---
	def save(self):
		data = {};

		usersDataArray = [];
		for user in self._users:
			userData = user.toJSON();
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
		for user in self._users:
			if user._id == p_id:
				return user;

		return None;


	# Add user ---
	def addUser(self, p_id, p_name):
		if self.getUserByID(p_id) is not None:
			print("ERROR: trying to add existing user " + p_pid);
			return;

		newUser = user.UserData();
		newUser._id = p_id;
		newUser._name = p_name;
		self._users.append(newUser);


	# Add quest place ---
	def addQuestPlace(self, p_questPlaceData):
		self._questPlaces.append(p_questPlaceData);


	# Add quest ---
	def addQuest(self, p_quest):
		self._activeQuests.append(p_quest);


	# Get active quest by id ---
	def getQuestByID(self, p_placeID):
		for quest in self._activeQuests:
			if quest._placeData._id == p_placeID:
				return quest;

		return None;



# eof

