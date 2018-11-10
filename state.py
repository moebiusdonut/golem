# state.py

import json
import quest

# ---------------------
#      GameState
# ---------------------
class GameState:
	_questPlaces  = [];
	_activeQuests = [];

	
	# Ctor ---
	def __init__(self):
		pass;


	# Load game state from save file ---
	def load(self):
		with open('save.json') as file:
			data = json.load(file);

		places = data['places'];
		for placeData in places:
			place = quest.QuestPlaceData('', '', '');
			place.fromJSON(placeData);
			self._questPlaces.append(place);


	# Save game state from save file ---
	def save(self):
		data = {};

		placesDataArray = [];
		for place in self._questPlaces:
			placeData = place.toJSON();
			placesDataArray.append(placeData);

		data['places'] = placesDataArray;

		with open('save.json', 'w') as outfile:
			json.dump(data, outfile);


	# Add quest place ---
	def addQuestPlace(self, p_questPlaceData):
		self._questPlaces.append(p_questPlaceData);
