"""
Script para gerar executável do Sistema de Bilheteria
Execute: python build_exe.py
"""

import subprocess
import sys
import os

def instalar_pyinstaller():
    """Instala o PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller já está instalado")
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado com sucesso!")

def gerar_executavel():
    """Gera o executável do sistema"""
    print("🔨 Gerando executável...")
    
    # Comando para gerar o executável
    comando = [
        "pyinstaller",
        "--onefile",                    # Um único arquivo .exe
        "--windowed",                   # Sem console (interface gráfica)
        "--name=Sistema_Bilheteria",    # Nome do executável
        "--icon=icon.ico",              # Ícone (opcional)
        "--add-data=database.py;.",     # Incluir arquivo do banco
        "--hidden-import=customtkinter",
        "--hidden-import=sqlite3",
        "--hidden-import=PIL",
        "main.py"
    ]
    
    # Remover parâmetros opcionais se arquivos não existirem
    if not os.path.exists("icon.ico"):
        comando = [cmd for cmd in comando if not cmd.startswith("--icon")]
    
    try:
        subprocess.run(comando, check=True)
        print("✅ Executável gerado com sucesso!")
        print("📁 Localização: dist/Sistema_Bilheteria.exe")
        
        # Criar pasta de distribuição
        if not os.path.exists("distribuicao"):
            os.makedirs("distribuicao")
        
        # Copiar executável para pasta de distribuição
        import shutil
        if os.path.exists("dist/Sistema_Bilheteria.exe"):
            shutil.copy2("dist/Sistema_Bilheteria.exe", "distribuicao/")
            print("📦 Executável copiado para pasta 'distribuicao/'")
        
        # Criar arquivo de instruções
        instrucoes = """
# Sistema de Bilheteria - Museu

## Como usar:

1. Execute o arquivo: Sistema_Bilheteria.exe
2. Login: funcionario1
3. Senha: 123456

## Funcionalidades:

- ✅ Registrar vendas de ingressos
- ✅ Ver relatórios de vendas
- ✅ Visualizar dados salvos
- ✅ Banco de dados local (SQLite)

## Preços:

- Inteira: R$ 10,00
- Meia: R$ 5,00
- Gratuito: Terças e idosos

## Observações:

- O banco de dados será criado automaticamente
- Todos os dados ficam salvos localmente
- Não precisa de internet para funcionar
- Sistema seguro e confiável

Para suporte, consulte o arquivo README.md
        """
        
        with open("distribuicao/INSTRUCOES.txt", "w", encoding="utf-8") as f:
            f.write(instrucoes)
        
        print("📋 Arquivo de instruções criado")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao gerar executável: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    print("🚀 Gerador de Executável - Sistema de Bilheteria")
    print("=" * 50)
    
    # Verificar se os arquivos necessários existem
    arquivos_necessarios = ["main.py", "database.py"]
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            return
    
    # Instalar PyInstaller
    instalar_pyinstaller()
    
    # Gerar executável
    if gerar_executavel():
        print("\n🎉 Processo concluído com sucesso!")
        print("📁 Verifique a pasta 'distribuicao/' para o executável final")
    else:
        print("\n❌ Erro no processo de geração")

if __name__ == "__main__":
    main()
