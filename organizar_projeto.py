"""
Script para organizar o projeto antes de publicar no GitHub
Remove arquivos desnecessários e prepara para commit
"""

import os
import shutil

def criar_gitignore():
    """Cria arquivo .gitignore"""
    content = """# Python
__pycache__/
*.pyc
.env
.venv
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
"""
    with open(".gitignore", "w") as f:
        f.write(content)
    print("✅ .gitignore criado!")

def criar_readme():
    """Cria README.md"""
    content = """# Trello Agente Completo 🚀

Sistema automatizado para gerenciamento do Trello usando Python.

## Funcionalidades

- Listar boards e listas
- Criar cards simples, com datas e labels
- Mover cards entre listas
- Adicionar checklists
- Gerar relatórios de progresso
- Buscar cards por palavra-chave
- Testes automatizados

## Instalação

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure suas credenciais no arquivo `.env`
4. Execute: `python trello_agente_completo.py`

## Como obter credenciais

Acesse: https://trello.com/power-ups/admin/

## Testes

Execute: `python teste_automatizado.py`

## Licença

MIT
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ README.md criado!")

def criar_env_example():
    """Cria .env.example"""
    content = """# Configuração do Trello API
TRELLO_API_KEY=sua_api_key_aqui
TRELLO_TOKEN=seu_token_aqui
"""
    with open(".env.example", "w") as f:
        f.write(content)
    print("✅ .env.example criado!")

def deletar_arquivos():
    """Deleta arquivos desnecessários"""
    arquivos = [
        "criar_tarefas_lote.py",
        "criar_tarefas_teste.py",
        "trello_manager_v2.py",
        "trello_manager.py",
        "test_credenciais.py",
        "test_detalhado.py",
    ]
    
    deletados = []
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            deletados.append(arquivo)
    
    return deletados

def deletar_pastas():
    """Deleta pastas de cache"""
    pastas = ["__pycache__"]
    deletadas = []
    
    for pasta in pastas:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
            deletadas.append(pasta)
    
    return deletadas

def main():
    print("="*50)
    print("ORGANIZANDO PROJETO PARA GITHUB")
    print("="*50)
    
    # Deletar arquivos desnecessários
    deletados = deletar_arquivos()
    if deletados:
        print("\nArquivos removidos:")
        for f in deletados:
            print(f"  - {f}")
    
    # Deletar pastas de cache
    pastas = deletar_pastas()
    if pastas:
        print("\nPastas removidas:")
        for p in pastas:
            print(f"  - {p}/")
    
    # Criar arquivos necessários
    print("\nCriando arquivos:")
    criar_gitignore()
    criar_readme()
    criar_env_example()
    
    print("\n" + "="*50)
    print("ARQUIVOS PARA COMMITAR:")
    print("="*50)
    arquivos_commit = [
        "trello_agente_completo.py",
        "teste_automatizado.py",
        "requirements.txt",
        ".gitignore",
        ".env.example",
        "README.md"
    ]
    
    for arquivo in arquivos_commit:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} (não encontrado)")
    
    print("\n" + "="*50)
    print("IMPORTANTE:")
    print("="*50)
    print("1. Verifique se .env está no .gitignore")
    print("2. NUNCA commite o arquivo .env")
    print("3. Execute: git status")
    print("4. Adicione os arquivos: git add .")
    print("5. Commit: git commit -m 'Primeira versao'")
    print("6. Push: git push origin main")

if __name__ == "__main__":
    main()