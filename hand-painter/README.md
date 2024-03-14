## Setup

Create a virtual environment and install the dependencies:

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```
<br>

## To run without the "Tirar foto" button:
This is useful when running without email environment variables setup.

```bash
python3 main.py --no-photo  # inside the src/ directory
```
<br>

## To run with **full functionality**:

Setup email environment variables in the .env file
```
MJ_APIKEY_PUBLIC=
MJ_APIKEY_PRIVATE=
```

Run the application

```bash
python3 main.py     # inside the src/ directory
```
