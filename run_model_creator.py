import click

from model_creator import Dataset, Preprocessor


@click.command()
@click.argument('path_to_dataset', type=click.Path(exists=True))
@click.option('--rating', '-r', prompt='Rating', type=click.IntRange(1, 5), help='Rating of the reviews used.')
@click.option('--state_size', '-s', prompt='States', type=click.IntRange(2, 12), help='Markov chain state size.')
def main(path_to_dataset, rating, state_size):
    try:
        preprocessor = Preprocessor(Dataset(path_to_dataset), rating, state_size)
    except ValueError:
        print('Dataset not supported.')
        exit()
    preprocessor.load_and_normalize_dataset()
    preprocessor.create_model()
    preprocessor.write_model_to_file()


if __name__ == '__main__':
    main()
