class PyCommanderError(Exception):
  # General errors
  pass

class PyCommanderInputError(PyCommanderError):
  # Input errors, i.e. return code -1 or 255
  pass

class PyCommanderRuntimeError(PyCommanderError):
  # Runtime errors, i.e. return code -2 or 254
  pass
