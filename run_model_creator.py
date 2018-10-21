import click

from model_creator import ModelCreator


@click.command()
@click.option('--category', '-c', prompt='Category', type=click.Choice(['marvel', 'hotel', 'cell']),
              help='Dataset category.')
@click.option('--rating', '-r', prompt='Rating (1-5)', type=click.IntRange(1, 5), help='Rating of the reviews used.')
@click.option('--state_size', '-s', prompt='State size (2-8)', type=click.IntRange(2, 8),
              help='Markov model state size.')
@click.option('--n_sample', '-n', type=click.IntRange(1, 100000),
              help='Only write a sample of original review sentences to a file.')
def main(category, rating, state_size, n_sample):
    try:
        model_creator = ModelCreator(category, rating, state_size)
    except ValueError:
        print('Dataset not supported.')
        exit()
    model_creator.load_and_normalize_dataset()
    model_creator.preprocess_dataset()
    if n_sample:
        model_creator.write_sample_to_file(n_sample)
    else:
        model_creator.create_model()
        model_creator.write_model_to_file()


if __name__ == '__main__':
    main()
