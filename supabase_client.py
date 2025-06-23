from supabase import create_client, Client

# TU URL Y CLAVE (ajusta los valores reales)
SUPABASE_URL = "https://nfbztfxvqbzkvhobpvvw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # <--- Usa la completa solo localmente

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
