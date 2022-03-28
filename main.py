from itertools import count
import math
import requests
import csv
import numpy as np
from git import Repo
from datetime import date
from datetime import datetime
import subprocess
import numpy as np
from entities.RepositoryCkData import RepositoryCkData
import shutil
import stat
import os

from entities.RepositoryMetrics import RepositoryMetrics

api_token = 'place_the_token_here'

headers = {'Authorization': 'token %s' % api_token}

# Get repository CK metrics
def get_repository_ck_data():
  with open('class.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, quotechar='|')
    next(spamreader)
    loc_total = 0
    cbo_array  = []
    dit_array  = []
    lcon_array  = []
    has_java_file = False

    for row in spamreader:
      loc = row[34]
      cbo = row[3]
      dit = row[8]
      lcon = row[11]

      loc_total += int(loc)
      cbo_array.append(int(cbo))
      dit_array.append(int(dit))
      lcon_array.append(int(lcon))
      has_java_file = True
  if not has_java_file:
    return RepositoryCkData(0, 0, 0, 0)
  cbo_final = np.median(cbo_array)
  dit_final = np.amax(dit_array)
  lcon_final = np.median(lcon_array)
  return RepositoryCkData(loc_total, cbo_final, dit_final, lcon_final)

def save_ck_data_to_file(repo_metrics: RepositoryMetrics):
  with open("result.csv", "a+", newline='') as csvfile:
    writer = csv.writer(csvfile)
    row = [repo_metrics.name, repo_metrics.repo_clone_url, repo_metrics.age, repo_metrics.releases_number, repo_metrics.loc, repo_metrics.cbo, repo_metrics.dit, repo_metrics.lcon]
    writer.writerow(row)

def calculate_repository_age(created_at):
  today = date.today()
  created_at = created_at.split("T", 1)
  datetime_object = datetime.strptime(created_at[0], '%Y-%m-%d').date()
  delta = today - datetime_object
  return delta.days/360

def remove_readonly(func, path, excinfo):
    path = r"{}".format(path)
    os.chmod(path, stat.S_IWRITE)
    func(path)

def save_data_to_file(data):
    # open the file in the write mode
    f = open('repositories.csv', 'a', newline='')
    writer = csv.writer(f)
    for repository in data:
        row = []
        row.append(repository['node']['name'])
        row.append(repository['node']['url'])
        age = calculate_repository_age(repository['node']['createdAt'])
        age = math.modf(age)
        age = age[1]
        row.append(age)
        row.append(repository['node']['releases']['totalCount'])
        writer.writerow(row)
    f.close()

# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query):
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.
query = """
{
  search(query: "is:public stars:>100 sort:stars-desc language:java", type: REPOSITORY, first: 10, after:null) {
    repositoryCount
    pageInfo {
      endCursor
      startCursor
    }
    edges {
      node {
        ... on Repository {
          name
          url
          createdAt
          releases {
            totalCount
          }
        }
      }
    }
  }
}
"""

header = ['name', 'repo_clone_url', 'age', 'releases_number']

f = open('repositories.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(header)
f.close()

query_result = run_query(query)  # Execute the query

save_data_to_file(query_result['data']['search']['edges'])
end_cursor = '"' + \
    query_result['data']['search']['pageInfo']['endCursor'] + '"'
query = query.replace('null', end_cursor)
old_end_cursor = end_cursor

for x in range(1, 100):
    query_result = run_query(query)
    save_data_to_file(query_result['data']['search']['edges'])
    new_end_cursor = '"' + \
        query_result['data']['search']['pageInfo']['endCursor'] + '"'
    query = query.replace(old_end_cursor, new_end_cursor)
    old_end_cursor = new_end_cursor

# Create result file
header = ['name', 'repo_clone_url', 'age', 'releases_number', 'size', 'CBO', 'DIT', 'LCOM']
f = open('result.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(header)
f.close()

today = date.today()
with open('repositories.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(spamreader)
  for row in spamreader:
    name = row[0].split(',')[0]
    repo_clone_url = row[0].split(',')[1]
    age = row[0].split(',')[2]
    releases_number = row[0].split(',')[3]
    # Repo.clone_from(repo_clone_url, "./repository")
    Repo.clone_from(repo_clone_url, "./repository")
    # Run CK
    subprocess.call(['java', '-jar', 'ck-ck-0.7.0/target/ck-0.7.0-jar-with-dependencies.jar', './repository'])
    repo_ck_metrics = get_repository_ck_data()
    if repo_ck_metrics.loc == 0:
      # Remove repository folder  
      shutil.rmtree(r'repository', onerror=remove_readonly)
      continue
    repo_metrcis = RepositoryMetrics(name, repo_clone_url, age, releases_number, repo_ck_metrics.loc, repo_ck_metrics.cbo, repo_ck_metrics.dit, repo_ck_metrics.lcon)
    save_ck_data_to_file(repo_metrcis)
    # Remove repository folder  
    shutil.rmtree(r'repository', onerror=remove_readonly)


