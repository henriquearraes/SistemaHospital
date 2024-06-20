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
        nome VARCHAR(50),
        idade INT,
        endereco VARCHAR(50),
        telefone INT
    )
"""
bancodedados_mysql.criarTabela(conexao, "hospitalABC", sql_criar_tabela_pacientes)
medicos = {}
sql_criar_tabela_medicos = """
    CREATE TABLE IF NOT EXISTS medicos(
        crm INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(50),
        especialidade VARCHAR(30),
        telefone INT
    )
"""
bancodedados_mysql.criarTabela(conexao, "hospitalABC", sql_criar_tabela_medicos)

sql_criar_tabela_agendamentos = """
    CREATE TABLE IF NOT EXISTS agendamentos(
        id INT AUTO_INCREMENT PRIMARY KEY,
        cpf_paciente INT,
        crm_medico INT,
        data VARCHAR(25),
        hora VARCHAR(25),
        FOREIGN KEY (cpf_paciente) REFERENCES pacientes(cpf),
        FOREIGN KEY (crm_medico) REFERENCES medicos(crm)
    )
"""
bancodedados_mysql.criarTabela(conexao, "hospitalABC", sql_criar_tabela_agendamentos)

sql_criar_tabela_procedimentos = """
    CREATE TABLE IF NOT EXISTS procedimentos(
        id INT AUTO_INCREMENT PRIMARY KEY,
        cpf_paciente INT,
        crm_medico INT,
        descricao VARCHAR(255),
        data VARCHAR(25),
        FOREIGN KEY (cpf_paciente) REFERENCES pacientes(cpf),
        FOREIGN KEY (crm_medico) REFERENCES medicos(crm)
    )
"""
bancodedados_mysql.criarTabela(conexao, "hospitalABC", sql_criar_tabela_procedimentos)

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
    sql_inserir_paciente = "INSERT INTO pacientes (cpf, nome, idade, endereco, telefone) VALUES (%s, %s, %s, %s, %s)"
    insert_paciente = (cpf, nome, idade, endereco, telefone)
    bancodedados_mysql.insertNaTabela(conexao, sql_inserir_paciente, insert_paciente)
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
    sql_inserir_medico = "INSERT INTO medicos (crm, nome, especialidade, telefone) VALUES (%s, %s, %s, %s)"
    insert_medico = (crm, nome, especialidade, telefone)
    bancodedados_mysql.insertNaTabela(conexao, sql_inserir_medico, insert_medico)
    print("Novo medico cadastrado com sucesso!")

def pesquisar_paciente_por_cpf():
    cpf = input("CPF do paciente: ")
    paciente = pacientes.get(cpf)
    listar_db_pacientes = f"SELECT * FROM pacientes WHERE cpf = {cpf} "
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
    listar_db_medicos = f"SELECT * FROM medicos WHERE crm = {crm}"
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
        sql_remover_paciente = "DELETE FROM pacientes WHERE cpf = %s"
        sql_remover_paciente_cpf = (cpf,)
        bancodedados_mysql.excluirDadosTabela(conexao, sql_remover_paciente, sql_remover_paciente_cpf)
        print("Registro excluido com sucesso!")
    else:
        print("Paciente nao encontrado.")
    
    

def excluir_medico_pelo_crm():
    crm = input("CRM do medico a ser excluido: ")
    if crm in medicos:
        del medicos[crm]
        sql_remover_medico = "DELETE FROM medicos WHERE crm = %s"
        sql_remover_medico_crm = (crm,)
        bancodedados_mysql.excluirDadosTabela(conexao, sql_remover_medico, sql_remover_medico_crm)
        print("Registro excluido com sucesso!")
    else:
        print("Medico nao encontrado.")

def agendar_consulta():
    cpf_paciente = input("CPF do paciente: ")
    crm_medico = input("CRM do médico: ")
    data = input("Data (AAAA-MM-DD): ")
    hora = input("Hora (HH:MM:SS): ")
    
    sql_inserir_agendamento = "INSERT INTO agendamentos (cpf_paciente, crm_medico, data, hora) VALUES (%s, %s, %s, %s)"
    insert_agendamento = (cpf_paciente, crm_medico, data, hora)
    bancodedados_mysql.insertNaTabela(conexao, sql_inserir_agendamento, insert_agendamento)
    print("Consulta agendada com sucesso!")

def visualizar_agendamentos():
    sql_listar_agendamentos = "SELECT * FROM agendamentos"
    agendamentos = bancodedados_mysql.listarBancoDados(conexao, sql_listar_agendamentos)
    
    for agendamento in agendamentos:
        print(f"ID: {agendamento[0]}, CPF Paciente: {agendamento[1]}, CRM Médico: {agendamento[2]}, Data: {agendamento[3]}, Hora: {agendamento[4]}")

def cancelar_agendamento():
    id_agendamento = input("ID do agendamento a ser cancelado: ")
    sql_remover_agendamento = "DELETE FROM agendamentos WHERE id = %s"
    sql_remover_agendamento_id = (id_agendamento,)
    bancodedados_mysql.excluirDadosTabela(conexao, sql_remover_agendamento, sql_remover_agendamento_id)
    print("Agendamento cancelado com sucesso!")

def registrar_procedimento():
    cpf_paciente = input("CPF do paciente: ")
    crm_medico = input("CRM do médico: ")
    descricao = input("Descrição do procedimento: ")
    data = input("Data (AAAA-MM-DD): ")
    
    sql_inserir_procedimento = "INSERT INTO procedimentos (cpf_paciente, crm_medico, descricao, data) VALUES (%s, %s, %s, %s)"
    insert_procedimento = (cpf_paciente, crm_medico, descricao, data)
    bancodedados_mysql.insertNaTabela(conexao, sql_inserir_procedimento, insert_procedimento)
    print("Procedimento registrado com sucesso!")

def visualizar_procedimentos():
    sql_listar_procedimentos = "SELECT * FROM procedimentos"
    procedimentos = bancodedados_mysql.listarBancoDados(conexao, sql_listar_procedimentos)
    
    for procedimento in procedimentos:
        print(f"ID: {procedimento[0]}, CPF Paciente: {procedimento[1]}, CRM Médico: {procedimento[2]}, Descrição: {procedimento[3]}, Data: {procedimento[4]}")

def personalizado(txt, itens, *chamadas):
    print()
    print('-=-' * 15)
    print(txt.center(45))
    print('-=-' * 15)
    print()
    for c in range(0, itens):
        print(f'{c +1} - {chamadas[c]}')


def menu():
    while True:
        personalizado("Sistema Gerenciamento - Hospital ABC", 12, "Adicionar Novo Paciente", "Adicionar Novo Medico", 
                      "Pesquisar Paciente por CPF", "Pesquisar Medico por CRM", "Excluir Paciente pelo CPF",
                      "Excluir Medico pelo CRM","Agendar Consulta","Visualizar Agendamentos","Cancelar Agendamento",
                      "Registrar Procedimento Médico","Visualizar Procedimentos Médicos", "Sair do Sistema")
        

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
            agendar_consulta()
        elif opcao == '8':
            visualizar_agendamentos()
        elif opcao == '9':
            cancelar_agendamento()
        elif opcao == '10':
            registrar_procedimento()
        elif opcao == '11':
            visualizar_procedimentos()
        elif opcao == '12':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
