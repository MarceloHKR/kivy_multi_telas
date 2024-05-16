import sqlite3

#cria ou conecta a base de dados
conn = sqlite3.connect('example.db')

#cria o objeto cursor
cursor = conn.cursor()

#cria e executa uma tabela
#cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)''')
#conn.commit()

#insere valores na tabela
#cursor.execute("INSERT INTO users (name) VALUES ('John')")
#conn.commit()

#atualiza os dados de usuários da tabela
#cursor.execute("UPDATE users SET name = 'Jane' WHERE name = 'John'")
#conn.commit()

#seleciona todos os dados do usuário da tabela
#cursor.execute("SELECT * FROM users")
#print(cursor.fetchall())

#seleciona os dados de tal usuário
#cursor.execute("SELECT * FROM users WHERE name = 'Jane'")
#print(cursor.fetchall())

#deleta os dados da tabela
cursor.execute("DELETE FROM users WHERE name = 'Jane'")
conn.commit()

#close the connection
conn.close()