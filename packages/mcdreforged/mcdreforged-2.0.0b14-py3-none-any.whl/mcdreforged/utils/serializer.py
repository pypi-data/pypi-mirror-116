import copy
from abc import ABC
from typing import Union, TypeVar, List, Dict, Type

T = TypeVar('T')


def serialize(obj) -> Union[None, int, float, str, list, dict]:
	if obj is None or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, str):
		return obj
	elif isinstance(obj, list) or isinstance(obj, tuple):
		return list(map(serialize, obj))
	elif isinstance(obj, dict):
		return dict(map(lambda t: (t[0], serialize(t[1])), obj.items()))
	try:
		attr_dict = vars(obj)
		# don't serialize protected fields
		for attr_name in list(attr_dict.keys()):
			if attr_name.startswith('_'):
				attr_dict.pop(attr_name)
	except TypeError:
		raise TypeError('Unsupported input type {}'.format(type(obj))) from None
	else:
		return serialize(attr_dict)


def deserialize(data, cls: Type[T], *, error_at_missing=False, error_at_redundancy=False) -> T:
	# Element (None, int, float, str, list, dict)
	if type(data) is cls:
		return data
	# float thing
	elif cls is float and isinstance(data, int):
		return float(data)
	# List
	elif isinstance(data, list) and getattr(cls, '__origin__', None) == List[int].__origin__:
		element_type = getattr(cls, '__args__')[0]
		return list(map(lambda e: deserialize(e, element_type, error_at_missing=error_at_missing, error_at_redundancy=error_at_redundancy), data))
	# Dict
	elif isinstance(data, dict) and getattr(cls, '__origin__', None) == Dict[int, int].__origin__:
		key_type = getattr(cls, '__args__')[0]
		val_type = getattr(cls, '__args__')[1]
		instance = {}
		for key, value in data.items():
			deserialized_key = deserialize(key, key_type, error_at_missing=error_at_missing, error_at_redundancy=error_at_redundancy)
			deserialized_value = deserialize(value, val_type, error_at_missing=error_at_missing, error_at_redundancy=error_at_redundancy)
			instance[deserialized_key] = deserialized_value
		return instance
	# Object
	elif isinstance(data, dict):
		try:
			result = cls()
		except TypeError:
			raise TypeError('Parameter cls needs to be a type instance since data is a dict, but {} found'.format(type(cls))) from None
		input_key_set = set(data.keys())
		for attr_name, attr_type in getattr(cls, '__annotations__', {}).items():
			if not attr_name.startswith('_'):
				if attr_name in data:
					result.__setattr__(attr_name, deserialize(data[attr_name], attr_type, error_at_missing=error_at_missing, error_at_redundancy=error_at_redundancy))
					input_key_set.remove(attr_name)
				elif error_at_missing:
					raise ValueError('Missing attribute {} for class {} in input object {}'.format(attr_name, cls, data))
				elif hasattr(cls, attr_name):
					result.__setattr__(attr_name, copy.copy(getattr(cls, attr_name)))
		if error_at_redundancy and len(input_key_set) > 0:
			raise ValueError('Redundancy attributes {} for class {} in input object {}'.format(input_key_set, cls, data))
		if isinstance(result, Serializable):
			result.on_deserialization()
		return result
	# Union
	elif getattr(cls, '__origin__', None) == Union:
		for possible_cls in getattr(cls, '__args__'):
			try:
				return deserialize(data, possible_cls, error_at_missing=error_at_missing, error_at_redundancy=error_at_redundancy)
			except (TypeError, ValueError):
				pass
		raise TypeError('Data in type {} cannot match any candidate of target class {}'.format(type(data), cls))
	else:
		raise TypeError('Unsupported input type: expected class {} but found data with class {}'.format(cls, type(data)))


class Serializable(ABC):
	def __init__(self, **kwargs):
		if len(kwargs) > 0:
			self.update_from(kwargs)

	def serialize(self) -> dict:
		return serialize(self)

	@classmethod
	def deserialize(cls, data: dict, **kwargs):
		return deserialize(data, cls, **kwargs)

	def update_from(self, data: dict):
		vars(self).update(vars(self.deserialize(data)))

	@classmethod
	def get_default(cls):
		return cls.deserialize({})

	def on_deserialization(self):
		"""
		Invoked after being deserialized
		"""
		pass
