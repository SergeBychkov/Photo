from dataclasses import dataclass


@dataclass
class FileInfo:
  path: str
  name: str
  dt: str | None = None

  def __str__(self):
    return f"{self.name} - {self.path} - {self.dt}"

  def __hash__(self):
    return hash((self.path, self.name))

