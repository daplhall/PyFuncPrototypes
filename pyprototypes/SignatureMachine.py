from abc import abstractmethod
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Protocol

from pyprototypes.BaseMatchers import (
	MetaSignature,
	NameMatcher,
	TypeMatcher,
)
from pyprototypes.exceptions import UnsupportedParameters


class SignatureMachineInterface(Protocol):
	is_typed: bool

	@abstractmethod
	def match(self, reference: MetaSignature, inpt: MetaSignature):
		pass


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
	reference: MetaSignature
	inpt: MetaSignature
	error_msg: str
	is_typed: bool


class SignatureMachine:
	def __init__(self, is_typed):
		self.is_typed = True
		self.states = {
			States.MATCH_NAME: self.match_name,
			States.NAME_ERROR: self.name_error,
			States.MATCH_TYPES: self.match_types,
			States.WITH_TYPES: self.with_types,
			States.TYPE_ERROR: self.type_error,
			States.ERROR_HANDLE: self.error_handle,
		}

	def match(
		self,
		signature: dict,
		inpt: dict,
	) -> bool:
		state = States.MATCH_NAME
		data = MachineData(signature, inpt, "", self.is_typed)
		while state != States.MATCH:
			callback = self.states[state]
			state = callback(data)
		if state == States.MATCH:
			return True

	@staticmethod
	def match_name(data: MachineData) -> States:
		if NameMatcher.has_oddities(
			data.reference.signature, data.inpt.signature
		):
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
			raise UnsupportedParameters(data.error_msg, data.inpt)
		else:
			return States.MATCH

	@staticmethod
	def match_types(data: MachineData) -> States:
		if TypeMatcher.has_oddities(
			data.reference.signature, data.inpt.signature
		):
			return States.TYPE_ERROR
		else:
			return States.ERROR_HANDLE

	@staticmethod
	def name_error(data: MachineData) -> States:
		matches_tree = []
		for odd in data.inpt.signature:
			if not NameMatcher.is_odd(data.reference.signature, odd):
				continue
			if matches := NameMatcher.match_str(data.reference.signature, odd):
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
		overlap = set(data.reference.signature) & set(data.inpt.signature)
		odd = TypeMatcher.match(overlap, data.reference.signature, data.inpt)
		for param, curr_type, corr_type in odd:
			data.error_msg += (
				f"* Wrong Type - Parameter '{param}'\n"
				f"\t it is '{curr_type.__name__}' "
				f"it should be '{corr_type.__name__}'\n"
			)
		return States.ERROR_HANDLE
