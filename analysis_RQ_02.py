from hashlib import new
import matplotlib.pyplot as plt
import pandas as pd

# RQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade ? 
df = pd.read_csv('result.csv')
df = df.dropna().sort_values(by=['age'], ascending=False)
fig, ax = plt.subplots()
ax.scatter(df['age'], df['CBO'])
ax.set(
    xlabel='Age',
    ylabel='CBO'
)
plt.savefig(f'charts/REQ02-CBO.png', dpi=300, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots()
ax.scatter(df['age'], df['DIT'])
ax.set(
    xlabel='Age',
    ylabel='DIT'
)
plt.savefig(f'charts/REQ02-DIT.png', dpi=300, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots()
ax.scatter(df['age'], df['LCOM'])
ax.set(
    xlabel='Age',
    ylabel='LCOM'
)
plt.savefig(f'charts/REQ02-LCOM.png', dpi=300, bbox_inches='tight')
plt.close()



# RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?  