import inspect


class UnsupportedParameters(Exception):
	def __init__(self, matches, wrong_types, function):
		msg = ""
		if wrong_types:
			for param, curr_type, corr_type in wrong_types:
				msg += (
					f"* Wrong Type - Parameter {param}\n"
					f"\t it is '{curr_type.__name__}' "
					f"it should be '{corr_type.__name__}'\n"
				)
		if matches:
			for written, match in matches:
				msg += (
					f"* Parameter '{written}' is not supported, "
					"did you mean:\n"
				)
				for suggestion in match:
					msg += f"\t- {suggestion}\n"
		super().__init__(
			f"\nError in the signature of '{function.__name__}' "
			f"in {inspect.getsourcefile(function)}\n" + msg
		)
