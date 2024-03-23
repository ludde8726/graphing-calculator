import time
from typing import Dict, Tuple
import math

class Timer:
  def __enter__(self):
    self.start_time = time.perf_counter()
    self.other_times : Dict[str, Tuple[float, float]] = {}
    return self
  
  def add_time(self, info: str):
    self.other_times[info] = (time.perf_counter(), 0)
  
  def end_time(self, info: str):
    self.other_times[info] = (self.other_times[info][0], time.perf_counter())

  def get_prefix(self, tot_time: float) -> Tuple[float, str]:
    prefixes = ['s', 'ms', 'us', 'ns', 'ps']
    prefix = math.ceil((-math.log10(tot_time)/3))
    prefix_multiplier = 10**(prefix*3)
    return prefix_multiplier, prefixes[prefix]

  def __exit__(self, exc_type, exc_value, traceback):
    end_time = time.perf_counter()
    prefix_multiplier, prefix = self.get_prefix(end_time-self.start_time)
    print(f"Total time: {(end_time-self.start_time)*prefix_multiplier:.3f}{prefix}")
    infos = self.other_times.keys()
    for i, info in enumerate(infos):
      tot_time = (end_time if self.other_times[info][1] == 0 else self.other_times[info][1]) - self.other_times[info][0]
      prefix_multiplier, prefix = self.get_prefix(tot_time)
      print(f"{info}: {tot_time*prefix_multiplier:.2f}{prefix}")