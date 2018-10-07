import click

from app.generator import ExportedModel, Generator


@click.command()
@click.option('--review_class', '-c', prompt='Review class', type=click.Choice(['hotel', 'predator', 'cell']),
              help='Class of the reviews generated.')
@click.option('--rating', '-r', prompt='Rating', type=click.IntRange(1, 5), help='Rating of the reviews generated.')
@click.option('--state_size', '-s', prompt='States', type=click.IntRange(2, 12), help='Markov chain state size.')
@click.option('--n_reviews', '-n', prompt='How many', type=click.IntRange(1, 100),
              help='Number of the reviews generated.')
def main(review_class, rating, state_size, n_reviews):
    path_to_exported_model = 'models/{}_{}_{}.json'.format(review_class, '{}', '{}')
    generator = Generator()
    try:
        generator.load_model(ExportedModel(path_to_exported_model), rating, state_size)
    except FileNotFoundError:
        print('Model not supported.')
        exit()
    print('{}'.format('\n'.join([generator.generate_review() for _ in range(n_reviews)])))


if __name__ == '__main__':
    main()
