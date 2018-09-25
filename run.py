import pandas as pd

df = pd.read_csv('data/7282_with_textcat_languagetags.csv', index_col=0)
df.columns = df.columns.str.replace('.', "_")
df = df.query('language_textcat == ["english", "scots"]')
print('\n'.join('{}: {}'.format(i, df.query('reviews_rating == {}'.format(i)).shape[0]) for i in range(1, 6)))
