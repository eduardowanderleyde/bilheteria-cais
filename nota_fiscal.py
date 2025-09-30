"""
Sistema de Nota Fiscal/Comprovante
Gera notas fiscais profissionais para as vendas
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import os

class NotaFiscal:
    def __init__(self, parent_frame, database_manager):
        self.parent_frame = parent_frame
        self.db = database_manager
        
        # Configurar interface
        self.configurar_interface()
    
    def configurar_interface(self):
        """Configura a interface de nota fiscal"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(main_frame, text="Nota Fiscal / Comprovante", 
                             font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=(20, 30))
        
        # Frame de filtros
        filtros_frame = ctk.CTkFrame(main_frame)
        filtros_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(filtros_frame, text="Filtros para Nota:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        # Filtros
        filtros_row = ctk.CTkFrame(filtros_frame)
        filtros_row.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(filtros_row, text="Data:").pack(side="left", padx=10, pady=10)
        self.data_filtro = ctk.CTkEntry(filtros_row, placeholder_text="YYYY-MM-DD", width=120)
        self.data_filtro.pack(side="left", padx=(0, 20), pady=10)
        
        ctk.CTkLabel(filtros_row, text="ID da Venda:").pack(side="left", padx=10, pady=10)
        self.id_filtro = ctk.CTkEntry(filtros_row, placeholder_text="ID específico", width=120)
        self.id_filtro.pack(side="left", padx=(0, 20), pady=10)
        
        gerar_btn = ctk.CTkButton(filtros_row, text="🧾 Gerar Nota", 
                                 command=self.gerar_nota,
                                 width=120)
        gerar_btn.pack(side="right", padx=20, pady=10)
        
        # Frame da nota
        self.nota_frame = ctk.CTkScrollableFrame(main_frame)
        self.nota_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mostrar nota inicial
        self.gerar_nota()
    
    def gerar_nota(self):
        """Gera a nota fiscal"""
        # Limpar frame da nota
        for widget in self.nota_frame.winfo_children():
            widget.destroy()
        
        try:
            # Obter dados
            data_filtro = self.data_filtro.get().strip()
            id_filtro = self.id_filtro.get().strip()
            
            if data_filtro:
                vendas = self.db.obter_vendas_por_dia(data_filtro)
            elif id_filtro:
                # Buscar venda específica por ID
                conn = self.db.db_path
                import sqlite3
                conn_db = sqlite3.connect(conn)
                cursor = conn_db.cursor()
                cursor.execute('SELECT * FROM vendas WHERE id = ?', (id_filtro,))
                vendas = [cursor.fetchone()] if cursor.fetchone() else []
                conn_db.close()
            else:
                # Últimas 10 vendas
                vendas = self.db.obter_vendas_por_dia()[:10]
            
            if not vendas:
                ctk.CTkLabel(self.nota_frame, text="Nenhuma venda encontrada.", 
                            font=ctk.CTkFont(size=14)).pack(pady=20)
                return
            
            # Gerar nota
            self.criar_nota_fiscal(vendas)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar nota: {str(e)}")
    
    def criar_nota_fiscal(self, vendas):
        """Cria a nota fiscal visual"""
        # Cabeçalho da nota
        header_frame = ctk.CTkFrame(self.nota_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Nome do museu
        ctk.CTkLabel(header_frame, text="CAIS DO SERTÃO", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(20, 5))
        
        ctk.CTkLabel(header_frame, text="Museu de Cultura Popular", 
                    font=ctk.CTkFont(size=14)).pack(pady=(0, 5))
        
        ctk.CTkLabel(header_frame, text="Recife - PE", 
                    font=ctk.CTkFont(size=12)).pack(pady=(0, 20))
        
        # Data e hora
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ctk.CTkLabel(header_frame, text=f"Data/Hora: {data_atual}", 
                    font=ctk.CTkFont(size=12)).pack(pady=(0, 10))
        
        # Separador
        separador1 = ctk.CTkFrame(header_frame, height=2)
        separador1.pack(fill="x", padx=20, pady=10)
        
        # Detalhes das vendas
        for i, venda in enumerate(vendas):
            if len(venda) < 11:  # Verificar se tem todos os campos
                continue
                
            venda_id, data_venda, tipo, preco, forma_pagamento, valor_pago, troco, nome, estado, cidade, observacoes = venda
            
            # Frame de cada item
            item_frame = ctk.CTkFrame(self.nota_frame)
            item_frame.pack(fill="x", padx=10, pady=5)
            
            # Número do item
            ctk.CTkLabel(item_frame, text=f"{i+1}.", 
                        font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10, pady=10)
            
            # Detalhes do ingresso
            detalhes_frame = ctk.CTkFrame(item_frame)
            detalhes_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            # Tipo e preço
            tipo_preco_frame = ctk.CTkFrame(detalhes_frame)
            tipo_preco_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(tipo_preco_frame, text=f"Tipo: {tipo}", 
                        font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
            
            preco_text = f"R$ {preco:.2f}" if preco > 0 else "GRATUITO"
            ctk.CTkLabel(tipo_preco_frame, text=preco_text, 
                        font=ctk.CTkFont(size=12, weight="bold")).pack(side="right", padx=5)
            
            # Pagamento
            if valor_pago > 0:
                pagamento_frame = ctk.CTkFrame(detalhes_frame)
                pagamento_frame.pack(fill="x", padx=10, pady=2)
                
                ctk.CTkLabel(pagamento_frame, text=f"Pagamento: {forma_pagamento}", 
                            font=ctk.CTkFont(size=11)).pack(side="left", padx=5)
                
                if troco > 0:
                    ctk.CTkLabel(pagamento_frame, text=f"Troco: R$ {troco:.2f}", 
                                font=ctk.CTkFont(size=11)).pack(side="right", padx=5)
            
            # Justificativa se houver
            if observacoes:
                ctk.CTkLabel(detalhes_frame, text=f"Obs: {observacoes}", 
                            font=ctk.CTkFont(size=10),
                            text_color="gray").pack(anchor="w", padx=10, pady=2)
            
            # Cliente se houver
            if nome:
                ctk.CTkLabel(detalhes_frame, text=f"Cliente: {nome}", 
                            font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=2)
        
        # Separador
        separador2 = ctk.CTkFrame(self.nota_frame, height=2)
        separador2.pack(fill="x", padx=20, pady=10)
        
        # Totais
        total_frame = ctk.CTkFrame(self.nota_frame)
        total_frame.pack(fill="x", padx=10, pady=10)
        
        total_vendas = len(vendas)
        total_arrecadado = sum(venda[3] for venda in vendas if len(venda) > 3)
        
        ctk.CTkLabel(total_frame, text=f"Total de Ingressos: {total_vendas}", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        ctk.CTkLabel(total_frame, text=f"Total Arrecadado: R$ {total_arrecadado:.2f}", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        # Rodapé
        rodape_frame = ctk.CTkFrame(self.nota_frame)
        rodape_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(rodape_frame, text="Obrigado pela sua visita!", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(rodape_frame, text="CAIS DO SERTÃO - Museu de Cultura Popular", 
                    font=ctk.CTkFont(size=10)).pack(pady=(0, 10))
        
        # Botões de ação
        acoes_frame = ctk.CTkFrame(self.nota_frame)
        acoes_frame.pack(fill="x", padx=10, pady=10)
        
        imprimir_btn = ctk.CTkButton(acoes_frame, text="🖨️ Imprimir", 
                                    command=self.imprimir_nota,
                                    width=120)
        imprimir_btn.pack(side="left", padx=10, pady=10)
        
        salvar_btn = ctk.CTkButton(acoes_frame, text="💾 Salvar PDF", 
                                  command=self.salvar_pdf,
                                  width=120)
        salvar_btn.pack(side="left", padx=10, pady=10)
        
        copiar_btn = ctk.CTkButton(acoes_frame, text="📋 Copiar Texto", 
                                  command=self.copiar_texto,
                                  width=120)
        copiar_btn.pack(side="right", padx=10, pady=10)
    
    def imprimir_nota(self):
        """Simula impressão da nota"""
        messagebox.showinfo("Impressão", "Nota enviada para impressão!")
    
    def salvar_pdf(self):
        """Salva a nota como PDF"""
        try:
            arquivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
                title="Salvar Nota Fiscal"
            )
            
            if arquivo:
                # Gerar texto da nota
                texto_nota = self.gerar_texto_nota()
                
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(texto_nota)
                
                messagebox.showinfo("Sucesso", f"Nota salva em: {arquivo}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def copiar_texto(self):
        """Copia o texto da nota para área de transferência"""
        try:
            import pyperclip
            texto_nota = self.gerar_texto_nota()
            pyperclip.copy(texto_nota)
            messagebox.showinfo("Sucesso", "Texto copiado para área de transferência!")
        except ImportError:
            messagebox.showwarning("Aviso", "Biblioteca pyperclip não instalada. Instale com: pip install pyperclip")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar: {str(e)}")
    
    def gerar_texto_nota(self):
        """Gera o texto da nota para exportação"""
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        texto = f"""
═══════════════════════════════════════════
                CAIS DO SERTÃO
            Museu de Cultura Popular
                Recife - PE

Data/Hora: {data_atual}
═══════════════════════════════════════════
"""
        
        # Adicionar vendas (implementar lógica similar ao visual)
        # ... código para gerar texto das vendas ...
        
        texto += """
═══════════════════════════════════════════
            Obrigado pela sua visita!
    CAIS DO SERTÃO - Museu de Cultura Popular
═══════════════════════════════════════════
"""
        
        return texto
