-- ============================================================================
-- SUPPORT AUTOMATION SYSTEM - SUPABASE DATABASE SCHEMA
-- ============================================================================
-- This script creates all necessary tables and indexes for the application
-- Run this in your Supabase SQL Editor
-- ============================================================================

-- ============================================================================
-- TABLE 1: USERS
-- Stores user account information
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add comments to columns for documentation
COMMENT ON TABLE users IS 'Stores user account information and authentication data';
COMMENT ON COLUMN users.id IS 'Unique user identifier (UUID)';
COMMENT ON COLUMN users.username IS 'Unique username for display';
COMMENT ON COLUMN users.email IS 'User email address (used for login)';
COMMENT ON COLUMN users.password_hash IS 'SHA-256 hashed password';
COMMENT ON COLUMN users.verified IS 'Email verification status';
COMMENT ON COLUMN users.last_login IS 'Timestamp of last successful login';

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at DESC);

-- ============================================================================
-- TABLE 2: SUPPORT_CASES
-- Stores all support case information and workflow status
-- ============================================================================

CREATE TABLE IF NOT EXISTS support_cases (
    case_id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
    
    -- Original request information
    original_query TEXT NOT NULL,
    language TEXT NOT NULL,
    
    -- Manufacturer information
    manufacturer_id TEXT NOT NULL,
    manufacturer_name TEXT NOT NULL,
    
    -- Translation data
    translated_query TEXT,
    
    -- Workflow tracking
    task_number TEXT UNIQUE,
    status TEXT DEFAULT 'awaiting_reply',
    
    -- Timestamps
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    forwarded_at TIMESTAMP WITH TIME ZONE,
    reply_received_at TIMESTAMP WITH TIME ZONE,
    reminder_sent_at TIMESTAMP WITH TIME ZONE,
    approved_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Manufacturer response
    manufacturer_reply TEXT,
    reply_translated TEXT,
    
    -- Flags
    reminder_sent BOOLEAN DEFAULT FALSE,
    needs_approval BOOLEAN DEFAULT FALSE,
    approved BOOLEAN DEFAULT FALSE,
    
    -- Additional notes
    notes TEXT
);

-- Add comments
COMMENT ON TABLE support_cases IS 'Stores all support case data and workflow information';
COMMENT ON COLUMN support_cases.case_id IS 'Unique case identifier';
COMMENT ON COLUMN support_cases.user_email IS 'Reference to user who created the case';
COMMENT ON COLUMN support_cases.original_query IS 'Original support query in user language';
COMMENT ON COLUMN support_cases.language IS 'Language of the original query';
COMMENT ON COLUMN support_cases.manufacturer_id IS 'Manufacturer system identifier';
COMMENT ON COLUMN support_cases.task_number IS 'Unique task number from manufacturer';
COMMENT ON COLUMN support_cases.status IS 'Current workflow status';
COMMENT ON COLUMN support_cases.reminder_sent IS 'Whether 24-hour reminder has been sent';
COMMENT ON COLUMN support_cases.needs_approval IS 'Whether case needs manual approval';

-- Create indexes for optimal query performance
CREATE INDEX IF NOT EXISTS idx_cases_user_email ON support_cases(user_email);
CREATE INDEX IF NOT EXISTS idx_cases_task_number ON support_cases(task_number);
CREATE INDEX IF NOT EXISTS idx_cases_status ON support_cases(status);
CREATE INDEX IF NOT EXISTS idx_cases_submitted_at ON support_cases(submitted_at DESC);
CREATE INDEX IF NOT EXISTS idx_cases_manufacturer_id ON support_cases(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_cases_reminder_sent ON support_cases(reminder_sent) WHERE reminder_sent = FALSE;

-- Composite index for checking overdue cases
CREATE INDEX IF NOT EXISTS idx_cases_overdue ON support_cases(status, reminder_sent, forwarded_at) 
    WHERE status = 'awaiting_reply' AND reminder_sent = FALSE;

-- ============================================================================
-- TABLE 3: CASE_HISTORY
-- Stores audit trail of all changes to support cases
-- ============================================================================

CREATE TABLE IF NOT EXISTS case_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id TEXT NOT NULL REFERENCES support_cases(case_id) ON DELETE CASCADE,
    changed_by TEXT,
    action TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE case_history IS 'Audit trail for all support case changes';
COMMENT ON COLUMN case_history.action IS 'Type of action performed (e.g., status_change, reply_received)';

CREATE INDEX IF NOT EXISTS idx_history_case_id ON case_history(case_id);
CREATE INDEX IF NOT EXISTS idx_history_changed_at ON case_history(changed_at DESC);

-- ============================================================================
-- TABLE 4: MANUFACTURERS
-- Stores manufacturer configuration and contact information
-- ============================================================================

CREATE TABLE IF NOT EXISTS manufacturers (
    manufacturer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    api_url TEXT,
    contact_email TEXT,
    active BOOLEAN DEFAULT TRUE,
    response_time_hours INTEGER DEFAULT 24,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE manufacturers IS 'Configuration for all supported manufacturers';

CREATE INDEX IF NOT EXISTS idx_manufacturers_active ON manufacturers(active) WHERE active = TRUE;

-- Insert default manufacturers
INSERT INTO manufacturers (manufacturer_id, name, api_url, contact_email) VALUES
    ('manufacturer_1', 'Tech Solutions Inc.', 'https://api.techsolutions.com', 'support@techsolutions.com'),
    ('manufacturer_2', 'Global Parts Ltd.', 'https://api.globalparts.com', 'support@globalparts.com'),
    ('manufacturer_3', 'Innovation Corp.', 'https://api.innovation.com', 'support@innovation.com')
ON CONFLICT (manufacturer_id) DO NOTHING;

-- ============================================================================
-- TABLE 5: EMAIL_LOGS
-- Stores all email communications for tracking
-- ============================================================================

CREATE TABLE IF NOT EXISTS email_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id TEXT REFERENCES support_cases(case_id) ON DELETE CASCADE,
    recipient TEXT NOT NULL,
    subject TEXT NOT NULL,
    body TEXT,
    email_type TEXT NOT NULL, -- verification, notification, reminder, reply
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT DEFAULT 'sent' -- sent, failed, pending
);

COMMENT ON TABLE email_logs IS 'Logs all email communications sent by the system';

CREATE INDEX IF NOT EXISTS idx_email_case_id ON email_logs(case_id);
CREATE INDEX IF NOT EXISTS idx_email_sent_at ON email_logs(sent_at DESC);
CREATE INDEX IF NOT EXISTS idx_email_type ON email_logs(email_type);

-- ============================================================================
-- TABLE 6: SYSTEM_SETTINGS
-- Stores system configuration and settings
-- ============================================================================

CREATE TABLE IF NOT EXISTS system_settings (
    setting_key TEXT PRIMARY KEY,
    setting_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE system_settings IS 'System-wide configuration settings';

-- Insert default settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
    ('reminder_hours', '24', 'Hours before sending reminder (business hours)'),
    ('exclude_weekends', 'true', 'Exclude weekends from business hours calculation'),
    ('max_reminder_attempts', '3', 'Maximum number of reminder emails to send'),
    ('translation_api', 'mock', 'Translation API provider (mock, google, deepl)')
ON CONFLICT (setting_key) DO NOTHING;

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Active cases waiting for response
CREATE OR REPLACE VIEW active_cases AS
SELECT 
    c.case_id,
    c.user_email,
    u.username,
    c.manufacturer_name,
    c.task_number,
    c.status,
    c.submitted_at,
    c.forwarded_at,
    c.reminder_sent,
    EXTRACT(EPOCH FROM (NOW() - c.forwarded_at))/3600 AS hours_since_forwarded
FROM support_cases c
JOIN users u ON c.user_email = u.email
WHERE c.status IN ('awaiting_reply', 'reminder_sent')
ORDER BY c.submitted_at DESC;

-- View: Cases needing manual approval
CREATE OR REPLACE VIEW cases_pending_approval AS
SELECT 
    c.case_id,
    c.user_email,
    u.username,
    c.manufacturer_name,
    c.original_query,
    c.manufacturer_reply,
    c.reply_translated,
    c.submitted_at,
    c.reply_received_at
FROM support_cases c
JOIN users u ON c.user_email = u.email
WHERE c.needs_approval = TRUE AND c.approved = FALSE
ORDER BY c.reply_received_at DESC;

-- View: User statistics
CREATE OR REPLACE VIEW user_statistics AS
SELECT 
    u.username,
    u.email,
    u.created_at,
    u.last_login,
    COUNT(c.case_id) AS total_cases,
    COUNT(CASE WHEN c.status = 'awaiting_reply' THEN 1 END) AS active_cases,
    COUNT(CASE WHEN c.approved = TRUE THEN 1 END) AS resolved_cases
FROM users u
LEFT JOIN support_cases c ON u.email = c.user_email
GROUP BY u.username, u.email, u.created_at, u.last_login;

-- ============================================================================
-- FUNCTIONS FOR AUTOMATION
-- ============================================================================

-- Function: Update timestamp on record modification
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers to tables
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_cases_updated_at ON support_cases;
CREATE TRIGGER update_cases_updated_at
    BEFORE UPDATE ON support_cases
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function: Log case changes to history
CREATE OR REPLACE FUNCTION log_case_change()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE' AND OLD.status IS DISTINCT FROM NEW.status) THEN
        INSERT INTO case_history (case_id, action, old_value, new_value)
        VALUES (NEW.case_id, 'status_change', OLD.status, NEW.status);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply history trigger
DROP TRIGGER IF EXISTS log_case_changes ON support_cases;
CREATE TRIGGER log_case_changes
    AFTER UPDATE ON support_cases
    FOR EACH ROW
    EXECUTE FUNCTION log_case_change();

-- ============================================================================
-- FUNCTION: Get overdue cases (for reminder system)
-- ============================================================================

CREATE OR REPLACE FUNCTION get_overdue_cases(hours_threshold INTEGER DEFAULT 24)
RETURNS TABLE (
    case_id TEXT,
    user_email TEXT,
    manufacturer_name TEXT,
    task_number TEXT,
    hours_elapsed NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.case_id,
        c.user_email,
        c.manufacturer_name,
        c.task_number,
        ROUND(EXTRACT(EPOCH FROM (NOW() - c.forwarded_at))/3600, 2) AS hours_elapsed
    FROM support_cases c
    WHERE c.status = 'awaiting_reply'
        AND c.reminder_sent = FALSE
        AND c.forwarded_at IS NOT NULL
        AND EXTRACT(EPOCH FROM (NOW() - c.forwarded_at))/3600 > hours_threshold
        -- Exclude weekends (this is simplified - you may need more complex logic)
        AND EXTRACT(DOW FROM NOW()) NOT IN (0, 6) -- 0=Sunday, 6=Saturday
    ORDER BY c.forwarded_at ASC;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- Enable if you want user-specific data access control
-- ============================================================================

-- Enable RLS on tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE support_cases ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own data
CREATE POLICY users_select_own ON users
    FOR SELECT
    USING (auth.email() = email);

CREATE POLICY cases_select_own ON support_cases
    FOR SELECT
    USING (auth.email() = user_email);

-- Policy: Users can insert their own cases
CREATE POLICY cases_insert_own ON support_cases
    FOR INSERT
    WITH CHECK (auth.email() = user_email);

-- Policy: Users can update their own cases
CREATE POLICY cases_update_own ON support_cases
    FOR UPDATE
    USING (auth.email() = user_email);

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================

-- Grant necessary permissions to authenticated users
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- ============================================================================
-- VERIFICATION QUERIES
-- Run these to verify the schema was created successfully
-- ============================================================================

-- Check all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Check all indexes
SELECT tablename, indexname 
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Check all views
SELECT table_name 
FROM information_schema.views 
WHERE table_schema = 'public';

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Success message
DO $$ 
BEGIN 
    RAISE NOTICE 'Database schema created successfully!';
    RAISE NOTICE 'Tables: users, support_cases, case_history, manufacturers, email_logs, system_settings';
    RAISE NOTICE 'Views: active_cases, cases_pending_approval, user_statistics';
    RAISE NOTICE 'Functions: get_overdue_cases(), update_updated_at_column(), log_case_change()';
END $$;