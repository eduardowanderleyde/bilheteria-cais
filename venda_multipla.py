"""
Sistema de Venda Múltipla Rápida
Para atender grupos rapidamente
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from sistema_politicas import SistemaPoliticas

class VendaMultipla:
    def __init__(self, parent_frame, database_manager, callback_venda_registrada):
        self.parent_frame = parent_frame
        self.db = database_manager
        self.callback = callback_venda_registrada
        self.sistema_politicas = SistemaPoliticas()
        
        # Lista de vendas atuais
        self.vendas_atual = []
        
        # Configurar interface
        self.configurar_interface()
    
    def configurar_interface(self):
        """Configura a interface de venda múltipla"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(main_frame, text="Venda Múltipla - Grupo", 
                             font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=(20, 30))
        
        # Frame de entrada rápida
        entrada_frame = ctk.CTkFrame(main_frame)
        entrada_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(entrada_frame, text="Entrada Rápida:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        # Campo de entrada
        entrada_row = ctk.CTkFrame(entrada_frame)
        entrada_row.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(entrada_row, text="Descrição:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        
        self.entrada_entry = ctk.CTkEntry(entrada_row, placeholder_text="Ex: 3 inteiras, 2 meias, 1 criança 4 anos",
                                         width=400, height=35, font=ctk.CTkFont(size=14))
        self.entrada_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        self.entrada_entry.bind('<Return>', lambda e: self.processar_entrada())
        
        adicionar_btn = ctk.CTkButton(entrada_row, text="➕ Adicionar", 
                                     command=self.processar_entrada,
                                     width=120, height=35)
        adicionar_btn.pack(side="right", padx=10)
        
        # Exemplos de uso
        exemplos_frame = ctk.CTkFrame(entrada_frame)
        exemplos_frame.pack(fill="x", padx=20, pady=10)
        
        exemplos_text = """
💡 Exemplos de entrada:
• "3 inteiras" → 3 ingressos inteiros
• "2 meias, 1 idoso 65 anos" → 2 meias + 1 meia (idoso)
• "1 criança 4 anos, 2 inteiras" → 1 gratuito + 2 inteiras
• "1 professor rede pública, 1 estudante" → 1 gratuito + 1 meia
• "1 terça-feira" → 1 gratuito (se for terça)
        """
        
        ctk.CTkLabel(exemplos_frame, text=exemplos_text, 
                    font=ctk.CTkFont(size=11),
                    text_color="gray").pack(pady=10)
        
        # Lista de vendas atuais
        lista_frame = ctk.CTkFrame(main_frame)
        lista_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(lista_frame, text="Vendas Adicionadas:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        # Frame scrollable para a lista
        self.lista_scroll = ctk.CTkScrollableFrame(lista_frame)
        self.lista_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame de totais e ações
        totais_frame = ctk.CTkFrame(main_frame)
        totais_frame.pack(fill="x", padx=20, pady=20)
        
        # Totais
        self.totais_label = ctk.CTkLabel(totais_frame, text="Total: 0 vendas | R$ 0,00", 
                                        font=ctk.CTkFont(size=16, weight="bold"))
        self.totais_label.pack(side="left", padx=20, pady=15)
        
        # Botões de ação
        acoes_frame = ctk.CTkFrame(totais_frame)
        acoes_frame.pack(side="right", padx=20, pady=15)
        
        limpar_btn = ctk.CTkButton(acoes_frame, text="🗑️ Limpar Tudo", 
                                  command=self.limpar_vendas,
                                  width=120, height=35)
        limpar_btn.pack(side="left", padx=5)
        
        finalizar_btn = ctk.CTkButton(acoes_frame, text="✅ Finalizar Venda", 
                                     command=self.finalizar_venda,
                                     width=150, height=35)
        finalizar_btn.pack(side="left", padx=5)
    
    def processar_entrada(self):
        """Processa a entrada do usuário e adiciona vendas"""
        entrada = self.entrada_entry.get().strip()
        if not entrada:
            return
        
        try:
            # Processar entrada usando sistema inteligente
            vendas_processadas = self.interpretar_entrada(entrada)
            
            # Adicionar à lista
            for venda in vendas_processadas:
                self.vendas_atual.append(venda)
            
            # Atualizar interface
            self.atualizar_lista()
            self.atualizar_totais()
            
            # Limpar entrada
            self.entrada_entry.delete(0, 'end')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar entrada: {str(e)}")
    
    def interpretar_entrada(self, entrada):
        """Interpreta a entrada do usuário e converte em vendas"""
        import re
        
        vendas = []
        entrada_lower = entrada.lower()
        
        # Padrões para detectar quantidades e tipos
        padroes = [
            (r'(\d+)\s*inteiras?', 'Inteira'),
            (r'(\d+)\s*meias?', 'Meia'),
            (r'(\d+)\s*crianças?\s*(\d+)\s*anos?', 'Criança'),
            (r'(\d+)\s*idosos?\s*(\d+)\s*anos?', 'Idoso'),
            (r'(\d+)\s*estudantes?', 'Estudante'),
            (r'(\d+)\s*professores?', 'Professor'),
            (r'(\d+)\s*terças?-feiras?', 'Terça-feira'),
            (r'(\d+)\s*gratuitos?', 'Gratuito')
        ]
        
        # Processar cada padrão encontrado
        for padrao, tipo_base in padroes:
            matches = re.finditer(padrao, entrada_lower)
            for match in matches:
                quantidade = int(match.group(1))
                
                if tipo_base == 'Criança':
                    idade = int(match.group(2))
                    for _ in range(quantidade):
                        resultado = self.sistema_politicas.aplicar_desconto_automatico({
                            'justificativa': f'Criança {idade} anos',
                            'idade': idade
                        })
                        vendas.append(resultado)
                
                elif tipo_base == 'Idoso':
                    idade = int(match.group(2))
                    for _ in range(quantidade):
                        resultado = self.sistema_politicas.aplicar_desconto_automatico({
                            'justificativa': f'Idoso {idade} anos',
                            'idade': idade
                        })
                        vendas.append(resultado)
                
                else:
                    for _ in range(quantidade):
                        resultado = self.sistema_politicas.aplicar_desconto_automatico({
                            'justificativa': tipo_base
                        })
                        vendas.append(resultado)
        
        # Se não encontrou padrões, tentar interpretação livre
        if not vendas:
            vendas = self.interpretacao_livre(entrada)
        
        return vendas
    
    def interpretacao_livre(self, entrada):
        """Interpretação livre da entrada"""
        vendas = []
        resultado = self.sistema_politicas.aplicar_desconto_automatico({
            'justificativa': entrada
        })
        vendas.append(resultado)
        return vendas
    
    def atualizar_lista(self):
        """Atualiza a lista de vendas na interface"""
        # Limpar lista atual
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
        
        # Adicionar cada venda
        for i, venda in enumerate(self.vendas_atual):
            item_frame = ctk.CTkFrame(self.lista_scroll)
            item_frame.pack(fill="x", padx=5, pady=2)
            
            # Tipo com cor
            tipo_label = ctk.CTkLabel(item_frame, text=venda['tipo'], 
                                     font=ctk.CTkFont(size=12, weight="bold"))
            if venda['tipo'] == "Inteira":
                tipo_label.configure(text_color="white")
            elif venda['tipo'] == "Meia":
                tipo_label.configure(text_color="blue")
            else:
                tipo_label.configure(text_color="green")
            tipo_label.pack(side="left", padx=10, pady=5)
            
            # Preço
            preco_text = f"R$ {venda['preco']:.2f}" if venda['preco'] > 0 else "GRATUITO"
            ctk.CTkLabel(item_frame, text=preco_text, font=ctk.CTkFont(size=12)).pack(side="left", padx=10, pady=5)
            
            # Justificativa
            ctk.CTkLabel(item_frame, text=venda['justificativa'], 
                        font=ctk.CTkFont(size=11),
                        text_color="gray").pack(side="left", padx=10, pady=5, fill="x", expand=True)
            
            # Botão remover
            remover_btn = ctk.CTkButton(item_frame, text="❌", 
                                       command=lambda idx=i: self.remover_venda(idx),
                                       width=30, height=25)
            remover_btn.pack(side="right", padx=5, pady=5)
    
    def remover_venda(self, index):
        """Remove uma venda da lista"""
        if 0 <= index < len(self.vendas_atual):
            self.vendas_atual.pop(index)
            self.atualizar_lista()
            self.atualizar_totais()
    
    def atualizar_totais(self):
        """Atualiza os totais da venda"""
        total_vendas = len(self.vendas_atual)
        total_valor = sum(venda['preco'] for venda in self.vendas_atual)
        
        self.totais_label.configure(text=f"Total: {total_vendas} vendas | R$ {total_valor:.2f}")
    
    def limpar_vendas(self):
        """Limpa todas as vendas"""
        self.vendas_atual = []
        self.atualizar_lista()
        self.atualizar_totais()
    
    def finalizar_venda(self):
        """Finaliza a venda múltipla"""
        if not self.vendas_atual:
            messagebox.showwarning("Aviso", "Nenhuma venda para finalizar!")
            return
        
        try:
            # Registrar cada venda no banco
            venda_ids = []
            for venda in self.vendas_atual:
                venda_id = self.db.registrar_venda(
                    tipo_ingresso=venda['tipo'],
                    preco=venda['preco'],
                    forma_pagamento="Dinheiro",  # Padrão para venda múltipla
                    valor_pago=venda['preco'],
                    troco=0,
                    observacoes=venda['justificativa']
                )
                venda_ids.append(venda_id)
            
            # Mostrar confirmação
            total_valor = sum(venda['preco'] for venda in self.vendas_atual)
            mensagem = f"Venda múltipla finalizada!\n\n"
            mensagem += f"Total: {len(self.vendas_atual)} ingressos\n"
            mensagem += f"Valor: R$ {total_valor:.2f}\n"
            mensagem += f"IDs: {', '.join(map(str, venda_ids))}"
            
            messagebox.showinfo("Sucesso", mensagem)
            
            # Limpar vendas
            self.limpar_vendas()
            
            # Callback para atualizar outras telas
            if self.callback:
                self.callback()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar venda: {str(e)}")
