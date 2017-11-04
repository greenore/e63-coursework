### Setup
# Load libraries
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Setup connection
cluster = Cluster()
session = cluster.connect('hw9')

### Functions
# Create a person record
def insert_person(id, first_name, last_name, city, cell1, cell2, cell3):
  session.execute("""INSERT INTO person (id, first_name, last_name, city,
                                         cell1, cell2, cell3)
                     VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                     (id, first_name, last_name, city, cell1, cell2, cell3))

# All
def select_all():
  statement = SimpleStatement("SELECT * FROM person")
  result = session.execute(statement)
  return result

# By id
def select_one(id):
  result = session.execute("""SELECT id, first_name, city FROM person
                              WHERE id = %s""", [id])[0]
  return result

# Update city
def update_city(id, city):
  session.execute("UPDATE person SET city = %s where id = %s", (city,id))

### Add three rows
# Add three new records
insert_person(4, 'Hans-Peter', 'Hugentobler', 'Grenchen', '444-111-0000', '444-222-0000', '444-333-0000')
insert_person(5, 'Christof', 'Hausmann', 'Bottmingen', '555-111-0000', '555-222-0000', '555-333-0000')
insert_person(6, 'Gabriela', 'Tschaggelar', 'Bottmingen', '666-111-0000','666-222-0000','666-222-0000')

# Select persons
df_persons = select_all()

# Print output
for i in df_persons:
  print(i)

### Update row
# Updade id 1
update_city(1, 'Bettlach')

# Select and print
df_person = select_one(1)
print(df_person.first_name + " has a new city with the name: " + df_person.city)

