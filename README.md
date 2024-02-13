# Readme under construction...


## Brodelo App

The inspiration for this project is based on the idea of my buddies and I meeting up at our local breweries and connecting, having a good time, venting, and creating a brotherhood. The name "Brodelo" is also a spin on the infamous mexican Pilsner-style Lager, emphasizing the importance of male bonding.

### Features

#### BREWERY FUNCTIONALITY
- Ability to ingest data from Open DB Brewery API
- Can add, edit, remove breweries
#### USER FUNCTIONALITY
- Can create, edit, and remove users
- OAuth2 authentication
- Add and Remove from favorites
#### FOLIUM MAP
- Map of USA with pins indicating brewery location
Detailed info including address, website, phone #, and brewery type
- Pinpointed using latitude and longitude coordinates


### Prerequisites
- Python 3.11.4 installed

### Installation
1. Clone the repository

```commandline
git clone https://github.com/markprubin/web-mapping
cd web-mapping
```
2. Set up a virtual environment (optional, but recommended):
```commandline
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```
3. Install the dependencies:
```commandline
pip install -r requirements.txt

```

### Usage

python -m scripts.map_script to run the script and generate the html file.

### Dependencies

