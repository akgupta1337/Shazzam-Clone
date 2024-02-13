# Shazzam Clone

## Description
Shazzam Clone is a Python project that implements audio fingerprinting using the Shazam algorithm. It allows for the identification of songs by analyzing audio features and comparing audio signatures.

## Features
- Audio fingerprinting using the Shazam algorithm.
- Extracting audio features and generating hashes for comparison.
- Comparing audio signatures to identify songs.

## Requirements
- Python 3.x
- NumPy
- PyDub
- Matplotlib
- SciPy

## Usage
1. Clone the repository.
2. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the example.py script to perform audio fingerprinting and song identification:
    ```bash
    python EXAMPLE.py
    ```

## Project Structure
- **logic**: Contains the Shazzam class for audio fingerprinting.
- **database**: Stores fingerprints in pkl format after the process.
- **mp3**: Put all your songs which you want to add in database here.
- **test**: Put the songs you want to match here.

## License
This project is licensed under the [Apache-2.0 license](LICENSE).

## Author
Akhil Gupta

## Acknowledgements
- This project is inspired by the Shazam algorithm for audio fingerprinting.
- A heartfelt thank you to the developers of Dejavu for their groundbreaking work on the audio fingerprinting logic.
- Deep appreciation goes to the developers of NumPy, PyDub, Matplotlib, and SciPy libraries for their invaluable contributions.
