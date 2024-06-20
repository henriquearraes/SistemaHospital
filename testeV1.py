import bancodedados_mysql

endereco = "localhost"
usuario = "root"
senha = "root"

conexao = bancodedados_mysql.criarConexaoInicial(endereco, usuario, senha)

sql_criar_bd = "CREATE DATABASE IF NOT EXISTS hospitalABC"
bancodedados_mysql.criarBancoDados(conexao, sql_criar_bd)


pacientes = {}
sql_criar_tabela_pacientes = """
    CREATE TABLE IF NOT EXISTS pacientes(
        cpf INT AUTO_INCREMENT PRIMARY KEY,
        idade INT,
        endereco VARCHAR(50),
        telefone INT,
    )
"""
bancodedados_mysql.criarTabela(conexao, "hospitalABC", sql_criar_tabela_pacientes)
medicos = {}
sql_criar_tabela_medicos = """
    CREATE TABLE IF NOT EXISTS medicos(
        crm INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(50),
        especialidade VARCHAR(30),
        telefone INT,
    )
"""
bancodedados_mysql.criarTabela(conexao, "hospitalABC", sql_criar_tabela_medicos)

def adicionar_novo_paciente():
    cpf = input("CPF: ")
    if cpf in pacientes:
        print("CPF ja cadastrado. Tente novamente.")
        return
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    endereco = input("Endereço: ")
    telefone = input("Telefone: ")
    pacientes[cpf] = {"nome": nome, "idade": idade, "endereco": endereco, "telefone": telefone}
    sql_inserir_paciente = "INSERT INTO pacientes (cpf, nome, idade, endereco, telefone) VALUES (%d, %s, %d, %s, %d)"
    insert_paciente = (cpf, nome, idade, endereco, telefone)
    bancodedados_mysql.insertNaTabela(conexao, "hospitalABC", sql_inserir_paciente)
    print("Novo paciente cadastrado com sucesso!")

def adicionar_novo_medico():
    crm = input("CRM: ")
    if crm in medicos:
        print("CRM ja cadastrado. Tente novamente.")
        return
    nome = input("Nome: ")
    especialidade = input("Especialidade: ")
    telefone = input("Telefone: ")
    medicos[crm] = {"nome": nome, "especialidade": especialidade, "telefone": telefone}
    sql_inserir_medico = "INSERT INTO medicos (crm, nome, especialidade, telefone) VALUES (%d, %s, %s, %d)"
    insert_medico = (crm, nome, especialidade, telefone)
    bancodedados_mysql.insertNaTabela(conexao, "hospitalABC", sql_inserir_medico)
    print("Novo medico cadastrado com sucesso!")

def pesquisar_paciente_por_cpf():
    cpf = input("CPF do paciente: ")
    paciente = pacientes.get(cpf)
    listar_db_pacientes = "SELECT * FROM pacientes WHERE cpf = %d"
    listar_db_paciente_cpf = (cpf)
    bancodedados_mysql.listarBancoDados(conexao, listar_db_pacientes)
    if paciente:
        print(f"Nome: {paciente['nome']}")
        print(f"Idade: {paciente['idade']}")
        print(f"Endereço: {paciente['endereco']}")
        print(f"Telefone: {paciente['telefone']}")
    else:
        print("Paciente nao encontrado.")
        


def pesquisar_medico_por_crm():
    crm = input("CRM do medico: ")
    medico = medicos.get(crm)
    listar_db_medicos = "SELECT * FROM medicos WHERE cpf = %d"
    listar_db_medicos_cpf = (crm)
    bancodedados_mysql.listarBancoDados(conexao, listar_db_medicos)
    if medico:
        print(f"Nome: {medico['nome']}")
        print(f"Especialidade: {medico['especialidade']}")
        print(f"Telefone: {medico['telefone']}")
    else:
        print("Medico não encontrado.")

def excluir_paciente_pelo_cpf():
    cpf = input("CPF do paciente a ser excluido: ")
    if cpf in pacientes:
        del pacientes[cpf]
        sql_remover_paciente = "DELETE FROM pacientes WHERE cpf = %d"
        sql_remover_paciente_cpf = (cpf)
        bancodedados_mysql.excluirDadosTabela(conexao, sql_remover_paciente, sql_remover_paciente_cpf)
        print("Registro excluido com sucesso!")
    else:
        print("Paciente nao encontrado.")
    
    

def excluir_medico_pelo_crm():
    crm = input("CRM do medico a ser excluido: ")
    if crm in medicos:
        del medicos[crm]
        sql_remover_medico = "DELETE FROM medicos WHERE crm = %d"
        sql_remover_medico_crm = (crm)
        bancodedados_mysql.excluirDadosTabela(conexao, sql_remover_medico, sql_remover_medico_crm)
        print("Registro excluido com sucesso!")
    else:
        print("Medico nao encontrado.")

def menu():
    while True:
        print("\nSistema Gerenciamento - Hospital ABC")
        print("1. Adicionar Novo Paciente")
        print("2. Adicionar Novo Medico")
        print("3. Pesquisar Paciente por CPF")
        print("4. Pesquisar Medico por CRM")
        print("5. Excluir Paciente pelo CPF")
        print("6. Excluir Medico pelo CRM")
        print("7. Sair do Sistema")

        opcao = input("Escolha uma opcao: ")

        if opcao == '1':
            adicionar_novo_paciente()
        elif opcao == '2':
            adicionar_novo_medico()
        elif opcao == '3':
            pesquisar_paciente_por_cpf()
        elif opcao == '4':
            pesquisar_medico_por_crm()
        elif opcao == '5':
            excluir_paciente_pelo_cpf()
        elif opcao == '6':
            excluir_medico_pelo_crm()
        elif opcao == '7':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()