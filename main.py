import sqlite3

con = sqlite3.connect("inv.db")

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS items (upc, item, pi)")
cur.execute("CREATE TABLE IF NOT EXISTS sales (id, date, upc, item, qty)")

cur.execute("ALTER TABLE items MODIFY upc INT")

event_stack = []

event_test = ('sale', 2, 4, cur)
event_testp = ('purchase', 3, 10, cur)

event_stack.append(event_testp)
event_stack.append(event_test)

for item in event_stack:
    print(list(item))

def add_entry(table, upc, item, pi, *args, **kwargs):
    cur.execute(f"""
        INSERT INTO {table} (upc, item, pi)
        SELECT ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM items WHERE upc=?)
    """, (upc, item, pi, upc))

def modify_entry(table, upc, col, val, cur):
    cur.execute(f"""
        UPDATE {table} SET {col} = ? WHERE upc = ? 
    """, (val, upc))

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

add_entry(sales, 1, )

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
