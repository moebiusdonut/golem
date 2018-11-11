# user

# ---------------------
#    UserData
# ---------------------
class UserData:
	_id        = "";
	_name      = "";
	_alterName = "";
	_credits   = 0;


	# Ctor ---
	def __init__(self):
		pass;


	# Init from JSON ---
	def fromJSON(self, p_data):
		self._id        = p_data['id'];
		self._name      = p_data['name'];
		self._alterName = p_data['altername'];
		self._credits   = p_data['creadits'];


	# Serialize to JSON ---
	def toJSON(self):
		data              = {};
		data['id']        = self._id;
		data['name']      = self._name;
		data['altername'] = self._alterName;
		data['creadits']  = self._credits;
		return data;


	# Get name representation ---
	def getNameRepresentation(self):
		username = self._name;
		if self._alterName != "":
			username += " aka " + self._alterName;

		return username;

#eof
