import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3

login_ = 'admin'
senha_ = 'admin'

def banco(): # Cria o banco de dados
    try:
        conn = sqlite3.connect('funcionarios.bd')
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE if not exists funcionarios(
            nome TEXT NOT NULL,
            idade INTEGER,
            email TEXT,
            telefone TEXT NOT NULL,
            salario TEXT NOT NULL)""")
            conn.commit()
    except Exception:
        box(1, 'Erro', 'Problema ao Criar Banco de Dados')

def box(ms, nome, msg): # Messagebox de erros,atenção,sim e não
    if ms == 1:
        messagebox.showerror(title=f'{nome}', message=f'{msg}')
    elif ms == 2:
        messagebox.showinfo(title=f'{nome}', message=f'{msg}')
    elif ms == 3:
        m = messagebox.askyesno(title=f'{nome}', message=f'{msg}')
        return m

def funcionario(): # Pega as dados do banco
    try:
        conn = sqlite3.connect('funcionarios.bd')
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT *,oid FROM funcionarios;""")
            return cursor.fetchall()
    except Exception:
        box(1, 'Arquivo', 'Erro ao Abrir Arquivos')

def update(): # Tela de atualizar os cadastro já existentes
    global nome_update, idade_update, email_update, telefone_update, salario_update, janela_update

    janela_update = ctk.CTkToplevel()
    janela_update.transient(janela)
    janela_update.title('Atualizar Cadastro')
    janela_update.state('zoomed')

    texto_cadastro = ctk.CTkLabel(janela_update, width=200, height=50, text='Atualize os Dados', font=('Gotham', 20))
    texto_cadastro.pack(padx=10, pady=10)

    nome_update = ctk.CTkEntry(janela_update, placeholder_text='Nome',width=200, height=30, textvariable=lin1, corner_radius=10)
    nome_update.pack(padx=10, pady=10)

    idade_update = ctk.CTkEntry(janela_update, placeholder_text='Idade',width=200, height=30, textvariable=lin2, corner_radius=10)
    idade_update.pack(padx=10, pady=10)

    email_update = ctk.CTkEntry(janela_update, placeholder_text='Email',width=200, height=30, textvariable=lin3, corner_radius=10)
    email_update.pack(padx=10, pady=10)

    telefone_update = ctk.CTkEntry(janela_update, placeholder_text='Telefone',width=200, height=30, textvariable=lin4, corner_radius=10)
    telefone_update.pack(padx=10, pady=10)

    salario_update = ctk.CTkEntry(janela_update, placeholder_text='Salário',width=200, height=30, textvariable=lin5, corner_radius=10)
    salario_update.pack(padx=10, pady=10)

    botao_atualiza = ctk.CTkButton(janela_update, text='Atualizar', command=gravar)
    botao_atualiza.pack(padx=10, pady=10)

    botao_voltar = ctk.CTkButton(janela_update, text='Voltar', command=janela_update.destroy)
    botao_voltar.pack()

def atualiza_add(): # Pega o click selecionado para atualizar
    global lin1, lin2, lin3, lin4, lin5, valor1

    try:
        del_dados = tabela_ver.focus()
        del_dic = tabela_ver.item(del_dados)
        atualiza = del_dic['values']
        valor1 = atualiza[5]

        lin1 = ctk.StringVar(janela_ver, value=atualiza[0])
        lin2 = ctk.StringVar(janela_ver, value=atualiza[1])
        lin3 = ctk.StringVar(janela_ver, value=atualiza[2])
        lin4 = ctk.StringVar(janela_ver, value=atualiza[3])
        lin5 = ctk.StringVar(janela_ver, value=atualiza[4])
        update()
        janela_ver.destroy()
    except Exception:
        box(1, 'Erro', 'Erro Atualizar Add')

def gravar():# Atualiza no banco os dados
    try:
        conn = sqlite3.connect('funcionarios.bd')
        with conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE funcionarios SET nome=?,idade=?,email=?,telefone=?,salario=?WHERE oid=?''',
                (nome_update.get(),
                idade_update.get(),
                email_update.get(),
                telefone_update.get(),
                salario_update.get(),
                valor1,))
            conn.commit()
            box(2, 'Atualização', 'Cadastro Atualizado com Sucesso')
            janela_update.destroy()
    except Exception:
        box(1, 'Erro', 'Erro ao fazer Atualização')

def deletecadastro():
    m = box(3, 'Deletar', 'Voçê Deseja Deletar o Cadastro Selecionado??')
    if m == True:
        try:
            del_dados = tabela_ver.focus()
            del_dic = tabela_ver.item(del_dados)
            del_list = del_dic['values']
            valor1 = del_list[5]
            conn = sqlite3.connect('funcionarios.bd')
            with conn:
                cursor = conn.cursor()
                cursor.execute('''DELETE FROM funcionarios
                WHERE oid=?''', (valor1,))
                conn.commit()
        except Exception:
            box(1, 'Delete', 'Problema ao DELETAR CADASTRO')
        finally:
            janela_ver.destroy()

def cadastrar():  # Melhorar para não aceitar campos vasio
    try:
        conn = sqlite3.connect('funcionarios.bd')
        with conn:
            cursor = conn.cursor()
            cursor.execute(' INSERT INTO funcionarios VALUES (:nome,:idade,:email,:telefone,:salario)',
            {'nome': nome_add.get(),
            'idade': idade_add.get(),
            'email': email_add.get(),
            'telefone': telefone_add.get(),
            'salario': salario_add.get()})
            conn.commit()
            janela_add.destroy()
            box(2, 'Novo Cadastro', 'Cadastro Realizado com Sucesso')
    except Exception:
        box(1, 'Novo Cadastro', 'PROBLEMA AO CADASTRAR')

def menu():
    janela.title('Cadastro de Funcionários')
    janela.state('zoomed')

    botao_add = ctk.CTkButton(janela, text='Novo Cadastro', command=add)
    botao_add.pack(padx=10, pady=10)

    botao_ver_cadastros = ctk.CTkButton(janela, text='Ver Cadastros',command=vercadastro)
    botao_ver_cadastros.pack(padx=10, pady=10)

    botao_sair = ctk.CTkButton(janela, text='Sair', command=janela.destroy)
    botao_sair.pack(padx=10, pady=10)

def add():
    global nome_add, idade_add, email_add, telefone_add, salario_add, janela_add

    janela_add = ctk.CTkToplevel()
    janela_add.transient(janela)
    janela_add.title('Cadastro de Colaboradores')
    janela_add.state('zoomed')

    texto_cadastro = ctk.CTkLabel(janela_add, width=200, height=50, text='Insira aos Dados', font=('Gotham', 20))
    texto_cadastro.pack(padx=10, pady=10)

    nome_add = ctk.CTkEntry(janela_add, placeholder_text='Nome', width=200, height=30, corner_radius=10)
    nome_add.pack(padx=10, pady=10)

    idade_add = ctk.CTkEntry(janela_add, placeholder_text='Idade', width=200, height=30, corner_radius=10)
    idade_add.pack(padx=10, pady=10)

    email_add = ctk.CTkEntry(janela_add, placeholder_text='Email', width=200, height=30, corner_radius=10)
    email_add.pack(padx=10, pady=10)

    telefone_add = ctk.CTkEntry(janela_add, placeholder_text='Telefone', width=200, height=30, corner_radius=10)
    telefone_add.pack(padx=10, pady=10)

    salario_add = ctk.CTkEntry(janela_add, placeholder_text='Salário', width=200, height=30, corner_radius=10)
    salario_add.pack(padx=10, pady=10)

    cadastrar_add = ctk.CTkButton(janela_add, text='Cadastrar', command=cadastrar,)
    cadastrar_add.pack(padx=10, pady=10)

    voltar_add = ctk.CTkButton(janela_add, text='Voltar', command=janela_add.destroy)
    voltar_add.pack()

def vercadastro():
    global tabela_ver, janela_ver

    janela_ver = ctk.CTkToplevel()
    janela_ver.transient(janela)
    janela_ver.title('Ver Cadastro de Colaboradores')
    janela_ver.state('zoomed')

    lista_cabeca = ['Nome', 'Idade', 'E-mail', 'Telefone', 'Salário', 'ID']

    tabela_ver = ttk.Treeview(janela_ver, selectmode='extended', columns=lista_cabeca, show='headings')
    tabela_ver.place(width=500, height=300, x=30, y=30)

    barra_vertical = ttk.Scrollbar(janela_ver, orient='vertical', command=tabela_ver.yview)
    barra_vertical.place(width=20, height=300, x=525, y=30)

    tabela_ver.configure(yscrollcommand=barra_vertical.set)

    h = [80, 50, 80, 80, 50, 20]
    n = 0

    for col in lista_cabeca:
        tabela_ver.heading(col, text=col.title(), anchor='center')
        tabela_ver.column(col, width=h[n], anchor='center')
        n += 1

    for item in funcionario():
        tabela_ver.insert('', 'end', values=item)

    atualiza_ver = ctk.CTkButton(janela_ver, text='Atualizar', command=atualiza_add)
    atualiza_ver.place(x=560, y=30)

    deletar_ver = ctk.CTkButton(janela_ver, text='Deletar', command=deletecadastro)
    deletar_ver.place(x=560, y=80)

    voltar_ver = ctk.CTkButton(janela_ver, text='Voltar', command=janela_ver.destroy)
    voltar_ver.place(x=560, y=130)

def logar(): # Verifica se login e senha estão corretos
    user = entry_1
    senh = senha_1
    try:
        if user.get() == login_ and senh.get() == senha_:
            menu()
            tk.destroy()
        else:
            box(1, 'Login', 'Erro nos Dados Preenchidos ')
    except Exception:
        box(1, 'Login', 'ERRO')

def login():
    global entry_1, senha_1, tk

    janela.withdraw()
    tk = ctk.CTkToplevel()
    tk.title('Programa Cadastro ')
    tk.geometry('300x400+437+291')

    texto = ctk.CTkLabel(tk, text='Login', font=('Gotham', 36))
    texto.pack(padx=60, pady=60)

    entry_1 = ctk.CTkEntry(master=tk, placeholder_text='Usuario',width=200, height=40, corner_radius=10)
    entry_1.pack(padx=10, pady=10)

    senha_1 = ctk.CTkEntry(tk, show='*', placeholder_text='Senha', width=200, height=40, corner_radius=10)
    senha_1.pack(padx=10, pady=10)

    botao_login = ctk.CTkButton(tk, text='Logar', width=100, height=40, command=logar)
    botao_login.pack(padx=25, pady=25)

janela = ctk.CTk()
login()
banco()
janela.mainloop()
