import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('result.csv')

df = df.dropna().sort_values(by=['stargazers'], ascending=False)

fig, ax = plt.subplots()
ax.scatter(df['CBO'], df['stargazers'])
ax.set(
    xlabel='CBO',
    ylabel='stargazers'
)
plt.savefig(f'charts/REQ01-CBO.png', dpi=300, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots()
ax.scatter(df['DIT'], df['stargazers'])
ax.set(
    xlabel='DIT',
    ylabel='stargazers'
)
plt.savefig(f'charts/REQ01-DIT.png', dpi=300, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots()
ax.scatter(df['LCOM'], df['stargazers'])
ax.set(
    xlabel='LCOM',
    ylabel='stargazers'
)
plt.savefig(f'charts/REQ01-LCOM.png', dpi=300, bbox_inches='tight')
plt.close()
