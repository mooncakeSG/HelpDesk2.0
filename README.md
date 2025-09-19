# 🎫 IT Helpdesk 2.0 - Complete Solution

A modern, full-featured IT Helpdesk system built with Flask, SQLiteCloud, and email notifications. Perfect for small to medium teams with enterprise-grade features.

## Features

- **Landing Page**: Role selection for users and agents
- **Ticket Submission**: User-friendly form for submitting support requests
- **Agent Portal**: Complete ticket management interface
- **Real-time Updates**: Live ticket status and notes management
- **Export Functionality**: Export tickets as PDF or CSV
- **Responsive Design**: Works on desktop and mobile devices
- **Cal.com Theme**: Modern, professional styling

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- SQLiteCloud.io account and API credentials

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up SQLiteCloud configuration**:
   - Copy `env_template.txt` to `.env`
   - Get your SQLiteCloud API key and database URL
   - Update the `.env` file with your credentials:
     ```
     SQLITECLOUD_API_KEY=your_actual_api_key
     SQLITECLOUD_URL=https://api.sqlitecloud.io/v1/db/your_db_id/query
     SECRET_KEY=your_secure_secret_key
     ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - The application will be running on all network interfaces

## Usage

### For Users (Ticket Submission)

1. Go to the landing page
2. Click "Submit a Ticket"
3. Fill out the form with:
   - Your full name
   - Email address
   - Detailed description of the issue
4. Click "Submit Ticket"

### For Agents (Ticket Management)

1. Go to the landing page
2. Click "Agent Portal"
3. View all submitted tickets
4. For each ticket, you can:
   - Add troubleshooting notes
   - Update the status (Open, In Progress, Resolved)
   - Export all tickets as CSV or PDF

## Database

The application uses SQLiteCloud.io for cloud-hosted database storage with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Unique ticket identifier |
| timestamp | TEXT | When the ticket was submitted |
| name | TEXT | Submitter's name |
| email | TEXT | Submitter's email |
| issue | TEXT | Description of the problem |
| notes | TEXT | Agent notes and updates |
| status | TEXT | Current status (Open, In Progress, Resolved) |

### SQLiteCloud Advantages

- **Team Collaboration**: All team members access the same cloud database
- **No Local Files**: No need to share database files between team members
- **Automatic Backups**: Cloud-hosted with built-in backup and recovery
- **Scalability**: Handles multiple concurrent users
- **REST API**: Standard HTTP API for database operations
- **Real-time Sync**: Changes are immediately available to all team members

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page with role selection |
| `/ticket` | GET/POST | Ticket submission form |
| `/agent` | GET | Agent portal with all tickets |
| `/update_ticket/<id>` | POST | Update ticket notes and status |
| `/export_csv` | GET | Export all tickets as CSV |
| `/export_pdf` | GET | Export all tickets as PDF |

## Team Collaboration

This system is designed for team collaboration:

- **Shared Database**: All team members access the same SQLite database
- **Real-time Updates**: Changes are immediately visible to all agents
- **Export Features**: Generate reports for team meetings or documentation
- **Status Tracking**: Monitor ticket progress across the team

## Customization

### Theme Colors

The application uses a Cal.com-inspired theme. You can customize colors in `static/style.css`:

```css
:root {
    --primary-color: #3B82F6;
    --secondary-color: #2563EB;
    --accent-color: #1E40AF;
    --background-color: #F3F4F6;
    --text-color: #111827;
}
```

### Adding Features

The Flask application is modular and easy to extend:

- Add new routes in `app.py`
- Create new templates in the `templates/` directory
- Extend the database schema as needed
- Add new export formats

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Database permissions**: Ensure the application has write permissions in the project directory

3. **Missing dependencies**: Run `pip install -r requirements.txt` again

### Development Mode

The application runs in debug mode by default, which provides:
- Automatic reloading when files change
- Detailed error messages
- Debug console

## Security Notes

This is a simulation application for learning purposes. For production use, consider:

- Adding user authentication
- Implementing proper input validation
- Using environment variables for configuration
- Adding HTTPS support
- Implementing proper error handling

## License

This project is for educational and simulation purposes.
