# Basic usage
Create and export Markov chain models with ```model_creator```.
```
Usage: run_model_creator.py [OPTIONS] PATH_TO_DATASET

Options:
  -r, --rating INTEGER RANGE      Rating of the reviews used.
  -s, --state_size INTEGER RANGE  Markov chain state size.
  --help                          Show this message and exit.
```
Then generate reviews from exported models with ```generator```.
```
Usage: run_cli.py [OPTIONS]

Options:
  -c, --review_class [hotel|predator|cell]
                                  Class of the reviews generated.
  -r, --rating INTEGER RANGE      Rating of the reviews generated.
  -s, --state_size INTEGER RANGE  Markov chain state size.
  -n, --n_reviews INTEGER RANGE   Number of the reviews generated.
  --help                          Show this message and exit.
```