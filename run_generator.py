import click

from generator import Generator


@click.command()
@click.option('--category', '-c', prompt='Category', type=click.Choice(['hotel', 'predator', 'cell']),
              help='Category of the generated reviews.')
@click.option('--rating', '-r', prompt='Rating (1-5)', type=click.IntRange(1, 5),
              help='Rating of the generated reviews.')
@click.option('--state_size', '-s', type=click.IntRange(2, 8), help='Markov model state size.', default=4)
@click.option('--output_type', '-o', type=click.Choice(['csv', 'txt']), help='Output file type.')
@click.option('--debug/--no-debug', default=False, help='Debug mode.')
def main(category, rating, state_size, output_type, debug):
    generator = Generator(category, rating, state_size, output_type, debug)
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
