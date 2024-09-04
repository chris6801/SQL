import sqlite3

con = sqlite3.connect("inv.db")

cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upc INTEGER,
            item VARCHAR(255),
            pi INTEGER)
    """)

cur.execute("""CREATE TABLE IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date VARCHAR(255),
            upc INTEGER,
            item VARCHAR(255),
            qty INTEGER,
            price REAL,
            total REAL)
    """)

event_stack = []

event_test = ('sale', 2, 4, cur)
event_testp = ('purchase', 3, 10, cur)

event_stack.append(event_testp)

cur = con.cursor()
event_stack.append(event_test)

for item in event_stack:
    print(list(item))


def add_item(upc, item, pi, cur):
    cur.execute(f"""
        INSERT INTO items (upc, item, pi)
        SELECT ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM items WHERE upc=?)
    """, (upc, item, pi, upc))

def add_sale(date, upc, item, qty, price, total, cur):
    cur.execute(f"""
        INSERT INTO sales (date, upc, item, qty, price, total)
        SELECT ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM items WHERE upc=?)
    """, (date, upc, item, qty, price, total))
    #tries to add item in case not in items
    add_item(upc, item, 0)
    event_stack.append('sales', upc, qty, c)

def modify_entry(table, id, col, val, cur):
    cur.execute(f"""
        UPDATE {table} SET {col} = ? WHERE id = ? 
    """, (val, id))

def parse_event(event_type, upc, amt, cur):
    match event_type:
        case 'sale':
            cur.execute("SELECT pi FROM items WHERE upc=?", (upc,))
            out = cur.fetchone()
            
            if out is not None:
                current_pi = out[0]
                new_pi = current_pi - amt

                modify_entry('items', upc, 'pi', new_pi, cur)
            else:
                print(f"No item found with UPC: {upc}")
        case 'purchase':
            cur.execute("SELECT pi FROM items WHERE upc=?", (upc,))
            out = cur.fetchone()
            
            if out is not None:
                current_pi = out[0]
                new_pi = current_pi + amt

                modify_entry('items', upc, 'pi', new_pi, cur)
            else:
                print(f"No item found with UPC: {upc}")
        case 'waste':
            cur.execute("SELECT pi FROM items WHERE upc=?", (upc,))
            out = cur.fetchone()
            
            if out is not None:
                current_pi = out[0]
                new_pi = current_pi - amt

                modify_entry('items', upc, 'pi', new_pi, cur)
            else:
                print(f"No item found with UPC: {upc}")             

#modify_entry('items', 2, 'pi', 10, cur)

while event_stack:
    e = event_stack.pop()
    parse_event(*e)
print(list(event_stack))

#add_item(4, 'potato', 3, cur)
add_sale('12/20/2024', 3, 'red apple', 5, 2.99, 14.95, cur)

con.commit()

cur.close()
con.close()

new_con = sqlite3.connect("inv.db")
new_cur = new_con.cursor()

new_cur.execute("SELECT * FROM items")

res = new_cur.fetchall()

for e in res:
    print(e)

new_cur.close()
new_con.close()
