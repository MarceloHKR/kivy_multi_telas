import sqlite3

conn = sqlite3.connect('cardapio.db')

cursor =conn.cursor()

#verifica de a tabela já existe
cursor.execute('''
    SELECT count(name) FROM sqlite_master WHERE
    type='table' AND name='cardapio'
''')

#se a tabela não existir ela é criada
if cursor.fetchone()[0]==0:
    cursor.execute(''' 
        CREATE TABLE cardapio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            descricao TEXT,
            disponivel INTEGER DEFAULT 1,
            pedido TEXT
                
        )      
    ''')

    conn.commit()


while True:
    nome = input("Nome do item(digite 'sair' para sair): ")
    if nome =="sair":
        break
    preco = float(input("Preço do item: "))
    descricao = input("descrição do item: ")
    pedido = input("pedido (1 - cozinha, 2 - Bar): ")
    pedido = "Cozinha" if pedido == "1" else "Bar"

    cursor.execute(f'''
        INSERT INTO cardapio (nome, preco, descricao, pedido)
        VALUES ('{nome}', {preco}, '{descricao}', '{pedido}')
    ''')
    
    conn.commit()

conn.close()