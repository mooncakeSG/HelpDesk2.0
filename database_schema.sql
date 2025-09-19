-- IT Helpdesk Database Schema
-- SQLiteCloud.io compatible SQL schema

-- Use the database (required for SQLiteCloud)
USE DATABASE 'my-database';

-- Create the tickets table
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    issue TEXT NOT NULL,
    notes TEXT DEFAULT '',
    status TEXT DEFAULT 'Open' CHECK (status IN ('Open', 'In Progress', 'Resolved'))
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tickets_timestamp ON tickets(timestamp);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_email ON tickets(email);

-- Insert some sample data (optional - remove if not needed)
INSERT OR IGNORE INTO tickets (timestamp, name, email, issue, notes, status) VALUES
('2024-01-15 09:30:00', 'John Smith', 'john.smith@company.com', 'Unable to access company email. Getting authentication error when trying to log in.', '', 'Open'),
('2024-01-15 10:15:00', 'Sarah Johnson', 'sarah.johnson@company.com', 'Laptop is running very slowly. Takes 5+ minutes to boot up and applications are unresponsive.', 'Restarted laptop and ran disk cleanup. Issue persists.', 'In Progress'),
('2024-01-15 11:00:00', 'Mike Wilson', 'mike.wilson@company.com', 'Need help setting up VPN connection for remote work. Following the guide but getting connection timeout errors.', 'Provided updated VPN configuration. User successfully connected.', 'Resolved'),
('2024-01-15 14:20:00', 'Emily Davis', 'emily.davis@company.com', 'Printer in office is showing "Paper Jam" error but no paper is visible. Tried opening all compartments.', '', 'Open'),
('2024-01-15 15:45:00', 'David Brown', 'david.brown@company.com', 'Microsoft Office applications are not opening. Getting "Application Error" when trying to launch Word or Excel.', 'Reinstalled Office suite. Issue resolved.', 'Resolved');

-- Create a view for ticket statistics (optional)
CREATE VIEW IF NOT EXISTS ticket_stats AS
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tickets), 2) as percentage
FROM tickets 
GROUP BY status;

-- Create a view for recent tickets (last 7 days)
CREATE VIEW IF NOT EXISTS recent_tickets AS
SELECT 
    id,
    timestamp,
    name,
    email,
    issue,
    status
FROM tickets 
WHERE datetime(timestamp) >= datetime('now', '-7 days')
ORDER BY timestamp DESC;
