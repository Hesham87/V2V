import statistics
# {"longitude":_init_float,"latitude":_init_float,"velocity":_init_float,"acceleration":_init_float,"heading":_init_float}
_init_float = -1
class DataManager:
	def __init__(self) -> None:
		self._max_size = 100
		self._dict_prev = {"longitude":_init_float, \
							"latitude":_init_float, \
							"velocity":_init_float, \
							"acceleration":_init_float,\
							"heading":_init_float}

		self._processed_data_dict = {"longitude":_init_float, \
							"latitude":_init_float, \
							"velocity":_init_float, \
							"acceleration":_init_float,\
							"heading":_init_float}

		self._indx_dict ={"longitude":0, \
							"latitude":0, \
							"velocity":0, \
							"acceleration":0,\
							"heading":0}

		self._list_dict = {"longitude":[], \
							"latitude":[], \
							"velocity":[], \
							"acceleration":[],\
							"heading":[]}


	def _get_keys_of_data_changed(self,dict:dict):
		keys = []
		for key in self._dict_prev:
			if dict[key] != self._dict_prev[key]:
				keys.append(key)
		return keys

	def _copy_dicts(self,src:dict,dst:dict ):
		for k in src:
			dst[k] = src [k]

	# def update_data(self,dict:dict):
	# 	keys = self._get_keys_of_data_changed(dict)
	# 	if len(keys) > 0:
	# 		for k in keys:
	# 			if(len(self._list_dict[k])<self._max_size):
	# 				self._list_dict[k].append(dict[k])
	# 			else:
	# 				indx = self._indx_dict[k]
	# 				self._list_dict[k][indx] = dict[k]
	# 				self._indx_dict[k] = self._indx_dict[k] + 1
	# 				if self._indx_dict[k]  >= self._max_size:
	# 					self._indx_dict[k] = 0
	# 	self._copy_dicts(dict,self._dict_prev)

	def update_data(self,dict:dict):
		for k in dict:
			if(len(self._list_dict[k])<self._max_size):
				self._list_dict[k].append(dict[k])
			else:
				indx = self._indx_dict[k]
				self._list_dict[k][indx] = dict[k]
				self._indx_dict[k] = self._indx_dict[k] + 1
				if self._indx_dict[k]  >= self._max_size:
					self._indx_dict[k] = 0
		self._copy_dicts(dict,self._dict_prev)

	def _is_valid_avg_dict_data(self):
		for k in self._processed_data_dict:
			if self._processed_data_dict[k] == _init_float:
				return False

	def get_thresh_low_val(self,dict:dict):
		self._processed_data_dict["longitude"] = dict["longitude"] ## NO threshhold for both latitude and longitude
		self._processed_data_dict["latitude"] = dict["latitude"]
		# if (dict["velocity"] < 1):
		# 	self._processed_data_dict["velocity"] = 0 
		# else: 
		self._processed_data_dict["velocity"] =	dict["velocity"]

		if (dict["acceleration"] < 1):
			self._processed_data_dict["acceleration"] = 0 
		else: 
			self._processed_data_dict["acceleration"] =	dict["acceleration"]
	
		self._processed_data_dict["heading"] = dict["heading"] 
		return self._processed_data_dict
		
	def _is_data_changed(self,dict:dict)-> bool:
		for key in self._dict_prev:
			if self._dict_prev[key] != dict[key]:
				return True
			return False

	def get_avg_data(self,dict:dict)->dict:
		for k in self._processed_data_dict:
			avg = 0
			for d in self._list_dict[k]:
				avg = avg + d
			length= len( self._list_dict[k])
			avg = avg / length
			self._processed_data_dict[k] = avg
		if self._is_valid_avg_dict_data():
			return self._processed_data_dict
		else:
			return self._dict_prev

	def get_median_data(self,dict:dict) -> dict:
		for k in dict:
			self._processed_data_dict[k] = statistics.median(self._list_dict[k])
		return self._processed_data_dict