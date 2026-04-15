from db import conn, c

def save_booking(user, source, dest, price, date):
    c.execute("INSERT INTO bookings VALUES (?, ?, ?, ?, ?)",
              (user, source, dest, price, date))
    conn.commit()