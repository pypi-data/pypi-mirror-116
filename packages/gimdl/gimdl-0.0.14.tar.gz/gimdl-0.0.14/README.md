# Google Image Search & Download using the API

This will fetch images using the google API and save to an 'images' subdirectory from where you run your code. You just specify the search term. eg. "cat" or "dog"

## Installation

Run the following to install:

```python
pip install gimdl
```

## Usage

```python
import gimdl
from gimdl import fetch_images

# specify what images you want to fetch
fetch_images("cat")
```
| Requirement | URL |
| ----------- | ----------- |
| pip install Google-Images-Search | https://pypi.org/project/Google-Images-Search/ |
| Google API Key | https://console.developers.google.com |
| pip install python-dotenv | https://pypi.org/project/python-dotenv/ |
| pip install windows-curses (Windows only)  | https://pypi.org/project/windows-curses/ |


