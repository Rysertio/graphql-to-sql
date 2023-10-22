import re

# Sample GraphQL schema data
schema = '''
type Author {
    ID: ID!
    name: String!
}

type Book {
    ID: ID!
    title: String!
    author: Author!
}
'''

# Define data types for mapping GraphQL types to SQL types
data_types = {
    'ID': 'INTEGER PRIMARY KEY',
    'String': 'TEXT',
    'Float' : 'FLOAT',
    'Int' : 'INT',
    'Boolean' : 'BOOLEAN'
}

# Regular expression to match GraphQL type definitions
type_pattern = r'type (\w+) {([^}]+)}'
field_pattern = r'\s+(\w+): ([\w\[\]!]+)'

# Parse the schema and generate SQL CREATE TABLE statements
matches = re.finditer(type_pattern, schema)
for match in matches:
    table_name = match.group(1)
    fields = re.finditer(field_pattern, match.group(2))
    
    sql_fields = []
    foreign_keys = []
    
    for field in fields:
        column_name = field.group(1)
        field_type = field.group(2)
        
        # Check if it's a foreign key
        if field_type not in data_types:
            field_type = 'INTEGER'
            foreign_keys.append(f'FOREIGN KEY ({column_name}) REFERENCES {field_type} (ID)')
        
        # Check for not null and arrays
        if '!' in field_type:
            field_type = field_type.rstrip('!')
            is_nullable = 'NOT NULL'
        else:
            is_nullable = ''
        
        if '[' in field_type:
            field_type = field_type.lstrip('[').rstrip(']')
        
        # Check for primary key
        if column_name == 'ID':
            sql_fields.append(f'{column_name} {field_type} PRIMARY KEY {is_nullable}')
        else:
            sql_fields.append(f'{column_name} {field_type} {is_nullable}')
    
    create_table_sql = f'CREATE TABLE {table_name} ({", ".join(sql_fields)}, {", ".join(foreign_keys)});'
    print(create_table_sql)
