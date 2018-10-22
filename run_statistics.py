import pandas as pd
import matplotlib.pyplot as plt

xi = [i for i in range(2, 7)]
yi = [i for i in range(0, 12000, 2000)]
plt.xticks(xi)
plt.yticks(yi)
marvel_path = 'generated_datasets/marvel_5_{}_10000.csv'
hotel_path = 'generated_datasets/hotel_5_{}_10000.csv'
# cell_path = 'generated_datasets/cell_5_{}_10000.csv'
plt.plot(xi, [df['text'].nunique() for df in [pd.read_csv(marvel_path.format(i)) for i in xi]], label='marvel')
plt.plot(xi, [df['text'].nunique() for df in [pd.read_csv(hotel_path.format(i)) for i in xi]], label='hotel')
# plt.plot(xi, [df['text'].nunique() for df in [pd.read_csv(cell_path.format(i)) for i in xi]], label='cell')
plt.legend(loc='upper right')
plt.xlabel('state size')
plt.ylabel('unique sentences')
plt.title('rating 5 model')
plt.grid(True)
plt.show()
