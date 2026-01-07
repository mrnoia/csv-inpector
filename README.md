# CSV Inspector

A Flask web application for uploading, inspecting, filtering, searching, amending, and downloading CSV files using Bootstrap and Tabulator.

## Features

- **File Upload**: Drag-and-drop or browse to upload CSV files (max 16MB)
- **Data Inspection**: View CSV data in a responsive, interactive table
- **Filtering**: Column-specific filters and global search
- **Editing**: In-place editing of all cells
- **Pagination**: Navigate through large datasets
- **Download**: Export amended data back to CSV format
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Run the application:
```bash
uv run python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Upload a CSV file**: 
   - Drag and drop a CSV file onto the upload area
   - Or click "Browse Files" to select a file

2. **Inspect and Edit Data**:
   - Use column headers to filter data
   - Use the global search bar to search across all columns
   - Click on any cell to edit its content
   - Use Ctrl+Z to undo, Ctrl+Y to redo

3. **Manage Data**:
   - Click "Add Row" to insert new rows
   - Click "Reset Filters" to clear all filters
   - Use pagination controls to navigate large datasets

4. **Download**:
   - Click "Download CSV" to save your changes
   - Click "Clear" to start over with a new file

## Technologies Used

- **Flask**: Python web framework
- **Bootstrap 5**: UI framework
- **Tabulator**: Interactive table library
- **Pandas**: Data manipulation library
- **Bootstrap Icons**: Icon library

## File Structure

```
windsurf/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Main HTML template
├── pyproject.toml        # Project dependencies
└── README.md            # This file
```

## API Endpoints

- `GET /`: Main application page
- `POST /upload`: Upload and parse CSV files
- `POST /download`: Download amended CSV data

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- File size limits
- CSV parsing errors
- Network errors
- Data validation errors