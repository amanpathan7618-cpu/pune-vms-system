import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="postgres123",
        database="postgres"
    )
    
    conn.autocommit = True
    cur = conn.cursor()
    
    try:
        cur.execute("CREATE DATABASE vms_punesmartcity;")
        print("✅ Database 'vms_punesmartcity' created successfully!")
    except psycopg2.errors.DuplicateDatabase:
        print("✅ Database 'vms_punesmartcity' already exists!")
    
    cur.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"❌ Error: {e}")
    print("Make sure PostgreSQL is running and password is correct!")
except Exception as e:
    print(f"❌ Unexpected error: {e}")