from supabase import create_client

SUPABASE_URL = "https://nfbztfxvqbzkvhobpvvw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mYnp0Znh2cWJ6a3Zob2JwdnZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA2ODkxMjQsImV4cCI6MjA2NjI2NTEyNH0.JRUoCqITGFyj5FWmtYCWWOTPepBeWc442I9jSWIBtQI"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


