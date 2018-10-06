# Installation

### Ubuntu
* ```curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash```
* ```sudo apt-get install git-lfs```
* ```git clone git@github.com:thalvari/SpamReviewGenerator.git```
* ```cd SpamReviewGenerator```
* ```python3 -m venv venv```
* ```source venv/bin/activate```
* ```python -m pip install -U pip setuptools```
* ```pip install -r requirements.txt```
* ```python -m spacy download en```

### Windows
* Install Python 3.6.6 (SpaCy has problems with 3.7.0) and Git
* Download 'Build Tools for Visual Studio 2017' and install 'VC++ 2015.3 v14.00 (v140) toolset for desktop'
* Run the following as administrator:
* ```git clone git@github.com:thalvari/SpamReviewGenerator.git```
* ```cd SpamReviewGenerator```
* ```python -m venv venv```
* ```source venv/Scripts/activate```
* ```python -m pip install -U pip setuptools```
* ```pip install -r requirements.txt```
* ```python -m spacy download en```
