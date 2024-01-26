"""
Created Date: 2023-12-Tu
Author: Lucas Barrez
-----
Last Modified: Thursday, 26th January
Modified By: Lucas Barrez
-----
HISTORY:
"""

from multiprocessing import Process, Queue
from typing import Any, Dict, Type
from datetime import datetime
import logging
import pytz
import os
import signal

t_message_queue = Type["Queue[Dict[Any, Any]]"]


class CustomLogger(Process):
    def __init__(self):
        Process.__init__(self)

    @staticmethod
    def process(
        message_queue: t_message_queue, evt: Any, debug_log_level: bool
    ):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        log_level = logging.INFO
        if debug_log_level == True:
            log_level = logging.DEBUG
        formatter = Formatter(
            fmt="%(asctime)s [%(name)s] %(levelname)s %(message)s"
        )
        # app Logger
        app_logger = logging.getLogger("APP LOGGER")
        hdlr_2 = logging.FileHandler("log/app.log")
        hdlr_2.setFormatter(formatter)
        app_logger.setLevel(log_level)
        app_logger.addHandler(hdlr_2)
        app_logger.log(
            logging.INFO,
            "+++++++++++++++++ STARTING APP - log Level:"
            f" {log_level} +++++++++++++++++",
        )
        app_logger.log(logging.INFO, f"Logger pid: {os.getpid()}")

        # error Logger
        error_logger = logging.getLogger("ERROR LOGGER")
        hdlr_4 = logging.FileHandler("log/error.log")
        hdlr_4.setFormatter(formatter)
        error_logger.setLevel(log_level)
        error_logger.addHandler(hdlr_4)

        try:
            while not evt.is_set():
                if message_queue.empty():  # type: ignore
                    continue
                payload = message_queue.get()  # type: ignore
                level = eval(f"logging.{payload['type'].upper()}")
                fichier_log = payload["log"].lower()
                exec(f'{fichier_log}_logger.log({level}, payload["message"])')
            app_logger.log(
                logging.INFO,
                "+++++++++++++++++ STOPPING APP FROM LOGGER +++++++++++++++++",
            )
        except Exception as ex:
            app_logger.log(logging.ERROR, ex)


class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""

    def converter(self, timestamp: float) -> datetime:
        dt = datetime.fromtimestamp(timestamp, tz=pytz.timezone("Europe/Paris"))
        return dt

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec="milliseconds")
            except TypeError:
                s = dt.isoformat()
        return s
