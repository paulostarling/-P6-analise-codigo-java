
class RepositoryMetrics:
  def __init__(self, name, repo_clone_url, age, releases_number, loc, cbo, dit, lcon):
    self.name = name
    self.repo_clone_url = repo_clone_url
    self.age = age
    self.releases_number = releases_number
    self.loc = loc
    self.cbo = cbo
    self.dit = dit
    self.lcon = lcon