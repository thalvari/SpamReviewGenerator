# Basic usage
Create and export Markov chain models with ```model_creator```.
```
Usage: run_model_creator.py [OPTIONS] PATH_TO_DATASET

Options:
  --rating INTEGER RANGE      Rating of the reviews used.
  --state_size INTEGER RANGE  Markov chain state size.
  --help                      Show this message and exit.
```
Then generate reviews from exported models with ```generator```.
```
Usage: run_cli.py [OPTIONS]

Options:
  --review_class [hotel|predator|cell]
                                  Class of the reviews generated.
  --rating INTEGER RANGE          Rating of the reviews generated.
  --state_size INTEGER RANGE      Markov chain state size.
  --n_reviews INTEGER RANGE       Number of the reviews generated.
  --help                          Show this message and exit.
```