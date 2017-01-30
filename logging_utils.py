from logging import Logger

from sficopaf.var_checker import check_var


class IndentedLogger(Logger):

    """
    A utility to create a logger with an indentation string automatically added at the beginning of every message
    """
    def __init__(self, logger: Logger, msg_prefix: str = None, indentation_level: int = None):

        check_var(logger, var_types=Logger, var_name='logger')
        self.logger = logger

        msg_prefix = msg_prefix or '--'
        check_var(msg_prefix, var_types=str, var_name='indent_str')
        self.msg_prefix = msg_prefix

        indentation_level = indentation_level or 0
        check_var(indentation_level, var_types=int, var_name='nb_indents')
        self.indentation_level = indentation_level

    def __getattr__(self, item):
        # easy version of the dynamic proxy just to save time :)
        # see http://code.activestate.com/recipes/496741-object-proxying/ for "the answer"

        # this is called only if the attribute was not found the usual way
        lg = object.__getattribute__(self, 'logger')
        if hasattr(lg, item):
            return getattr(lg, item)
        else:
            raise AttributeError('\'' + self.__class__.__name__ + '\' object has no attribute \'' + item + '\'')

    def _log(self, level, msg, *args, **kwargs):
        prefix = ''
        for i in range(self.indentation_level):
            prefix += self.msg_prefix

        self.logger._log(level, prefix + msg, *args, **kwargs)

    def indent(self):
        """
        Returns a new IntendedLogger with one more indentation level
        :return:
        """
        return IndentedLogger(self.logger, self.msg_prefix, self.indentation_level + 1)