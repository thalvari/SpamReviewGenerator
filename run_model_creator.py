import click

from model_creator import Dataset, ModelCreator


@click.command()
@click.argument('path_to_dataset', type=click.Path(exists=True))
@click.option('--rating', '-r', prompt='Rating (1-5)', type=click.IntRange(1, 5), help='Rating of the reviews used.')
@click.option('--state_size', '-s', prompt='State size (2-8)', type=click.IntRange(2, 8),
              help='Markov model state size.')
def main(path_to_dataset, rating, state_size):
    try:
        preprocessor = ModelCreator(Dataset(path_to_dataset), rating, state_size)
    except ValueError:
        print('Dataset not supported.')
        exit()
    preprocessor.load_and_normalize_dataset()
    preprocessor.create_model()
    preprocessor.write_model_to_file()


if __name__ == '__main__':
    main()
