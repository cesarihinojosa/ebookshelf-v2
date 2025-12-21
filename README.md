# EbookShelf v2

EbookShelf v2 is a web application for managing and browsing your ebook collection. It features a simple web interface and integrates with Goodreads for enhanced book metadata.

## Features
- Browse and search your ebook collection via a web interface
- Integration with Goodreads for book information
- Static assets served from the `static/` directory

## Project Structure
```
app.py                # Main FastAPI application
goodreads_adapter.py  # Goodreads API integration
requirements.txt      # Python dependencies
static/
  index.html          # Main HTML page
  images/             # Static images
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd ebookshelf-v2
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```
2. Open your browser and go to `http://localhost:8000`.

## API Endpoints

- `/` : Serves the main web interface (`static/index.html`)
- `/ebooks` : Returns a list of ebooks in JSON format
- `/goodreads/{book_id}` : Fetches Goodreads metadata for a book

## Usage
- Access the web interface to browse your ebooks.
- Use the Goodreads integration to fetch additional book details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.
