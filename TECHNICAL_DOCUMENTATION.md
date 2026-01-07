# CSV Inspector - Technical Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Frontend Architecture](#frontend-architecture)
3. [Backend Architecture](#backend-architecture)
4. [Database Design](#database-design)
5. [Key Features Implementation](#key-features-implementation)
6. [Code Structure](#code-structure)
7. [Future Improvements](#future-improvements)
8. [Performance Considerations](#performance-considerations)
9. [Security Considerations](#security-considerations)

## Architecture Overview

### **Technology Stack**
- **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript (ES6+)
- **Backend**: Python 3.12+, Flask
- **Database**: SQLite3
- **Data Processing**: Pandas
- **UI Components**: Tabulator.js for tables, Bootstrap for layout

### **Application Flow**
```
User Interface (HTML/JS) → Flask Backend → SQLite Database
        ↓                    ↓              ↓
    Browser Events → API Endpoints → Data Operations
        ↓                    ↓              ↓
    Dynamic Updates → JSON Responses → Persistent Storage
```

## Frontend Architecture

### **HTML Structure**
- **Single Page Application**: All functionality in `index.html`
- **Bootstrap Components**: Cards, modals, forms, alerts
- **Responsive Design**: Mobile-first approach

### **JavaScript Architecture**

#### **Global State Management**
```javascript
let table;           // Tabulator instance
let currentData = []; // Current dataset
let originalFileName = ''; // Original CSV filename
let currentColumns = []; // Column definitions
let isCardView = false; // View mode flag
```

#### **Event-Driven Architecture**
- **Initialization**: `DOMContentLoaded` → `initializeEventListeners()`
- **File Operations**: Upload, download, save, load
- **Data Operations**: Edit, add, delete, search, filter
- **View Management**: Toggle between table and card views

#### **Key Functions**

**Data Management:**
- `displayTable()`: Initializes Tabulator and stores data
- `handleFileSelect()`: Processes CSV upload
- `downloadCSV()`: Exports data as CSV
- `saveData()`: Persists to database
- `loadSavedData()`: Retrieves from database

**View Management:**
- `toggleView()`: Switches between table/card views
- `renderCardView()`: Creates card layout
- `createDataCard()`: Generates individual data cards
- `updateDataField()`: Handles inline editing

**Search & Filter:**
- `handleGlobalSearch()`: Filters across all columns
- `resetFilters()`: Clears all filters

**Autocomplete:**
- `showFieldSuggestions()`: Dynamic suggestions based on existing data

### **CSS Architecture**

#### **Component-Based Styling**
```css
/* Layout Components */
.container-fluid, .row, .col-md-6

/* Interactive Elements */
.drop-zone, .data-card, .suggestions-dropdown

/* State Classes */
.dragover, .d-none, .loading
```

#### **Responsive Design**
- **Mobile**: Stacked cards, full-width tables
- **Tablet**: Two-column layout, optimized spacing
- **Desktop**: Maximum utilization of screen space

## Backend Architecture

### **Flask Application Structure**

#### **Application Setup**
```python
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
```

#### **Database Configuration**
```python
DATABASE = 'csv_inspector.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Creates saved_data table if not exists
```

### **API Endpoints**

#### **File Operations**
- `POST /upload`: Process CSV files
- `POST /download`: Export data as CSV

#### **Database Operations**
- `POST /save`: Store data with metadata
- `GET /load/<id>`: Retrieve specific saved dataset
- `GET /saved`: List all saved datasets
- `DELETE /delete/<id>`: Remove saved dataset

#### **Static Routes**
- `GET /`: Serve main application

### **Data Processing Pipeline**

#### **CSV Upload Flow**
```
File Upload → Pandas Read → JSON Conversion → Frontend Display
     ↓              ↓              ↓              ↓
  Validation    Data Cleaning   Column Detection   Table Init
```

#### **Database Storage Flow**
```
Frontend Request → JSON Serialization → SQLite Storage
       ↓                 ↓                  ↓
   Validation        Data Preparation    Metadata Storage
```

## Database Design

### **Schema**
```sql
CREATE TABLE saved_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    data TEXT NOT NULL,        -- JSON array of data rows
    columns TEXT NOT NULL,      -- JSON array of column definitions
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Design Decisions**
- **JSON Storage**: Flexible schema for varying CSV structures
- **SQLite**: Lightweight, file-based, no external dependencies
- **Row Factory**: Enables dictionary-like access to rows
- **Auto-increment ID**: Simple primary key generation

### **Data Flow**
```
CSV File → Pandas DataFrame → JSON Array → SQLite TEXT
    ↓            ↓                ↓              ↓
  Parse      Clean Data      Serialize      Store
```

## Key Features Implementation

### **1. Dual View System**

#### **Table View (Tabulator)**
```javascript
table = new Tabulator("#csvTable", {
    data: data,
    columns: columns,
    layout: "fitColumns",
    responsiveLayout: "hide",
    addRowPos: "top",
    history: true
});
```

#### **Card View (Custom)**
```javascript
function createDataCard(data, rowId) {
    // Dynamic card creation with inline editing
    // Field suggestions integration
    // CRUD operations
}
```

#### **View Synchronization**
- **Single Source of Truth**: `currentData` array
- **Consistent Updates**: Both views update from same data
- **State Management**: `isCardView` flag tracks current mode

### **2. Real-time Search**

#### **Global Search Implementation**
```javascript
function handleGlobalSearch() {
    const searchTerm = globalSearch.value.toLowerCase();
    const filteredData = currentData.filter(row => {
        return Object.values(row).some(value => 
            value && value.toString().toLowerCase().includes(searchTerm)
        );
    });
    updateBothViews(filteredData);
}
```

#### **Search Features**
- **Multi-column**: Searches across all fields
- **Case-insensitive**: Normalized search terms
- **Real-time**: Updates as user types
- **View-agnostic**: Works in both table and card views

### **3. Inline Autocomplete**

#### **Suggestion Generation**
```javascript
function showFieldSuggestions(input, field, currentValue) {
    const values = currentData
        .map(row => row[field])
        .filter(val => val !== null && val !== undefined && val.toString().trim() !== '');
    
    const frequency = {};
    values.forEach(val => {
        const key = val.toString().toLowerCase();
        frequency[key] = (frequency[key] || 0) + 1;
    });
    
    const matchingSuggestions = Object.keys(frequency)
        .filter(val => val.includes(currentValue.toLowerCase()))
        .sort((a, b) => frequency[b] - frequency[a])
        .slice(0, 5);
}
```

#### **Features**
- **Frequency-based**: Most common values first
- **Type-ahead**: Shows matching suggestions as user types
- **Context-aware**: Different suggestions per field
- **Non-intrusive**: Easy to dismiss with Tab/Escape

### **4. Data Persistence**

#### **Save Operation**
```javascript
const dataToSave = {
    name: name,
    description: description,
    data: currentData,
    columns: currentColumns
};
```

#### **Load Operation**
```javascript
function loadSavedData(saveId) {
    fetch(`/load/${saveId}`)
        .then(response => response.json())
        .then(result => {
            displayTable(result.data, result.columns, result.name);
        });
}
```

## Code Structure

### **File Organization**
```
csv-inspector/
├── app.py                 # Flask backend (200+ lines)
├── templates/
│   └── index.html        # Frontend (1100+ lines)
├── pyproject.toml          # Dependencies
├── README.md              # User documentation
├── GIT_SETUP.md           # Setup guide
└── .gitignore             # Git exclusions
```

### **Frontend Code Organization**
```javascript
// 1. Global Variables (lines 346-351)
// 2. Event Listeners (lines 407-443)
// 3. File Operations (lines 453-500)
// 4. View Management (lines 502-580)
// 5. Data Operations (lines 582-700)
// 6. Database Operations (lines 702-850)
// 7. Utility Functions (lines 852-950)
```

### **Backend Code Organization**
```python
# 1. Imports and Configuration (lines 1-46)
# 2. Database Setup (lines 18-40)
# 3. File Upload Handler (lines 48-80)
# 4. Database Operations (lines 81-157)
# 5. Download Handler (lines 158-180)
# 6. Application Entry (lines 182-184)
```

## Future Improvements

### **1. Performance Optimizations**

#### **Frontend**
- **Virtual Scrolling**: Handle large datasets (>10,000 rows)
- **Lazy Loading**: Load data in chunks
- **Debounced Search**: Reduce search API calls
- **Web Workers**: Offload data processing

#### **Backend**
- **Database Indexing**: Improve query performance
- **Caching**: Redis for frequently accessed data
- **Pagination**: Server-side data pagination
- **Compression**: Gzip responses

### **2. Enhanced Features**

#### **Data Visualization**
- **Charts**: Bar, line, pie charts from CSV data
- **Statistics**: Summary statistics dashboard
- **Data Profiling**: Column type detection, distributions

#### **Advanced Editing**
- **Bulk Operations**: Multi-row edit, delete
- **Formula Support**: Excel-like formulas
- **Validation Rules**: Custom field validation
- **Undo/Redo**: Comprehensive history tracking

#### **Import/Export**
- **Multiple Formats**: Excel, JSON, XML
- **API Integration**: Import from external APIs
- **Scheduled Imports**: Automated data updates

### **3. User Experience**

#### **Responsive Design**
- **Mobile Optimization**: Touch-friendly interface
- **Progressive Web App**: Offline functionality
- **Dark Mode**: Theme switching
- **Accessibility**: WCAG 2.1 compliance

#### **Collaboration**
- **Multi-user**: Real-time collaboration
- **Comments**: Cell-level annotations
- **Version Control**: Data versioning
- **Permissions**: Role-based access

### **4. Architecture Improvements**

#### **Frontend**
- **Component Framework**: React/Vue for better state management
- **TypeScript**: Type safety and better IDE support
- **Testing**: Unit tests, integration tests
- **Build Pipeline**: Webpack/Vite for optimization

#### **Backend**
- **RESTful API**: Better API design
- **Authentication**: User accounts and sessions
- **Microservices**: Separate services for different features
- **Containerization**: Docker deployment

### **5. Security Enhancements**

#### **Data Protection**
- **Encryption**: Encrypt sensitive data at rest
- **Input Validation**: Comprehensive input sanitization
- **CSRF Protection**: Cross-site request forgery prevention
- **Rate Limiting**: Prevent abuse

#### **Access Control**
- **User Authentication**: Login/logout functionality
- **Authorization**: Permission-based access
- **Audit Logging**: Track all data changes
- **Data Retention**: Automatic cleanup policies

## Performance Considerations

### **Current Limitations**
- **Memory Usage**: Entire dataset loaded in browser memory
- **Search Performance**: O(n*m) complexity (n rows × m columns)
- **Database Size**: No data cleanup mechanism
- **Concurrent Users**: No user isolation

### **Optimization Strategies**
- **Pagination**: Load data in chunks
- **Indexing**: Database indexes for faster queries
- **Caching**: Browser and server-side caching
- **Compression**: Reduce data transfer size

## Security Considerations

### **Current Security Measures**
- **File Upload Limits**: 16MB maximum
- **File Type Validation**: CSV only
- **Input Sanitization**: Basic validation
- **SQL Injection Prevention**: Parameterized queries

### **Security Gaps**
- **No Authentication**: Open access to all data
- **No Authorization**: No permission system
- **Data Exposure**: All data visible to all users
- **No Audit Trail**: No change tracking

### **Recommended Security Improvements**
- **User Accounts**: Authentication system
- **Role-Based Access**: Different permission levels
- **Data Encryption**: Sensitive field encryption
- **Audit Logging**: Comprehensive change tracking

This documentation provides a complete understanding of the CSV Inspector application's architecture, implementation details, and potential areas for future enhancement.
