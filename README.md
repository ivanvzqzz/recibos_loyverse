# Project Name: Loyverse Receipts Downloader

## Description
This project automates the process of downloading receipts from the Loyverse API and saving them to a `receipts.json` file. The script fetches new receipts, prevents duplicates by adding one second to the latest receipt's timestamp, and appends them to the existing file.

## Features
- Fetch receipts from the Loyverse API.
- Prevent duplicate entries by checking the timestamp of existing receipts.
- Paginated API requests to fetch all available receipts.
- Saves receipts to a `receipts.json` file for future use.

## Prerequisites

Before running the script, you need to have the following installed:
- Python 3.6 or higher
- `pip` (Python's package installer)

## Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/ivanvzqzz/recibos_loyverse.git
    cd recibos_loyverse
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
   - On **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install the dependencies from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set up your `.env` file with your **Loyverse API Access Token**:
    ```bash
    LOYVERSE_ACCESS_TOKEN=<your_access_token_here>
    ```

2. Run the script to fetch receipts:
    ```bash
    python app.py
    ```

This will send an HTTP request to the Loyverse API, retrieve the receipts (up to 50 per request, with pagination), and save them in a file called `receipts.json`. If the file already exists, new receipts will be appended, and duplicates will be avoided by adjusting the timestamp of the last receipt. If you pay for the premium suscription, you can modify the script to download all the receipts.

## requirements.txt

The `requirements.txt` file includes the necessary Python packages for the project:

- `requests` – for making HTTP requests to the API.
- `dotenv` – for loading environment variables from a `.env` file.
- `python-dateutil` – for parsing ISO 8601 timestamps.

## License 

This project is open-source and available under the [MIT license](LICENSE).