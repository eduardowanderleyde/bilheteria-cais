import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self):
        self.db_path = "bilheteria.db"
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados e cria as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de vendas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo_ingresso TEXT NOT NULL,
                preco REAL NOT NULL,
                nome_cliente TEXT,
                estado TEXT,
                cidade TEXT,
                observacoes TEXT
            )
        ''')
        
        # Tabela de usuários (para autenticação)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        
        # Inserir usuário padrão se não existir
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE username = ?', ('funcionario1',))
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO usuarios (username, senha) VALUES (?, ?)', 
                          ('funcionario1', '123456'))
        
        conn.commit()
        conn.close()
    
    def autenticar_usuario(self, username, senha):
        """Autentica um usuário"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND senha = ?', 
                      (username, senha))
        resultado = cursor.fetchone()
        
        conn.close()
        return resultado is not None
    
    def registrar_venda(self, tipo_ingresso, preco, nome_cliente=None, estado=None, cidade=None, observacoes=None):
        """Registra uma nova venda"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO vendas (tipo_ingresso, preco, nome_cliente, estado, cidade, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (tipo_ingresso, preco, nome_cliente, estado, cidade, observacoes))
        
        conn.commit()
        venda_id = cursor.lastrowid
        conn.close()
        return venda_id
    
    def obter_vendas_por_dia(self, data=None):
        """Obtém vendas por dia específico ou todas as vendas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if data:
            cursor.execute('''
                SELECT * FROM vendas 
                WHERE DATE(data_venda) = DATE(?)
                ORDER BY data_venda DESC
            ''', (data,))
        else:
            cursor.execute('SELECT * FROM vendas ORDER BY data_venda DESC')
        
        vendas = cursor.fetchall()
        conn.close()
        return vendas
    
    def obter_relatorio_vendas(self, data_inicio=None, data_fim=None):
        """Obtém relatório de vendas por período"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if data_inicio and data_fim:
            cursor.execute('''
                SELECT 
                    DATE(data_venda) as data,
                    tipo_ingresso,
                    COUNT(*) as quantidade,
                    SUM(preco) as total
                FROM vendas 
                WHERE DATE(data_venda) BETWEEN ? AND ?
                GROUP BY DATE(data_venda), tipo_ingresso
                ORDER BY data DESC, tipo_ingresso
            ''', (data_inicio, data_fim))
        else:
            cursor.execute('''
                SELECT 
                    DATE(data_venda) as data,
                    tipo_ingresso,
                    COUNT(*) as quantidade,
                    SUM(preco) as total
                FROM vendas 
                GROUP BY DATE(data_venda), tipo_ingresso
                ORDER BY data DESC, tipo_ingresso
            ''')
        
        relatorio = cursor.fetchall()
        conn.close()
        return relatorio
    
    def obter_total_arrecadado(self, data_inicio=None, data_fim=None):
        """Obtém total arrecadado no período"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if data_inicio and data_fim:
            cursor.execute('''
                SELECT SUM(preco) as total
                FROM vendas 
                WHERE DATE(data_venda) BETWEEN ? AND ?
            ''', (data_inicio, data_fim))
        else:
            cursor.execute('SELECT SUM(preco) as total FROM vendas')
        
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado[0] else 0
    
    def obter_estatisticas_gerais(self):
        """Obtém estatísticas gerais do sistema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total de vendas
        cursor.execute('SELECT COUNT(*) FROM vendas')
        total_vendas = cursor.fetchone()[0]
        
        # Total arrecadado
        cursor.execute('SELECT SUM(preco) FROM vendas')
        total_arrecadado = cursor.fetchone()[0] or 0
        
        # Vendas por tipo
        cursor.execute('''
            SELECT tipo_ingresso, COUNT(*), SUM(preco)
            FROM vendas 
            GROUP BY tipo_ingresso
        ''')
        vendas_por_tipo = cursor.fetchall()
        
        conn.close()
        return {
            'total_vendas': total_vendas,
            'total_arrecadado': total_arrecadado,
            'vendas_por_tipo': vendas_por_tipo
        }
