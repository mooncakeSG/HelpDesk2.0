-- IT Helpdesk Database Schema - Updated with Priority and Agent Assignment
-- SQLiteCloud.io compatible SQL schema

-- Use the database (required for SQLiteCloud)
USE DATABASE 'my-database';

-- Add new columns to existing tickets table
ALTER TABLE tickets ADD COLUMN priority TEXT DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High'));
ALTER TABLE tickets ADD COLUMN assigned_agent TEXT DEFAULT '';

-- Update the status check constraint to include more statuses
-- Note: SQLite doesn't support ALTER COLUMN, so we'll need to recreate the table
-- For now, we'll work with the existing structure and add the new columns

-- Create indexes for the new columns
CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority);
CREATE INDEX IF NOT EXISTS idx_tickets_assigned_agent ON tickets(assigned_agent);

-- Update existing tickets to have default priority and empty assigned_agent
UPDATE tickets SET priority = 'Medium' WHERE priority IS NULL;
UPDATE tickets SET assigned_agent = '' WHERE assigned_agent IS NULL;

-- Create a view for tickets by priority
CREATE VIEW IF NOT EXISTS tickets_by_priority AS
SELECT 
    priority,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tickets), 2) as percentage
FROM tickets 
GROUP BY priority;

-- Create a view for tickets by agent
CREATE VIEW IF NOT EXISTS tickets_by_agent AS
SELECT 
    assigned_agent,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tickets), 2) as percentage
FROM tickets 
WHERE assigned_agent != ''
GROUP BY assigned_agent;

-- Create a view for agent workload
CREATE VIEW IF NOT EXISTS agent_workload AS
SELECT 
    assigned_agent,
    COUNT(*) as total_tickets,
    SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) as open_tickets,
    SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) as in_progress_tickets,
    SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) as resolved_tickets
FROM tickets 
WHERE assigned_agent != ''
GROUP BY assigned_agent
ORDER BY total_tickets DESC;
