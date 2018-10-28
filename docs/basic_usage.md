# Basic usage
Create and export Markov chain models with ```python run_model_creator.py```.
```
Usage: run_model_creator.py [OPTIONS]

Options:
  -c, --category [marvel|hotel|cell]
                                  Dataset category.
  -r, --rating INTEGER RANGE      Rating of the reviews used (1-5).
  -s, --state_size INTEGER RANGE  Markov model state size (2-6).
  -n, --n_sample INTEGER RANGE    Only write a sample of n original sentences
                                  with the given rating to a file (1-100000).
  --help                          Show this message and exit.
```
Print generated sentences from premade models with ```python run_generator.py```.
```
Usage: run_generator.py [OPTIONS]

Options:
  -c, --category [marvel|hotel|cell]
                                  Category of the generated reviews.
  -r, --rating INTEGER RANGE      Rating of the generated reviews (1-5).
  -s, --state_size INTEGER RANGE  Markov model state size (2-6). Default is 4.
  -o, --output_type [csv|txt]     Instead write the sentences (csv) or a whole
                                  review (txt) to a file of given type.
  --help                          Show this message and exit.
```
