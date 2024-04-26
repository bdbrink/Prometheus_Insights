import psutil
import subprocess

def check_prometheus_process():
  """Checks if the Prometheus process is running."""
  for proc in psutil.process_iter():
    if proc.name() == "prometheus":
      return proc
  return None

def check_prometheus_port(port):
  """Checks if the Prometheus port is open."""
  try:
    subprocess.check_output(["nc", "-z", "localhost", str(port)])
    return True
  except subprocess.CalledProcessError:
    return False

def check_disk_space(path):
  """Checks available disk space on the path where Prometheus data is stored."""
  try:
    disk_usage = psutil.disk_usage(path)
    free_space_percent = disk_usage.free / disk_usage.total * 100
    if free_space_percent < 10:
      print(f"Warning: Low disk space available on {path} ({free_space_percent:.1f}%)")
  except (PermissionError, FileNotFoundError):
    print(f"Error: Unable to check disk space for {path}")

def main():
  # Check if Prometheus process is running
  prometheus_proc = check_prometheus_process()
  if not prometheus_proc:
    print("Error: Prometheus process not found!")
  else:
    print(f"Prometheus process running (PID: {prometheus_proc.pid})")

  # Check if Prometheus port is open
  if not check_prometheus_port(9090):
    print("Error: Prometheus port (9090) is not open!")

  # Check disk space for Prometheus data directory (replace with your actual path)
  check_disk_space("/var/lib/prometheus")

if __name__ == "__main__":
  main()