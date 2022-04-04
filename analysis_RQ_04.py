import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('result.csv')

df = df.dropna().sort_values(by=['size'], ascending=False)

fig, ax = plt.subplots()
ax.scatter(df['CBO'], df['size'])
ax.set(
    xlabel='CBO',
    ylabel='size'
)
plt.savefig(f'charts/REQ04-CBO.png', dpi=300, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots()
ax.scatter(df['DIT'], df['size'])
ax.set(
    xlabel='DIT',
    ylabel='size'
)
plt.savefig(f'charts/REQ04-DIT.png', dpi=300, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots()
ax.scatter(df['LCOM'], df['size'])
ax.set(
    xlabel='LCOM',
    ylabel='size'
)
plt.savefig(f'charts/REQ04-LCOM.png', dpi=300, bbox_inches='tight')
plt.close()
