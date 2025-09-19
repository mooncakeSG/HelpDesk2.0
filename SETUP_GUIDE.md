# SQLiteCloud Setup Guide

## Step 1: Get SQLiteCloud Credentials

1. Sign up for a free account at [SQLiteCloud.io](https://sqlitecloud.io)
2. Create a new database
3. Get your API key and database URL from the dashboard

## Step 2: Configure Environment Variables

1. Copy `env_template.txt` to `.env`
2. Update the `.env` file with your actual credentials:

```bash
# Copy the template
cp env_template.txt .env

# Edit the .env file with your credentials
SQLITECLOUD_API_KEY=your_actual_api_key_from_dashboard
SQLITECLOUD_URL=https://api.sqlitecloud.io/v1/db/your_actual_db_id/query
SECRET_KEY=generate_a_secure_random_key
```

## Step 3: Set Up Database Schema

1. **Option A: Use the SQL schema file** (Recommended):
   - Use the provided `database_schema.sql` file
   - Execute it in your SQLiteCloud dashboard or via API
   - This creates the table with sample data and indexes

2. **Option B: Let the application create it automatically**:
   - The application will create the basic table structure when it starts

## Step 4: Test the Connection

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Test your SQLiteCloud connection**:
   ```bash
   python setup_sqlitecloud.py
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Step 4: Verify Setup

1. Open your browser to `http://localhost:5000`
2. Submit a test ticket
3. Check the agent portal to see the ticket
4. Verify the ticket appears in your SQLiteCloud dashboard

## Troubleshooting

### Common Issues

1. **"SQLITECLOUD_API_KEY and SQLITECLOUD_URL must be set"**
   - Make sure your `.env` file exists and contains the correct variables
   - Check that there are no extra spaces in your API key or URL

2. **"Database error" messages**
   - Verify your API key is correct
   - Check that your database URL is properly formatted
   - Ensure your SQLiteCloud account is active

3. **Connection timeouts**
   - Check your internet connection
   - Verify the SQLiteCloud service is accessible

### Testing Without SQLiteCloud

If you want to test the application without SQLiteCloud first, you can temporarily modify `app.py` to use local SQLite by:

1. Commenting out the SQLiteCloud configuration
2. Uncommenting the original SQLite code
3. This will create a local `tickets.db` file for testing

## Database Schema

The `database_schema.sql` file contains:

- **Table Creation**: Creates the `tickets` table with proper structure
- **Indexes**: Performance indexes on timestamp, status, and email
- **Sample Data**: 5 sample tickets for testing
- **Views**: Pre-built views for statistics and recent tickets
- **Constraints**: Data validation rules

### To use the schema:

1. **Via SQLiteCloud Dashboard**:
   - Copy the contents of `database_schema.sql`
   - Paste into the SQL editor in your dashboard
   - Execute the script

2. **Via API** (using the setup script):
   ```bash
   python setup_sqlitecloud.py
   ```

## Next Steps

Once your SQLiteCloud integration is working:

1. Share the `.env` template with your team
2. Each team member should create their own SQLiteCloud account or use shared credentials
3. All team members will access the same cloud database
4. No need to share database files - everything is in the cloud!
