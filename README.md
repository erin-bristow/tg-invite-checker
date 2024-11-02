# Telegram Invite Checker

Check Telegram channel invite links to see if they're alive, and return channel title, description, and number of subscribers. Removes duplicate channels by default (if the channel title and description are the same as another channel, it isn't included in the final results set).

## Requirements

Before running this project, make sure you have the following installed:
- Python 3.12
- [Poetry](https://python-poetry.org/) for dependency management

## Dependencies
Use poetry to install dependences:   

`poetry install`

## Usage
Run with an input file containing Telegram invite links (each link should be separated by a newline):  

`poetry run checker -f outputfile.txt`

Run for a single invite link:  

`poetry run checker -l https://t.me/+086P3jaraClmYjRi`

Example output:  

`('PureLife Essentials', '4 041 subscribers', 'Discover a life of vitality and well-being with PureLife Essential, your trusted partner in holistic health. At PureLife Essentia, we are committed to providing a range of premium Healthy Life Products that empower you to thrive.', 'https://t.me/+vLb2sP9aEak0MWE1')`
