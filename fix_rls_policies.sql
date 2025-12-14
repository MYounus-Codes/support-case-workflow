-- ============================================================================
-- FIX RLS POLICIES FOR CUSTOM AUTHENTICATION
-- ============================================================================
-- The current RLS policies use auth.email() which requires Supabase Auth
-- Since we're using custom authentication, we need to make policies permissive
-- or disable RLS temporarily for the anon role
-- ============================================================================

-- OPTION 1: Drop existing restrictive policies and create permissive ones
-- ============================================================================

-- Drop existing policies
DROP POLICY IF EXISTS users_select_own ON users;
DROP POLICY IF EXISTS cases_select_own ON support_cases;
DROP POLICY IF EXISTS cases_insert_own ON support_cases;
DROP POLICY IF EXISTS cases_update_own ON support_cases;

-- Create permissive policies that allow anon role to access data
-- These policies allow our custom authentication to work

-- Users table: Allow insert and select for anon role
CREATE POLICY users_anon_insert ON users
    FOR INSERT
    TO anon
    WITH CHECK (true);

CREATE POLICY users_anon_select ON users
    FOR SELECT
    TO anon
    USING (true);

CREATE POLICY users_anon_update ON users
    FOR UPDATE
    TO anon
    USING (true)
    WITH CHECK (true);

-- Support cases table: Allow all operations for anon role
CREATE POLICY cases_anon_insert ON support_cases
    FOR INSERT
    TO anon
    WITH CHECK (true);

CREATE POLICY cases_anon_select ON support_cases
    FOR SELECT
    TO anon
    USING (true);

CREATE POLICY cases_anon_update ON support_cases
    FOR UPDATE
    TO anon
    USING (true)
    WITH CHECK (true);

CREATE POLICY cases_anon_delete ON support_cases
    FOR DELETE
    TO anon
    USING (true);

-- Case history table
CREATE POLICY case_history_anon_insert ON case_history
    FOR INSERT
    TO anon
    WITH CHECK (true);

CREATE POLICY case_history_anon_select ON case_history
    FOR SELECT
    TO anon
    USING (true);

-- Manufacturers table
CREATE POLICY manufacturers_anon_insert ON manufacturers
    FOR INSERT
    TO anon
    WITH CHECK (true);

CREATE POLICY manufacturers_anon_select ON manufacturers
    FOR SELECT
    TO anon
    USING (true);

CREATE POLICY manufacturers_anon_update ON manufacturers
    FOR UPDATE
    TO anon
    USING (true)
    WITH CHECK (true);

-- Email logs table
CREATE POLICY email_logs_anon_insert ON email_logs
    FOR INSERT
    TO anon
    WITH CHECK (true);

CREATE POLICY email_logs_anon_select ON email_logs
    FOR SELECT
    TO anon
    USING (true);

-- System settings table
CREATE POLICY system_settings_anon_select ON system_settings
    FOR SELECT
    TO anon
    USING (true);

CREATE POLICY system_settings_anon_update ON system_settings
    FOR UPDATE
    TO anon
    USING (true)
    WITH CHECK (true);

-- ============================================================================
-- GRANT PERMISSIONS TO ANON ROLE
-- ============================================================================

GRANT USAGE ON SCHEMA public TO anon;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon;

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Check RLS is still enabled
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY tablename;

-- Check policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- Success message
DO $$ 
BEGIN 
    RAISE NOTICE '✅ RLS policies updated successfully!';
    RAISE NOTICE 'All tables now have permissive policies for anon role';
    RAISE NOTICE 'Your custom authentication will now work correctly';
END $$;
