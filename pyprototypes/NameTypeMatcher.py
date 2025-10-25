from dataclasses import dataclass
from enum import IntEnum, auto

from pyprototypes.BaseMatchers import NameMatcher, TypeMatcher, FuncMetaData
from pyprototypes.exceptions import UnsupportedParameters


class States(IntEnum):
	MATCH_NAME = auto()
	NAME_ERROR = auto()
	MATCH_TYPES = auto()
	TYPE_ERROR = auto()
	WITH_TYPES = auto()
	ERROR_HANDLE = auto()
	MATCH = auto()
	ERROR = auto()


@dataclass
class MachineData:
	signature: dict
	inpt: dict
	error_msg: str
	is_typed: bool
	meta: FuncMetaData


class MatcherMachine:
	def __init__(self):
		self.states = {
			States.MATCH_NAME: self.match_name,
			States.NAME_ERROR: self.name_error,
			States.MATCH_TYPES: self.match_types,
			States.WITH_TYPES: self.with_types,
			States.TYPE_ERROR: self.type_error,
			States.ERROR_HANDLE: self.error_handle,
			States.MATCH: self.SHOULD_NOT_RUN,
			States.ERROR: self.SHOULD_NOT_RUN,
		}

	def match(
		self,
		signature: dict,
		inpt: dict,
		meta: FuncMetaData,
		is_typed: bool = True,
	) -> bool:
		state = States.MATCH_NAME
		data = MachineData(signature, inpt, "", is_typed, meta)
		while state != States.ERROR and state != States.MATCH:
			callback = self.states[state]
			state = callback(data)
		if state == States.ERROR:
			return False
		elif state == States.MATCH:
			return True

	@staticmethod
	def match_name(data: MachineData) -> States:
		if NameMatcher.is_odd(data.signature, data.inpt):
			return States.NAME_ERROR
		else:
			return States.WITH_TYPES

	@staticmethod
	def with_types(data: MachineData) -> States:
		if data.is_typed:
			return States.MATCH_TYPES
		else:
			return States.ERROR_HANDLE

	@staticmethod
	def error_handle(data: MachineData) -> States:
		if data.error_msg:
			raise UnsupportedParameters(data.error_msg, data.meta)
		else:
			return States.MATCH

	@staticmethod
	def match_types(data: MachineData) -> States:
		if TypeMatcher.is_odd(data.signature, data.inpt):
			return States.TYPE_ERROR
		else:
			return States.ERROR_HANDLE

	@staticmethod
	def name_error(data: MachineData) -> States:
		matches_tree = []
		for odd in data.inpt:
			if matches := NameMatcher.match_str(data.signature, odd):
				matches_tree.append((odd, matches))
		for written, match in matches_tree:
			data.error_msg += (
				f"* Parameter '{written}' is not supported, did you mean:\n"
			)
			for suggestion in match:
				data.error_msg += f"\t- {suggestion}\n"
		return States.WITH_TYPES

	@staticmethod
	def type_error(data: MachineData) -> States:
		overlap = set(data.signature) & set(data.inpt)
		odd = TypeMatcher.match(overlap, data.signature, data.inpt)
		for param, curr_type, corr_type in odd:
			data.error_msg += (
				f"* Wrong Type - Parameter {param}\n"
				f"\t it is '{curr_type.__name__}' "
				f"it should be '{corr_type.__name__}'\n"
			)
		return States.ERROR_HANDLE

	@staticmethod
	def SHOULD_NOT_RUN(self, data):
		return NotImplemented
