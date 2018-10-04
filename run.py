from app.generator import Dataset, Generator

generator = Generator()
while True:
    print('---------------------\nSpam review generator\n---------------------')
    print('\n'.join(['{}. {}'.format(dataset.index, dataset.name) for dataset in Dataset]))
    print('0. Exit\n')
    number = int(input('Enter a number: '))
    assert number in range(0, len(Dataset) + 1)
    if number == 0:
        exit()
    generator.load_dataset(Dataset(number))
    rating = int(input('What rating? (1 - 5): '))
    assert rating in range(1, 6)
    n_reviews = int(input('How many?: '))
    assert n_reviews > 0
    print('\n{}\n'.format('\n'.join([generator.generate_review(rating) for i in range(0, n_reviews)])))
