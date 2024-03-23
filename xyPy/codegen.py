import tempfile, subprocess, ctypes, pathlib

class ClangProgram:
  def __init__(self, code: str, use_temp: bool = True) -> None:
    if not use_temp: self.code = code
    self.code = f"""#include <math.h> 
    void prg(float* x_coords, float* y_coords, float min_x, float max_x, float step) {{int num_points = round((max_x - min_x)/step) + 1;float x = min_x;for (int i = 0; i <= num_points; ++i) {{x_coords[i] = x;y_coords[i] = {code};x += step;}}}}"""
    self.compiled = None
    self.fxn = None
  
  def compile(self):
    with tempfile.NamedTemporaryFile(delete=True) as output_file:
      arguments = f"clang -x c - -shared -O2 -o {output_file.name}".split()
      try: subprocess.check_output(args=arguments, input=self.code.encode("utf-8"), stderr=subprocess.PIPE)
      except subprocess.CalledProcessError as e: print(f"Error during compilation: {e.stderr.decode()}")
      self.compiled = pathlib.Path(output_file.name).read_bytes()
  
  def __call__(self, *bufs, values=(), argtypes=None):
    if self.fxn: return self.fxn.prg(*bufs, *values)
    if not argtypes: raise Exception("Argtypes for function must be defined")
    if not self.compiled: raise Exception("Program not compiled!")
    with tempfile.NamedTemporaryFile(delete=True) as cached_file_path:
      pathlib.Path(cached_file_path.name).write_bytes(self.compiled)
      self.fxn = ctypes.CDLL(str(cached_file_path.name))
      self.fxn.prg.argtypes = argtypes
      self.fxn.prg(*bufs, *values)