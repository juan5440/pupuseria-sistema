from database import Database
from datetime import datetime, timedelta, timezone

def verify_timezone():
    db = Database("test_timezone.db")
    
    # Create a dummy sale
    items = [{'id': 1, 'cantidad': 1, 'precio': 1.00}]
    venta_id = db.create_sale(1.00, 1.00, 0.00, items)
    
    # Fetch the sale
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fecha FROM ventas WHERE id = ?", (venta_id,))
    fecha_str = cursor.fetchone()[0]
    conn.close()
    
    print(f"Fecha guardada: {fecha_str}")
    
    # Calculate expected time (approximate)
    offset = timezone(timedelta(hours=-6))
    expected = datetime.now(offset)
    
    # Parse saved time
    saved = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    # Add timezone info to saved time for comparison (since it's naive in DB)
    saved = saved.replace(tzinfo=offset)
    
    diff = abs((expected - saved).total_seconds())
    print(f"Diferencia en segundos: {diff}")
    
    if diff < 5:
        print("VERIFICACIÓN EXITOSA: La fecha coincide con UTC-6")
    else:
        print("VERIFICACIÓN FALLIDA: La fecha no coincide")

if __name__ == "__main__":
    verify_timezone()
