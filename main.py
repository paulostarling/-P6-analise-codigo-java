import math
import requests
import csv
import numpy as np
from git import Repo
from datetime import date
from datetime import datetime
import subprocess

api_token = 'place_the_token_here'

headers = {'Authorization': 'token %s' % api_token}

def calculate_repository_age(created_at):
  today = date.today()
  created_at = created_at.split("T", 1)
  datetime_object = datetime.strptime(created_at[0], '%Y-%m-%d').date()
  delta = today - datetime_object
  return delta.days/360


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

today = date.today()
with open('repositories.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(spamreader)
  for row in spamreader:
    name = row[0].split(',')[0]
    repo_clone_url = row[0].split(',')[1]
    age = row[0].split(',')[2]
    releases_number = row[0].split(',')[3]
    break

# Repo.clone_from(repo_clone_url, "./repository")
Repo.clone_from(repo_clone_url, "./repository")

# Run CK
subprocess.call(['java', '-jar', 'ck-ck-0.7.0/target/ck-0.7.0-jar-with-dependencies.jar', './repository'])

# Get repository CK metrics
with open('class.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  next(spamreader)
  loc_total = 0
  cbo_total  = 0
  dit_total  = 0
  lcon_total  = 0
  for row in spamreader:
    loc = row[0].split(',')[34]
    cbo = row[0].split(',')[3]
    dit = row[0].split(',')[8]
    lcon = row[0].split(',')[11]

    loc_total += int(loc) 
    cbo_total += int(cbo) 
    dit_total += int(dit) 
    lcon_total += int(lcon)


header = ['name', 'repo_clone_url', 'age', 'releases_number', 'size', 'CBO', 'DIT', 'LCOM']
row = [name, repo_clone_url, age, releases_number, loc_total, cbo_total, dit_total, lcon_total]
f = open('result.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(header)
writer.writerow(row)
f.close()

