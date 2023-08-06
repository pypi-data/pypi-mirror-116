# Python Logger

PySimpleLogger is a very simple logging library for Python.

Its main functionalities are based on the Python logging library with some tweaks.

Currently, it is based on the Singleton pattern. So, only one logger instance can be created.

# (Very short) Tutorial

First create a `Logger` instance:

```python
from PyLogger import Logger
logger = Logger() # using current work directory
logger = Logger(path_to_log_file) # or using custom path
```

Then log whatever you want to:

```
logger.info("Some info")
logger.warning("Some warning")
logger.error("Some error")
```

It currently accepts prefix, end and sep kwargs for logging.
