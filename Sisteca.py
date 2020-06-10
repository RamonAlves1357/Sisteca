#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importações
import os
import sqlite3
from datetime import datetime, timedelta, date

# Conectando ao BD
con = sqlite3.connect('banco.db')
cursor = con.cursor()

def createTable():	# Criando as tabelas (Alunos & Livros)
	cursor.execute("""CREATE TABLE IF NOT EXISTS Alunos(
					Matricula INT,
					Nome TEXT NOT NULL,
					CPF INT PRIMARY KEY NOT NULL,
					Telefone INT,
					Idade INT,
					Email TEXT,
					Estado TEXT,
					Cidade TEXT,
					cdLivro INT,
					Data_Enprestimo TEXT,
					Data_Entrega TEXT
					)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS Livros(
					cdLivro INT PRIMARY KEY NOT NULL,
					Nome TEXT NOT NULL,
					Genero TEXT NOT NULL,
					Paginas INT,
					Editora TEXT,
					Autor TEXT,
					Edição TEXT,
					idioma TEXT
					)""")

def leitor():		# Cadrastro de leitor
	# Solicitando os dados do leitor
	matricula = int(input(" Matricula: "))
	x = (matricula,)
	cursor.execute("SELECT matricula FROM Alunos WHERE Matricula =?", x)
	l = cursor.fetchone()

	# Verifica se o essa matricula não esta cadrastada no BD
	if not l:
		# Solicitando os dados para o cadastro do leitor
		nome = input(" Nome: ")
		cpf = int(input(" CPF: "))
		telefone = int(input(" Telefone: "))
		idade = int(input(" Idade: "))
		email = input(" Email: ")
		estado = input(" UF: ")
		cidade = input(" Cidade: ")
		cdLivro = input(" cdLivro: ")
		
		x = (cdLivro,)
		cursor.execute("SELECT cdLivro FROM Livros WHERE cdLivro =?", x)
		l = cursor.fetchone()

		# Verifica se o livro está cadrastado no BD
		if l:
			# inserindo os dados na tabela
			cursor.execute("INSERT INTO Alunos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
			(matricula, nome.title(), cpf, telefone, idade, email, estado.upper(), cidade.title(), int(cdLivro), data(0), data(15)))
			con.commit()

			# Exibe o cadrasto do Leitor 
			cursor.execute("SELECT * FROM Alunos WHERE Nome = '" + nome + "' OR Matricula =?", x)
			print()
			for linha in cursor.fetchall():
				print("=========================================================")
				print(" Matricula: ", linha[0])
				print(" Nome: ", linha[1])
				print(" CPF: ", linha[2])
				print(" Telefone: ", linha[3])
				print(" Idade: ", linha[4])
				print(" Email: ", linha[5])
				print(" UF: ", linha[6])
				print(" Cidade: ", linha[7])
				print(" Codigo do Livro: ", linha[8])
				print(" Data do Emprestimo: ", linha[9])
				print(" Data de Entrega: ", linha[10])
				print("=========================================================")
				print()
			print(" Cadrastro realizado com sucesso!")
		# Caso o livro não esteja cadrastado
		else:
			print("Livro não cadrastado no Banco de dados.")
	# Caso a matricula ja exista...
	else:
		print(" Leitor já cadrastrado!")

def livro():		# Cadrastro de livro
	# Solicitando os dados do livro
	cdLivro = int(input(" cdLivro: "))
	x = (cdLivro,)
	cursor.execute("SELECT cdLivro FROM Livros WHERE cdLivro =?", x)
	l = cursor.fetchone()

	# Verificar se livro não esta cadrastado...
	if not l:
		# Solicitando os dados para o cadastro do livro
		nome = input(" Nome: ")
		genero = input(" Genero: ")
		pag = int(input(" Quant. de Paginas: "))
		editora = input(" Editora: ")
		autor = input(" Autor: ")
		edicao = input(" Edição: ")
		idioma = input(" Idioma: ")

		# inserindo os dados na tabela
		cursor.execute("INSERT INTO Livros VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
		(cdLivro, nome.title(), genero.title(), pag, editora.title(), autor.title(), edicao, idioma.title()))
		con.commit()

		# Exibe o cadrasto do Livro
		cursor.execute("SELECT * FROM Livros WHERE Nome = '" + nome + "' OR cdLivro = '" + cdLivro + "' OR Autor = '" + autor + "' OR Genero = '" + genero + "';")
		print()
		for linha in cursor.fetchall():
			print("=========================================================")
			print(" cdLivro: ", linha[0])
			print(" Nome: ", linha[1])
			print(" Genero: ", linha[2])
			print(" Quant. de Paginas: ", linha[3])
			print(" Editora: ", linha[4])
			print(" Autor: ", linha[5])
			print(" Edição: ", linha[6])
			print(" Idioma: ", linha[7])
			print("=========================================================")
			print()
		print(" Cadrastro realizado com sucesso!")		
	# Verifica se o livro ja esta cadrastado no BD
	else:
		print(" Este livro/codigo já foi cadrastado!")

def busca_leitor():	# Função de busca
	n = input(" Digite a Matricula ou Nome: ")
	x = (n,)
	cursor.execute("SELECT * FROM Alunos WHERE Nome LIKE '%" + n + "%' OR Matricula LIKE '%" + n + "%';")
	l = cursor.fetchone()
	# Verifica se o essa matricula já existente no BD
	if l:
		cursor.execute("SELECT * FROM Alunos WHERE Nome LIKE '%" + n + "%' OR Matricula LIKE '%" + n + "%';")
		print()
		for linha in cursor.fetchall():
			print("=========================================================")
			print(" Matricula: ", linha[0])
			print(" Nome: ", linha[1])
			print(" CPF: ", linha[2])
			print(" Telefone: ", linha[3])
			print(" Idade: ", linha[4])
			print(" Email: ", linha[5])
			print(" UF: ", linha[6])
			print(" Cidade: ", linha[7])
			print(" Codigo do Livro: ", linha[8])
			print(" Data do Emprestimo: ", linha[9])
			print(" Data de Entrega: ", linha[10])
			print("=========================================================")
			print()
	else:
		print(" Leitor não cadrastado! \n Realize o cadrasto e tente novamente.")

def busca_livro():	# Função de busca
	n = input(" Digite o Nome, Codigo, Autor ou genero do livro: ")
	x = (n,)
	cursor.execute("SELECT * FROM Livros WHERE Nome LIKE '%" + n + "%' OR cdLivro LIKE '%" + n + "%' OR Autor LIKE '%" + n + "%' OR Genero LIKE '%" + n + "%'")
	l = cursor.fetchone()
	# Verificar se livro está cadrastado...
	if l:
		cursor.execute("SELECT * FROM Livros WHERE Nome LIKE '%" + n + "%' OR cdLivro LIKE '%" + n + "%' OR Autor LIKE '%" + n + "%' OR Genero LIKE '%" + n + "%'")
		print()

		for linha in cursor.fetchall():
			print("=========================================================")
			print(" cdLivro: ", linha[0])
			print(" Nome: ", linha[1])
			print(" Genero: ", linha[2])
			print(" Quant. de Paginas: ", linha[3])
			print(" Editora: ", linha[4])
			print(" Autor: ", linha[5])
			print(" Edição: ", linha[6])
			print(" Idioma: ", linha[7])
			print("=========================================================")
			print()
	else:
		print(" Livro não cadrastado! \n Realize o cadrasto e tente novamente.")

def data(x):		# Função Data
	# Pega a data atual
	data_atual = date.today()
	# somar 15 dias à data atual
	D = data_atual + timedelta(days=x)
	# Transforma a data atual em string
	#d = '{}/{}/{}'.format(D.day, D.month, D.year)
	d = D.strftime('%d/%m/%Y')
	return d	

def main():			# Função principal, montado com as funções anteriores...
	createTable()
	i = True

	print("""
		=======================================================
		||         <<<===>>> Bem Vindo <<<===>>>             ||
		||~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~||
		||            <<<===>>> ao <<<===>>>                 ||
		||~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~||
		||          <<<===>>> Sisteca! <<<===>>>             ||
		=======================================================
	 """)

	while(i == True):
		print("\n	Informe o número correspondente para a opção desejada: ")
		print("	(1) Realizar cadrastro de um livro;")
		print("	(2) Realizar cadrastro de um leitor;")
		print("	(3) Entrega de livro;")
		print("	(4) Trocar/Pegar livro;")
		print("	(5) Buscar leitor;")
		print("	(6) Consultar livro;")
		print("	(0) Para Encerrar;")
		op = int(input(">>> "))

		if(op < 0) or (op > 6):			# Caso a opção informada seja invalida
			print("\n <|||> ERRO: opção invalida... <|||> \n  **Por favor imforme uma opção valida...")

		elif(op == 1):					# Caso queira cadrastrar um livro
			os.system('cls' if os.name == 'nt' else 'clear') #limpa a tela
			livro()

		elif(op == 2):					# Caso queira cadratrar leitor
			os.system('cls' if os.name == 'nt' else 'clear') #limpa a tela
			leitor()

		elif(op == 3):					# Entrega de livro
			os.system('cls' if os.name == 'nt' else 'clear') #limpa a tela
			
			n = input(" Digite o Nome ou a Matricula: ")

			# Atualizando os valores do BD
			cursor.execute("UPDATE Alunos SET cdLivro = '' WHERE Nome = '" + n + "' OR Matricula = '" + n + "';")
			con.commit()
			cursor.execute("UPDATE Alunos SET Data_Enprestimo = '' WHERE Nome = '" + n + "' OR Matricula = '" + n + "';")
			con.commit()
			cursor.execute("UPDATE Alunos SET Data_Entrega = '' WHERE Nome = '" + n + "' OR Matricula = '" + n + "';")
			con.commit()
			
			# Mostra a entrega do livro
			cursor.execute("SELECT * FROM Alunos WHERE Nome = '" + n + "' OR Matricula = '" + n + "';")
			print()
			for linha in cursor.fetchall():
				print("=========================================================")
				print(" Matricula: ", linha[0])
				print(" Nome: ", linha[1])
				print(" CPF: ", linha[2])
				print(" Telefone: ", linha[3])
				print(" Idade: ", linha[4])
				print(" Email: ", linha[5])
				print(" UF: ", linha[6])
				print(" Cidade: ", linha[7])
				print(" Codigo do Livro: ", linha[8])
				print(" Data do Emprestimo: ", linha[9])
				print(" Data de Entrega: ", linha[10])
				print("=========================================================")
				print()
			
			print(" Entrega de livro realizada com sucesso!")

		elif(op == 4):					# Troca de livro
			os.system('cls' if os.name == 'nt' else 'clear') #limpa a tela
			
			n = input(" Digite o Nome ou a Matricula: ")
		
			# Atualizando os valores do BD		
			cd = input(" Digite o codigo do novo livro: ")
			cursor.execute("UPDATE Alunos SET cdLivro = '" + cd + "' WHERE Nome = '" + n + "' OR Matricula = '" + n + "';")
			con.commit()
			cursor.execute("UPDATE Alunos SET Data_Enprestimo = '" + data(0) + "' WHERE Nome = '" + n + "' OR Matricula = '" + n + "';")
			con.commit()
			cursor.execute("UPDATE Alunos SET Data_Entrega = '" + data(15) + "' WHERE Nome = '" + n + "' OR Matricula = '" + n + "';")
			con.commit()

			# Mostra a troca do livro
			cursor.execute("SELECT * FROM Alunos WHERE Nome = '" + n + "' OR Matricula = '" + n + "';")
			print()
			for linha in cursor.fetchall():
				print("=========================================================")
				print(" Matricula: ", linha[0])
				print(" Nome: ", linha[1])
				print(" CPF: ", linha[2])
				print(" Telefone: ", linha[3])
				print(" Idade: ", linha[4])
				print(" Email: ", linha[5])
				print(" UF: ", linha[6])
				print(" Cidade: ", linha[7])
				print(" Codigo do Livro: ", linha[8])
				print(" Data do Emprestimo: ", linha[9])
				print(" Data de Entrega: ", linha[10])
				print("=========================================================")
				print()

			print(" Troca realizada com sucesso!")
		
		elif(op == 5):					# Busca de Leitor
			os.system('cls' if os.name == 'nt' else 'clear') #limpa a tela
			busca_leitor()

		elif(op == 6): 					# Busca Livro
			os.system('cls' if os.name == 'nt' else 'clear') #limpa a tela
			busca_livro()

		elif(op == 0) or (i == False):	# Encerra o programa
			os.system('cls' if os.name == 'nt' else 'clear') #limpa a tela
			print("	Obg por usar o nosso sistema! ")
			print("				< by Ramon Alves > ")
			break
		
main()
