from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Any

from pyprototypes.DictStack import DictStack
from pyprototypes.exceptions import FixtureNotDefined

EMPTY = None


@dataclass
class MachineData:
	signature: DictStack
	fixtures: dict[str]
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


class FixtureMachine:
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

	def match(self, inpt_signature, fixtures) -> dict[str, Any]:
		data = MachineData(DictStack(inpt_signature), fixtures, {})
		out = Output({})
		state = States.CHECK_FOR_ARGS
		while state != States.EXIT:
			callback = self.states[state]
			state = callback(data, out)
		return out.kwards

	@staticmethod
	def check_for_args(data: MachineData, out: Output) -> States:
		if not data.signature:
			return States.EXIT
		return States.FIXTURE_CHOICE

	@staticmethod
	def fixture_choice(data: MachineData, out: Output) -> States:
		arg, _ = data.signature.top()
		if arg in data.fixtures:
			fixture = data.fixtures[arg]
			if fixture.signature:
				return States.RECURSION
			else:
				return States.EVALUATE
		else:
			return States.NOT_FIXTURE

	@staticmethod
	def evaluate(data: MachineData, out: Output) -> States:
		arg, _ = data.signature.pop()
		if data.fixtures[arg].signature:
			out.kwards[arg] = data.fixtures[arg].func(**data.recursion_retrn)
		else:
			out.kwards[arg] = data.fixtures[arg].func()
		return States.CHECK_FOR_ARGS

	@staticmethod
	def recursion(data: MachineData, out: Output) -> States:
		arg, _ = data.signature.top()
		machine = FixtureMachine()
		data.recursion_retrn = machine.match(data.fixtures[arg], data.fixtures)
		return States.EVALUATE

	@staticmethod
	def not_fixture(data: MachineData, out: Output) -> States:
		name, _ = data.signature.top()
		raise FixtureNotDefined(f"Fixture '{name}' is not defined\n")
		return NotImplemented
