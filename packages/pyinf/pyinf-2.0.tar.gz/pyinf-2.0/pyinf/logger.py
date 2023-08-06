# -*- coding: utf-8 -*-
import copy
import logging
import logging.config
import logging.handlers


DEFAULT_CONFIG_DICT = {
    'version': 1,
    'formatters': {
        'basic': {
            'format': '[%(asctime)s] %(name)s %(levelname)s in'
                      ' %(module)s %(message)s'
        },
        'advanced': {
            'format': '________________________________________\n'
                      '[%(asctime)s] %(name)s %(process)d %(levelname)s'
                      ' in %(module)s [%(pathname)s:%(lineno)d]: '
                      '%(message)s\n'
        },
    },
    'handlers': {
        'stream_handler': {
            'level': 'DEBUG',
            'formatter': 'basic',
            'class': 'logging.StreamHandler',
        },
        'file_handler': {
            'level': 'DEBUG',
            'formatter': 'advanced',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/tmp/Pyinf.log',
        },
    },
    'loggers': {
        'Pyinf': {
            'handlers': ['stream_handler', 'file_handler'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}


class Logger(object):
    """
    Handles the logging as a common module for code reuse.
    The available options to set are:
       - config:    a dict like config can be standard logging
                    dict config or the pyinf config.
       - level:     log level for all the handlers.
       - formatter: log formatter for all the handlers.
       - log_file:  log_file for all file handlers.
    """

    # Inner class to store the static information
    class LogHandler:
        """
        Inner class to store the static information of logger
        """
        def __init__(self):
            self.loggers = []
            self.file_handlers = []
            self.console_handler = None
            self.email_handler = None

    __instance = None

    def __init__(self, **kwargs):
        """
        load the config or use default config to initial the loggers
        logging.getLogger('name') to get the generated logger.
        """
        # Initialize the default values
        self.level = None
        self.default_level = logging.DEBUG
        self.log_file = None
        self.formatter = None
        self.default_formatter =\
            '________________________________________\n' \
            '%(name)s %(process)d %(levelname)s in %(module)s' \
            ' [%(pathname)s:%(lineno)d]:\n%(message)s\n'

        self.default_config = DEFAULT_CONFIG_DICT
        self.config = None
        self.name = 'Pyinf'

        # Gets specific passed values as parameters
        parameters = [
            "level",
            "log_file",
            "formatter",
            "config",
            "default_config"
        ]

        for i in parameters:
            if (i in kwargs) and not (kwargs[i] is None):
                setattr(self, i, kwargs[i])

        # Init the logging system
        self.__init_logger()

        if self.log_file:
            # Clear the fileHandler associated to loggers
            self.__clear_logger()

            for logger_name in self.__instance.loggers:

                # Creating the logger with the name
                logger = logging.getLogger(logger_name)

                logger.propagate = False

                # Creates a file handler to set to the logger
                handler = self.__get_file_handler(self.log_file)

                # Stores the file handler into internal __instance
                self.__instance.file_handlers.append(handler)
                logger.addHandler(handler)

    def __get_file_handler(self, log_file):
        """
        Get a new FileHandler with specific values.
        """
        handler = logging.handlers.WatchedFileHandler(log_file)

        if self.level:
            handler.setLevel(self.level)
        else:
            handler.setLevel(self.default_level)

        if self.formatter:
            format = logging.Formatter(self.formatter)
            handler.setFormatter(format)
        else:
            format = logging.Formatter(self.default_formatter)
            handler.setFormatter(format)
        return handler

    def __clear_logger(self):
        """
        Clear the current logger. Removes all the file handlers in the Logger.
        """
        for hdlr in self.__instance.file_handlers:
            for logger in self.__instance.loggers:
                logging.getLogger(logger).removeHandler(hdlr)

            hdlr.close()

        self.__instance.file_handlers = []

    def __init_logger(self):
        """
        Initialize the Logger with values from config
        """
        Logger.__instance = Logger.LogHandler()

        # Clear the logging.Logger.manager in case
        # there are previous Logger with same name
        logging.Logger.manager.loggerDict = {}

        if self.config and isinstance(self.config, dict):

            # Process the pyinf_config to get logging settings
            if self.config.__class__.__name__ == 'Config':
                pyinf_config = self.__build_dict_config(self.config)
                logging.config.dictConfig(pyinf_config)

                if self.config.get('EMAIL') is True:
                    print("!!!!!!!!!!!!!")
                    self.__init_email_handler(self.config)

            else:
                logging.config.dictConfig(self.config)

        else:
            logging.config.dictConfig(self.default_config)

        # Store the handlers in internal __instance
        for hdlr in logging._handlers.values():
            if isinstance(hdlr, logging.FileHandler):
                self.__instance.file_handlers.append(hdlr)
            else:
                self.__instance.console_handler = hdlr

        # Apply the input level and format setting
        self.__apply_extra_config()

        # Store the logger names in internal __instance
        self.__instance.loggers = self.__get_logger_in_config()

    def __init_email_handler(self, config):
        """
        Initialize the email handler with values from config
        """
        email_config = config.get_namespace('EMAIL_')
        mail_server = email_config['server']
        mail_port = email_config['port']
        fromaddr = email_config['from']
        toaddrs = email_config['to']
        subject = email_config.get(
            'subject', 'Logging email from pyinf_logging module'
        )
        log_level = email_config.get('log_level')
        credentials = (
            email_config['username'],
            email_config['password']
        )

        mail_handler = logging.handlers.SMTPHandler(
            mailhost=(mail_server, mail_port),
            fromaddr=fromaddr,
            toaddrs=toaddrs,
            subject=subject,
            credentials=credentials,
            secure=None
        )

        if log_level:
            mail_handler.setLevel(log_level)
        else:
            mail_handler.setLevel(logging.CRITICAL)

        logger = logging.getLogger(self.name)
        logger.addHandler(mail_handler)
        self.__instance.email_handler = mail_handler

    def __get_logger_in_config(self):
        """
        This method looks for a loggers which are defined in the config
        """
        if self.config and self.config.__class__.__name__ != 'Config':
            loggers = self.config.get("loggers")
            if loggers:
                return loggers.keys()
        else:
            return DEFAULT_CONFIG_DICT['loggers'].keys()

    def __build_dict_config(self, input_config):
        """
        build new logging dict from pyinf_config base on the default
        support below settings:

        DEBUG: to set Pyinf logger's level (not handlers)
        LOG_FORMAT: to set all the formatters
        LOG_FILE_CLASS: to set the file handler class
        LOG_FILE: to set file handler log file
        LOG_ENABLE_CONSOLE: set True to enable StreamHandler
        """
        config = copy.deepcopy(DEFAULT_CONFIG_DICT)

        debug_mode = input_config.get('DEBUG')
        if debug_mode:
            for k, v in config['loggers'].items():
                v['level'] = 'DEBUG'

        log_config = input_config.get_namespace('LOG_')

        format = log_config.get('format')
        if format:
            for k, v in config['formatters'].items():
                v['format'] = format

        file_class = log_config.get('file_class')
        if file_class:
            config['handlers']['file_handler']['class'] = file_class

        log_file = log_config.get('file')
        if log_file:
            config['handlers']['file_handler']['filename'] = log_file

        enable_console = log_config.get('enable_console')
        if not enable_console and not debug_mode:
            config['loggers']['Pyinf']['handlers'].remove('stream_handler')

        return config

    def __apply_extra_config(self):
        """
        apply the rest of the input parameter configs
        """
        hdlrs = []
        hdlrs.extend(self.__instance.file_handlers)
        hdlrs.append(self.__instance.console_handler)
        hdlrs.append(self.__instance.email_handler)
        hdlrs = [i for i in hdlrs if i]

        if self.formatter:
            for hdlr in hdlrs:
                formatter = logging.Formatter(self.formatter)
                hdlr.setFormatter(formatter)

        if self.level:
            for hdlr in hdlrs:
                hdlr.setLevel(self.level)
