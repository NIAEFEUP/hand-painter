## Setup

Create a virtual environment and install the dependencies:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```
<br>

## To run without the "Tirar foto" button:

```python
python3 main.py --no-photo
```
<br>

## To run with **full functionality**:

Setup email environment variables in the .env file
```
EMAIL=custom_email@example.com
PASSWORD=very_secure_password
```

Run the application

```python
python3 main.py
```
