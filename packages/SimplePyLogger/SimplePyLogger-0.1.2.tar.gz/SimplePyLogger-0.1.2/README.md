# Python Logger

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

You can use any `print()` kwargs.
