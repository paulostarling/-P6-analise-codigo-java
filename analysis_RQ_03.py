from hashlib import new
import matplotlib.pyplot as plt
import pandas as pd

# RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade? 
df = pd.read_csv('result.csv')
df = df.dropna().sort_values(by=['releases_number'], ascending=False)
fig, ax = plt.subplots()
ax.scatter(df['releases_number'], df['CBO'])
ax.set(
    xlabel='Releases',
    ylabel='CBO'
)
plt.savefig(f'charts/REQ03-CBO.png', dpi=300, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots()
ax.scatter(df['releases_number'], df['DIT'])
ax.set(
    xlabel='Releases',
    ylabel='DIT'
)
plt.savefig(f'charts/REQ03-DIT.png', dpi=300, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots()
ax.scatter(df['releases_number'], df['LCOM'])
ax.set(
    xlabel='Releases',
    ylabel='LCOM'
)
plt.savefig(f'charts/REQ03-LCOM.png', dpi=300, bbox_inches='tight')
plt.close()



  