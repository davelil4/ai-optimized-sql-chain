import os

def create_schemata():
    file = open(os.path.join(os.getcwd(), 'database.sql'), 'r')
    
    if not os.path.exists(os.path.join(os.getcwd(), 'schemata')):
        os.mkdir(os.path.join(os.getcwd(), 'schemata'))
    
    schema_map = {}
    
    schemata = set()
    
    cur_schem = None
    
    in_table = None
    
    key_switch = False
    
    
    
    
    
    for line in file.readlines():
        
        if 'PRIMARY KEYS' in line: 
            print('switched')
            key_switch = True
        elif key_switch and 'VIEWS' in line: 
            key_switch = False
            cur_schem = None
            in_table = None
        
        if key_switch:
            
            if "ALTER TABLE" in line:
                new_line = line.lstrip("ALTER TABLE ")
                new_line = new_line.rstrip(" ADD\n")
                schema_table = new_line.split(".")
                cur_schem = schema_table[0]
                in_table = schema_table[1]
                
            try:
                f = open(os.path.join(os.getcwd(), f"schemata/{cur_schem}/{in_table}.txt"), "a")
                f.write(line)
                f.close()
            except:
                pass
        else:
            if in_table is not None and line[len(line)-3] == ')':
                f = open(os.path.join(
                    os.getcwd(),
                    f'schemata/{cur_schem}/{in_table}.txt'
                ), "a")
                
                f.write("   )\n")
                f.close()
                in_table = None
            elif in_table is not None:
                f = open(os.path.join(
                    os.getcwd(),
                    f'schemata/{cur_schem}/{in_table}.txt'
                ), "a")
                
                f.write(line)
                f.close()
                
                continue
            
            if 'CREATE SCHEMA' in line and line[14].isupper():
                
                schema = line.split("CREATE SCHEMA ")[1].replace("\n", "")
                schemata.add(schema)
                
                cur_schem = schema
                
                if os.path.exists(
                    os.path.join(os.getcwd(), 
                                f'schemata/{schema}')
                    ): continue
                
                os.mkdir(
                    os.path.join(os.getcwd(), 
                    f'schemata/{schema}'))
                
                cur_schem = schema
            
            elif 'CREATE TABLE' in line and cur_schem != None:
                table = line.split("CREATE TABLE ")[1].replace("(\n", "")
                
                in_table = table
                
                f = open(os.path.join(
                    os.getcwd(),
                    f'schemata/{cur_schem}/{in_table}.txt'
                ), "a")
                
                f.write(line)
                f.close()
                
                tables = schema_map.get(cur_schem, set())
                tables.add(table)
                
                schema_map[cur_schem] = tables
                
                if line[len(line)-3] == ';':
                    cur_schem = None

            
            
            
    
    file.close()

def create_schemata_files():
    for subdir, dirs, files in os.walk(os.path.join(os.getcwd(), 'schemata')):
        for dir in dirs:
            f = open(os.path.join(os.getcwd(), f'schemata/{dir}.txt'), 'w')
            for filename in os.listdir(os.path.join(os.getcwd(), f'schemata/{dir}')):
                f.write(open(os.path.join(os.getcwd(), f'schemata/{dir}/{filename}'), 'r').read())
            f.close()
        

if __name__ == '__main__':
    create_schemata_files()