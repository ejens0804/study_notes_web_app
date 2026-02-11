# FastAPI Multi-Page Application

## File Structure

```
project/
│
├── app.py                      # Main FastAPI application
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template (inherited by all pages)
│   ├── home.html              # Home page
│   ├── api_demo.html          # API demo page
│   ├── about.html             # About page
│   └── contact.html           # Contact page
│
└── static/                     # Static files
    ├── css/
    │   └── style.css          # Main stylesheet
    │
    └── js/
        ├── main.js            # Main JavaScript
        ├── api.js             # API demo functionality
        └── contact.js         # Contact form functionality
```

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn jinja2 python-multipart
   ```

2. **Create the directory structure:**
   - Create `templates/` folder
   - Create `static/css/` folder
   - Create `static/js/` folder

3. **Add all the files** as shown in the structure above

4. **Run the application:**
   ```bash
   uvicorn app:app --reload
   ```

5. **Open your browser:**
   Navigate to `http://127.0.0.1:8000`

## How It Works

### Templates (Jinja2)
- **base.html**: Contains the common structure (navbar, footer, CSS/JS links)
- **Other templates**: Extend base.html and only define their unique content
- Use `{% extends "base.html" %}` and `{% block content %}...{% endblock %}`

### Static Files
- **CSS**: Styling separated into `static/css/style.css`
- **JS**: JavaScript separated by functionality in `static/js/`
- Referenced using: `{{ url_for('static', path='/css/style.css') }}`

### Routes
- Each page has its own route (/, /api-demo, /about, /contact)
- FastAPI renders the appropriate template for each route
- Templates receive data via the `templates.TemplateResponse()` method

## Benefits of This Structure

✓ **Separation of Concerns**: HTML, CSS, and JS are in separate files
✓ **Reusability**: Base template prevents code duplication
✓ **Maintainability**: Easy to update styles or scripts globally
✓ **Scalability**: Easy to add new pages
✓ **Organization**: Clear file structure for larger projects
