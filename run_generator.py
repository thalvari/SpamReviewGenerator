import click

from generator import Generator


@click.command()
@click.option('--category', '-c', prompt='Category', type=click.Choice(['marvel', 'hotel', 'cell']),
              help='Category of the generated reviews.')
@click.option('--rating', '-r', prompt='Rating (1-5)', type=click.IntRange(1, 5),
              help='Rating of the generated reviews (1-5).')
@click.option('--state_size', '-s', type=click.IntRange(2, 6), default=4,
              help='Markov model state size (2-6). Default is 4.', )
@click.option('--output_type', '-o', type=click.Choice(['csv', 'txt']),
              help='Instead write the sentences (csv) or a whole review (txt) to a file of given type.')
def main(category, rating, state_size, output_type):
    generator = Generator(category, rating, state_size, output_type)
    try:
        generator.load_model()
    except FileNotFoundError:
        print('Model not supported.')
        exit()
    while True:
        if output_type:
            n_sentences = click.prompt('Number (1-10000)', type=click.IntRange(1, 10000))
            generator.generate_output(n_sentences)
            break
        else:
            n_sentences = click.prompt('Number (1-100)', type=click.IntRange(1, 100))
            generator.generate_output(n_sentences)
            click.confirm('Continue', default=True, abort=True)


if __name__ == '__main__':
    main()
