from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import requests
import csv
import io
import os
from datetime import datetime
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# SQLiteCloud configuration
API_KEY = os.getenv("SQLITECLOUD_API_KEY")
API_URL = os.getenv("SQLITECLOUD_URL")

if not API_KEY or not API_URL:
    raise ValueError("SQLITECLOUD_API_KEY and SQLITECLOUD_URL must be set in environment variables")

headers = {"Authorization": f"Bearer {API_KEY}"}

# Database helper functions
def execute_query(query, params=None):
    """Execute a query against SQLiteCloud API"""
    try:
        # Include USE DATABASE in the same request
        full_query = f"USE DATABASE 'my-database'; {query}"
        
        # SQLiteCloud v2 API format
        payload = {"sql": full_query}
        if params:
            payload["params"] = params
        
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        # Handle SQLiteCloud v2 response format
        if 'data' in result:
            return result
        elif 'result' in result:
            return {'data': result['result']}
        else:
            return result
            
    except requests.exceptions.RequestException as e:
        print(f"Database error: {e}")
        return None

def init_db():
    """Initialize the tickets table in SQLiteCloud"""
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            name TEXT,
            email TEXT,
            issue TEXT,
            notes TEXT,
            status TEXT DEFAULT 'Open'
        )
    '''
    result = execute_query(create_table_query)
    if result is None:
        print("Warning: Could not initialize database table")

# Initialize database on startup
init_db()

def send_ticket_notification(name, email, issue, priority):
    """Send email notification to helpdesk team when a new ticket is submitted"""
    try:
        # Prepare ticket data for email notification
        ticket_data = {
            "name": name,
            "email": email,
            "subject": f"New Ticket - {priority} Priority",
            "description": issue
        }
        
        # Send to email notification service
        email_service_url = "https://it-helpdesk-email.onrender.com/submit_ticket"
        
        response = requests.post(
            email_service_url,
            json=ticket_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Email notification sent for ticket from {name}")
        else:
            print(f"❌ Email notification failed: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Email notification service not available (port 5001)")
    except Exception as e:
        print(f"❌ Email notification error: {e}")

@app.route('/')
def index():
    """Landing page with role selection"""
    return render_template('index.html')

@app.route('/ticket', methods=['GET', 'POST'])
def ticket_form():
    """User ticket submission form"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        issue = request.form.get('issue')
        priority = request.form.get('priority', 'Medium')  # Default to Medium if not specified
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Escape single quotes to prevent SQL injection
        name_escaped = name.replace("'", "''")
        email_escaped = email.replace("'", "''")
        issue_escaped = issue.replace("'", "''")
        priority_escaped = priority.replace("'", "''")
        
        # Store in SQLiteCloud database
        insert_query = f'''
            USE DATABASE 'my-database';
            INSERT INTO tickets (timestamp, name, email, issue, notes, status, priority, assigned_agent)
            VALUES ('{timestamp}', '{name_escaped}', '{email_escaped}', '{issue_escaped}', '', 'Open', '{priority_escaped}', '')
        '''
        
        result = execute_query(insert_query)
        if result is None:
            return render_template('ticket_form.html', error="Failed to submit ticket. Please try again.")
        
        # Send email notification to helpdesk team
        try:
            send_ticket_notification(name, email, issue, priority)
        except Exception as e:
            print(f"Email notification failed: {e}")
            # Don't fail the ticket submission if email fails
        
        return redirect(url_for('index'))
    
    return render_template('ticket_form.html')

@app.route('/agent')
def agent_page():
    """Agent page showing all tickets"""
    select_query = 'SELECT * FROM tickets ORDER BY timestamp DESC'
    result = execute_query(select_query)
    
    if result is None:
        return render_template('agent_page.html', tickets=[], error="Failed to load tickets. Please try again.")
    
    # Extract data from SQLiteCloud response and convert to tuple format for template compatibility
    raw_tickets = result.get('data', [])
    tickets = []
    
    for ticket in raw_tickets:
        # Convert dictionary to tuple format: (id, timestamp, name, email, issue, notes, status, priority, assigned_agent)
        ticket_tuple = (
            ticket.get('id', ''),
            ticket.get('timestamp', ''),
            ticket.get('name', ''),
            ticket.get('email', ''),
            ticket.get('issue', ''),
            ticket.get('notes', ''),
            ticket.get('status', 'Open'),
            ticket.get('priority', 'Medium'),
            ticket.get('assigned_agent', '')
        )
        tickets.append(ticket_tuple)
    
    return render_template('agent_page.html', tickets=tickets)

@app.route('/update_ticket/<int:ticket_id>', methods=['POST'])
def update_ticket(ticket_id):
    """Update notes, status, priority, and assigned agent for a ticket"""
    notes = request.form.get('notes', '')
    status = request.form.get('status', 'Open')
    priority = request.form.get('priority', 'Medium')
    assigned_agent = request.form.get('assigned_agent', '')
    
    # Escape single quotes to prevent SQL injection
    notes_escaped = notes.replace("'", "''")
    priority_escaped = priority.replace("'", "''")
    assigned_agent_escaped = assigned_agent.replace("'", "''")
    
    update_query = f'''
        USE DATABASE 'my-database';
        UPDATE tickets 
        SET notes = '{notes_escaped}', status = '{status}', priority = '{priority_escaped}', assigned_agent = '{assigned_agent_escaped}'
        WHERE id = {ticket_id}
    '''
    
    result = execute_query(update_query)
    if result is None:
        return redirect(url_for('agent_page') + '?error=update_failed')
    
    return redirect(url_for('agent_page'))

@app.route('/export_csv')
def export_csv():
    """Export all tickets as CSV file"""
    select_query = 'SELECT * FROM tickets ORDER BY timestamp DESC'
    result = execute_query(select_query)
    
    if result is None:
        return "Failed to export tickets. Please try again.", 500
    
    # Extract data from SQLiteCloud response and convert to tuple format
    raw_tickets = result.get('data', [])
    tickets = []
    
    for ticket in raw_tickets:
        ticket_tuple = (
            ticket.get('id', ''),
            ticket.get('timestamp', ''),
            ticket.get('name', ''),
            ticket.get('email', ''),
            ticket.get('issue', ''),
            ticket.get('notes', ''),
            ticket.get('status', 'Open'),
            ticket.get('priority', 'Medium'),
            ticket.get('assigned_agent', '')
        )
        tickets.append(ticket_tuple)
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Timestamp', 'Name', 'Email', 'Issue', 'Notes', 'Status', 'Priority', 'Assigned Agent'])
    
    # Write ticket data
    for ticket in tickets:
        writer.writerow(ticket)
    
    # Prepare file for download
    output.seek(0)
    csv_data = io.BytesIO()
    csv_data.write(output.getvalue().encode('utf-8'))
    csv_data.seek(0)
    
    return send_file(
        csv_data,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'tickets_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/export_pdf')
def export_pdf():
    """Export all tickets as PDF file"""
    select_query = 'SELECT * FROM tickets ORDER BY timestamp DESC'
    result = execute_query(select_query)
    
    if result is None:
        return "Failed to export tickets. Please try again.", 500
    
    # Extract data from SQLiteCloud response and convert to tuple format
    raw_tickets = result.get('data', [])
    tickets = []
    
    for ticket in raw_tickets:
        ticket_tuple = (
            ticket.get('id', ''),
            ticket.get('timestamp', ''),
            ticket.get('name', ''),
            ticket.get('email', ''),
            ticket.get('issue', ''),
            ticket.get('notes', ''),
            ticket.get('status', 'Open'),
            ticket.get('priority', 'Medium'),
            ticket.get('assigned_agent', '')
        )
        tickets.append(ticket_tuple)
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Create content
    story = []
    
    # Title
    title = Paragraph("IT Helpdesk Tickets Report", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Create table data
    table_data = [['ID', 'Timestamp', 'Name', 'Email', 'Issue', 'Notes', 'Status', 'Priority', 'Agent']]
    
    for ticket in tickets:
        # Truncate long text for better display
        issue_text = ticket[4][:40] + '...' if len(ticket[4]) > 40 else ticket[4]
        notes_text = ticket[5][:25] + '...' if len(ticket[5]) > 25 else ticket[5]
        
        table_data.append([
            str(ticket[0]),
            ticket[1],
            ticket[2],
            ticket[3],
            issue_text,
            notes_text,
            ticket[6],
            ticket[7],
            ticket[8] if ticket[8] else 'Unassigned'
        ])
    
    # Create table
    table = Table(table_data, colWidths=[0.4*inch, 1*inch, 0.8*inch, 1.2*inch, 1.5*inch, 1.2*inch, 0.6*inch, 0.6*inch, 0.8*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'tickets_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
