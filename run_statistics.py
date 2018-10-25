import pandas as pd
import matplotlib.pyplot as plt

xi = [i for i in range(2, 7)]
yi = [i for i in range(0, 12000, 2000)]
plt.xticks(xi)
plt.yticks(yi)
for category in ['marvel', 'hotel', 'cell']:
    path = 'generated_datasets/{}_5_{}_10000.csv'.format(category, '{}')
    plt.plot(xi, [df['text'].nunique() for df in [pd.read_csv(path.format(i)) for i in xi]], label=category)
plt.legend(loc='lower left')
plt.xlabel('state size')
plt.ylabel('unique sentences')
plt.title('Rating 5 models: unique sentences / 10000 generated')
plt.grid(True)
plt.show()
