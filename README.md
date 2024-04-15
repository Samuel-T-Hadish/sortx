# sortX

sortX is a DASH Python application that allows users to upload an Excel file containing document numbers and then crawls through a specified directory to find matching folders. The application then updates the DataFrame with the status, file path, and processed date for each document number.

## Project Structure
The project has the following structure:

- **app.py**: The main entry point for the application.
- **src/**: Contains the source code for the application.
- **components/**: Contains the components of the application, such as the upload and download components.
- **data/**: Contains the FileCrawler class, which is responsible for crawling the file system.