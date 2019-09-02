import inspect
import logging
from functools import wraps

from meiga.result import Result


class LoggingDecorator(object):
    def __init__(self, log_level, message, *, logger=None):
        self.log_level = log_level
        self.message = message
        self._logger = logger

    def before_execution(self, fn, *args, **kwargs):
        pass

    def after_execution(self, fn, result, *args, **kwargs):
        pass

    def on_error(self, fn, result, *args, **kwargs):
        pass

    @staticmethod
    def log(logger, log_level, msg):
        logger.log(log_level, msg)

    def get_logger(self, fn):
        if self._logger is None:
            self._logger = logging.getLogger(fn.__module__)

        return self._logger

    @staticmethod
    def build_extensive_kwargs(fn, *args, **kwargs):
        function_signature = inspect.signature(fn)
        extensive_kwargs = function_signature.bind_partial(*args, **kwargs)

        return extensive_kwargs.arguments

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            self.before_execution(fn, *args, **kwargs)

            result = fn(*args, **kwargs)

            if isinstance(result, Result) and result.is_failure:
                self.on_error(fn, result, *args, **kwargs)
            else:
                self.after_execution(fn, result, *args, **kwargs)
            return result

        return wrapper


class log_on_start(LoggingDecorator):
    def before_execution(self, fn, *args, **kwargs):
        logger = self.get_logger(fn)
        extensive_kwargs = self.build_extensive_kwargs(fn, *args, **kwargs)
        msg = self.message.format(**extensive_kwargs)

        self.log(logger, self.log_level, msg)


class log_on_end(LoggingDecorator):
    def __init__(
        self, log_level, message, *, logger=None, result_format_variable="result"
    ):
        super().__init__(log_level, message, logger=logger)
        self.result_format_variable = result_format_variable

    def after_execution(self, fn, result, *args, **kwargs):
        logger = self.get_logger(fn)
        extensive_kwargs = self.build_extensive_kwargs(fn, *args, **kwargs)
        extensive_kwargs[self.result_format_variable] = result
        msg = self.message.format(**extensive_kwargs)

        self.log(logger, self.log_level, msg)


class log_on_error(LoggingDecorator):
    def __init__(self, log_level, message, *, logger=None):
        super().__init__(log_level, message, logger=logger)

    def _log_error(self, fn, message, *args, **kwargs):
        logger = self.get_logger(fn)
        extensive_kwargs = self.build_extensive_kwargs(fn, *args, **kwargs)
        extensive_kwargs["error"] = message
        msg = self.message.format(**extensive_kwargs)
        self.log(logger, self.log_level, msg)

    def on_error(self, fn, result, *args, **kwargs):
        if result.is_failure:
            message = getattr(result.value, "message", None)
            if not message:
                message = result.value.__class__.__name__

            self._log_error(fn, message, *args, **kwargs)
