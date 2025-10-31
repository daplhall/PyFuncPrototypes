from abc import abstractmethod
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Any, Protocol

from pyprototypes.exceptions import FixtureNotDefined
from pyprototypes.signature import SigMeta
from pyprototypes.stack import DictStack


class FixFinder_t(Protocol):
	@abstractmethod
	def match(
		self, signature: SigMeta, fixtures: dict[str, SigMeta]
	) -> dict[str, Any]:
		raise NotImplementedError


@dataclass
class MachineData:
	arg_stack: DictStack
	fixtures: dict[str, SigMeta]
	recursion_retrn: dict[str, Any]


@dataclass
class Output:
	kwards: dict


class States(IntEnum):
	CHECK_FOR_ARGS = auto()
	FIXTURE_CHOICE = auto()
	RECURSION = auto()
	EVALUATE = auto()
	NOT_FIXTURE = auto()
	EXIT = auto()


class FixFinder:
	"""
	output: dict of collapsed attributes
	"""

	def __init__(self):
		self.states = {
			States.CHECK_FOR_ARGS: self.check_for_args,
			States.FIXTURE_CHOICE: self.fixture_choice,
			States.RECURSION: self.recursion,
			States.EVALUATE: self.evaluate,
			States.NOT_FIXTURE: self.not_fixture,
		}

	def match(
		self, signature: SigMeta, fixtures: dict[str, SigMeta]
	) -> dict[str, Any]:
		data = MachineData(DictStack(signature), fixtures, {})
		out = Output({})
		state = States.CHECK_FOR_ARGS
		while state != States.EXIT:
			callback = self.states[state]
			state = callback(data, out)
		return out.kwards

	def check_for_args(self, data: MachineData, out: Output) -> States:
		if not data.arg_stack:
			return States.EXIT
		return States.FIXTURE_CHOICE

	def fixture_choice(self, data: MachineData, out: Output) -> States:
		arg, _ = data.arg_stack.top()
		if arg in data.fixtures:
			fixture = data.fixtures[arg]
			if fixture.signature:
				return States.RECURSION
			else:
				return States.EVALUATE
		else:
			return States.NOT_FIXTURE

	def evaluate(self, data: MachineData, out: Output) -> States:
		arg, _ = data.arg_stack.pop()
		if data.fixtures[arg].signature:
			out.kwards[arg] = data.fixtures[arg].func(**data.recursion_retrn)
		else:
			out.kwards[arg] = data.fixtures[arg].func()
		return States.CHECK_FOR_ARGS

	def recursion(self, data: MachineData, out: Output) -> States:
		arg, _ = data.arg_stack.top()
		data.recursion_retrn = self.match(data.fixtures[arg], data.fixtures)
		return States.EVALUATE

	def not_fixture(self, data: MachineData, out: Output) -> States:
		name, _ = data.arg_stack.top()
		raise FixtureNotDefined(f"Fixture '{name}' is not defined\n")
		return NotImplemented
