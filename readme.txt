This is a project to develop a perpetual inventory management system using
Python and sqlite3. Currently I plan to use a simple stack event driven architecture
whereby each type of event can be used to modify the main table. Transaction tables such as
sales and purchases will create events which then alter the main items table.