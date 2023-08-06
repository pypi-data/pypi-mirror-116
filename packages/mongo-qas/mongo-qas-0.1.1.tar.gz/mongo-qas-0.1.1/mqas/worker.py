from .queue import Queue
from .job import Job
from typing import Type, Union, Tuple, Callable
from time import sleep
from threading import Thread
import importlib

class Worker:

  def __init__(self, queues: Union[Tuple[Queue,...], Type[Queue]], channel: Union[Tuple[str,...], str]=None, heart_beat: int = 1, verbosity: str = "error", logger: Union[str, Callable] = None ) -> None:
    
    if isinstance(queues, tuple) or isinstance(queues, list):
      self.queues = queues
    elif isinstance(queues, Queue):
      self.queues = tuple([queues])

    if isinstance(channel, tuple) or isinstance(channel, list):
      self._channels = channel
    elif isinstance(channel, str):
      self._channels = [channel]
    else:
      self._channels = None

    self._working = False
    self._heart_beat = heart_beat
    self._running = False

    self._verbosity = verbosity
    self.setLogger(logger)
    
  def setLogger(self, logger: Union[str, Callable]):
    if callable(logger):
      self._logger = logger
    elif isinstance(logger, str):
      callback = str(logger)
      if str(callback).__contains__("."):
        mod_name, func_name = callback.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        func = getattr(mod, func_name)
        self._logger = func
      elif callback in globals():
        func = globals()[callback]
        self._logger = func
    else:
      self._logger = None

  def setVerbosity(self, verbosity: str):
    self.verbosity = verbosity

  def start(self):
    self._running = True
    self._run()

  def stop(self):
    self._running = False

  def _work(self):
    self._working = True
    job: Type[Job] = None

    for queue in self.queues:
      if self._channels is None:
        job = queue.dequeue()
        if not job is None:
          break
      else:
        for channel in self._channels:
          job = queue.dequeue(channel)
          if not job is None:
            break
        if not job is None:
          break

    if not job is None:
      self.thread = Thread(target=self._run_job, kwargs={'job': job})
      self.thread.start()
      self.thread.join()
      self._working = False
    else:
      self._working = False

  def _run_job(self, job: Type[Job]):
    payload = job.payload
    job.setVerbosity(self._verbosity)
    job.setLogger(self._logger)
    try:
      if not payload is None:
        callback = payload.get("function_name")
        if not callback is None:
          if str(callback).__contains__("."):
            mod_name, func_name = callback.rsplit(".", 1)
            mod = importlib.import_module(mod_name)
            func = getattr(mod, func_name)
            args = payload.get("args", [])
            kwargs = payload.get("kwargs", {})
            result = func(*args, **kwargs)
            job.complete(result)
          elif callback in globals():
            func = globals()[callback]
            args = payload.get("args", [])
            kwargs = payload.get("kwargs", {})
            result = func(*args, **kwargs)
            job.complete(result)
          else:
            job.error(f"Function {callback} not found!")

    except Exception as ex:
      job.error(f"Error: {ex}")
      print(f"Error: {ex}")

  def _run(self):
    while True:
      if not self._running:
        break

      if not self._working:
        self._work()

      sleep(self._heart_beat)