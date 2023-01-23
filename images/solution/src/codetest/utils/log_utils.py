import logging


def get_custom_logger(name:str, log_level:int=logging.DEBUG) -> logging.Logger:
    """Function to return a custom formatted logger object

    Args:
        name (str): name of logger
        log_level (int, optional): desired logging level. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: custom formatted Logger streaming to stdout
    """
    logger = logging.getLogger(name)
    
    # handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    # formatters
    formatter = logging.Formatter(f'[%(name)s][%(asctime)s][%(levelname)s]:  %(message)s', "%Y-%m-%d %H:%M:%S")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(log_level)

    return logger


if __name__ == "__main__":
    logger = get_custom_logger('Logger')
    logger.info('Hello World')