import click

from generator import Generator


@click.command()
@click.option('--review_type', '-t', prompt='Review type', type=click.Choice(['hotel', 'predator', 'cell']),
              help='Type of the reviews generated.')
@click.option('--rating', '-r', prompt='Rating', type=click.IntRange(1, 5), help='Rating of the reviews generated.')
@click.option('--state_size', '-s', prompt='States', type=click.IntRange(2, 12), help='Markov chain state size.')
@click.option('--n_reviews', '-n', prompt='How many', type=click.IntRange(1, 100000),
              help='Number of the reviews generated.')
@click.option('--output_format', '-o', type=click.Choice(['csv', 'txt']), help='Generates a dataset of given format.')
def main(review_type, rating, state_size, n_reviews, output_format):
    generator = Generator(review_type, rating, state_size, n_reviews, output_format)
    try:
        generator.load_model()
    except FileNotFoundError:
        print('Model not supported.')
        exit()
    generator.generate_output()


if __name__ == '__main__':
    main()
