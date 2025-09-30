import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from database import DatabaseManager
from datetime import datetime, date
import os

# Configuração do tema
ctk.set_appearance_mode("dark")  # "system", "dark", "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class BilheteriaApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sistema de Bilheteria - Museu")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Inicializar banco de dados
        self.db = DatabaseManager()
        
        # Variáveis de controle
        self.usuario_logado = False
        
        # Configurar layout principal
        self.configurar_interface()
        
    def configurar_interface(self):
        """Configura a interface principal"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mostrar tela de login inicialmente
        self.mostrar_tela_login()
    
    def mostrar_tela_login(self):
        """Exibe a tela de login"""
        # Limpar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Frame de login
        login_frame = ctk.CTkFrame(self.main_frame)
        login_frame.pack(expand=True, fill="both")
        
        # Título
        titulo = ctk.CTkLabel(login_frame, text="Sistema de Bilheteria", 
                             font=ctk.CTkFont(size=28, weight="bold"))
        titulo.pack(pady=(50, 30))
        
        subtitulo = ctk.CTkLabel(login_frame, text="Museu", 
                                font=ctk.CTkFont(size=18))
        subtitulo.pack(pady=(0, 50))
        
        # Campos de login
        campos_frame = ctk.CTkFrame(login_frame)
        campos_frame.pack(pady=20, padx=50, fill="x")
        
        # Usuário
        ctk.CTkLabel(campos_frame, text="Usuário:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(20, 5), padx=20)
        self.usuario_entry = ctk.CTkEntry(campos_frame, placeholder_text="Digite seu usuário",
                                         width=300, height=35)
        self.usuario_entry.pack(pady=(0, 10), padx=20)
        
        # Senha
        ctk.CTkLabel(campos_frame, text="Senha:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(10, 5), padx=20)
        self.senha_entry = ctk.CTkEntry(campos_frame, placeholder_text="Digite sua senha",
                                       width=300, height=35, show="*")
        self.senha_entry.pack(pady=(0, 20), padx=20)
        
        # Botão de login
        login_btn = ctk.CTkButton(campos_frame, text="Entrar", 
                                 command=self.fazer_login,
                                 width=300, height=40,
                                 font=ctk.CTkFont(size=16))
        login_btn.pack(pady=(0, 20), padx=20)
        
        # Informações de login padrão
        info_frame = ctk.CTkFrame(login_frame)
        info_frame.pack(pady=20, padx=50, fill="x")
        
        info_text = "Usuário padrão: funcionario1\nSenha padrão: 123456"
        info_label = ctk.CTkLabel(info_frame, text=info_text, 
                                 font=ctk.CTkFont(size=12),
                                 text_color="gray")
        info_label.pack(pady=15)
        
        # Bind Enter para login
        self.root.bind('<Return>', lambda e: self.fazer_login())
        self.usuario_entry.focus()
    
    def fazer_login(self):
        """Realiza a autenticação do usuário"""
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return
        
        if self.db.autenticar_usuario(usuario, senha):
            self.usuario_logado = True
            self.mostrar_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
    
    def mostrar_tela_principal(self):
        """Exibe a tela principal do sistema"""
        # Limpar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Header com logout
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        titulo = ctk.CTkLabel(header_frame, text="Sistema de Bilheteria - Museu", 
                             font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(side="left", padx=20, pady=15)
        
        logout_btn = ctk.CTkButton(header_frame, text="Sair", 
                                  command=self.logout,
                                  width=100, height=35)
        logout_btn.pack(side="right", padx=20, pady=15)
        
        # Frame principal com abas
        self.notebook = ctk.CTkTabview(self.main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Aba de Vendas
        self.notebook.add("Vendas")
        self.configurar_aba_vendas()
        
        # Aba de Relatórios
        self.notebook.add("Relatórios")
        self.configurar_aba_relatorios()
        
        # Aba de Dados
        self.notebook.add("Dados Salvos")
        self.configurar_aba_dados()
    
    def configurar_aba_vendas(self):
        """Configura a aba de vendas"""
        vendas_frame = self.notebook.tab("Vendas")
        
        # Frame de venda
        venda_frame = ctk.CTkFrame(vendas_frame)
        venda_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(venda_frame, text="Registrar Venda", 
                             font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=(20, 30))
        
        # Formulário de venda
        form_frame = ctk.CTkFrame(venda_frame)
        form_frame.pack(pady=20, padx=50, fill="x")
        
        # Tipo de ingresso
        ctk.CTkLabel(form_frame, text="Tipo de Ingresso:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(20, 5), padx=20)
        
        self.tipo_ingresso = ctk.CTkSegmentedButton(form_frame, 
                                                   values=["Inteira (R$ 10,00)", "Meia (R$ 5,00)", "Gratuito"],
                                                   width=400, height=35)
        self.tipo_ingresso.pack(pady=(0, 10), padx=20)
        self.tipo_ingresso.set("Inteira (R$ 10,00)")
        
        # Informações do cliente (opcional)
        ctk.CTkLabel(form_frame, text="Informações do Cliente (Opcional):", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(20, 5), padx=20)
        
        # Nome
        ctk.CTkLabel(form_frame, text="Nome:", 
                    font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(10, 5), padx=20)
        self.nome_entry = ctk.CTkEntry(form_frame, placeholder_text="Nome do cliente",
                                      width=400, height=35)
        self.nome_entry.pack(pady=(0, 5), padx=20)
        
        # Estado
        ctk.CTkLabel(form_frame, text="Estado:", 
                    font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(10, 5), padx=20)
        self.estado_entry = ctk.CTkEntry(form_frame, placeholder_text="Estado",
                                        width=400, height=35)
        self.estado_entry.pack(pady=(0, 5), padx=20)
        
        # Cidade
        ctk.CTkLabel(form_frame, text="Cidade:", 
                    font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(10, 5), padx=20)
        self.cidade_entry = ctk.CTkEntry(form_frame, placeholder_text="Cidade",
                                        width=400, height=35)
        self.cidade_entry.pack(pady=(0, 20), padx=20)
        
        # Botões
        botoes_frame = ctk.CTkFrame(form_frame)
        botoes_frame.pack(pady=20, padx=20, fill="x")
        
        registrar_btn = ctk.CTkButton(botoes_frame, text="Registrar Venda", 
                                     command=self.registrar_venda,
                                     width=200, height=40,
                                     font=ctk.CTkFont(size=16))
        registrar_btn.pack(side="left", padx=(0, 10))
        
        limpar_btn = ctk.CTkButton(botoes_frame, text="Limpar", 
                                  command=self.limpar_formulario,
                                  width=200, height=40,
                                  font=ctk.CTkFont(size=16))
        limpar_btn.pack(side="left")
        
        # Informações sobre preços
        info_frame = ctk.CTkFrame(vendas_frame)
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        info_text = ("💡 Informações: Inteira R$ 10,00 | Meia R$ 5,00 | Gratuito (Terças-feiras e Idosos) | "
                    "Todos os campos do cliente são opcionais")
        info_label = ctk.CTkLabel(info_frame, text=info_text, 
                                 font=ctk.CTkFont(size=12),
                                 text_color="gray")
        info_label.pack(pady=15)
    
    def configurar_aba_relatorios(self):
        """Configura a aba de relatórios"""
        relatorios_frame = self.notebook.tab("Relatórios")
        
        # Frame de filtros
        filtros_frame = ctk.CTkFrame(relatorios_frame)
        filtros_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(filtros_frame, text="Filtros de Relatório", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        # Filtros de data
        datas_frame = ctk.CTkFrame(filtros_frame)
        datas_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(datas_frame, text="Data Início:").pack(side="left", padx=10, pady=10)
        self.data_inicio = ctk.CTkEntry(datas_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.data_inicio.pack(side="left", padx=(0, 20), pady=10)
        
        ctk.CTkLabel(datas_frame, text="Data Fim:").pack(side="left", padx=10, pady=10)
        self.data_fim = ctk.CTkEntry(datas_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.data_fim.pack(side="left", padx=(0, 20), pady=10)
        
        gerar_btn = ctk.CTkButton(datas_frame, text="Gerar Relatório", 
                                 command=self.gerar_relatorio,
                                 width=150)
        gerar_btn.pack(side="right", padx=20, pady=10)
        
        # Frame de resultados
        self.resultados_frame = ctk.CTkScrollableFrame(relatorios_frame)
        self.resultados_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Mostrar relatório inicial
        self.gerar_relatorio()
    
    def configurar_aba_dados(self):
        """Configura a aba de dados salvos"""
        dados_frame = self.notebook.tab("Dados Salvos")
        
        # Frame de controles
        controles_frame = ctk.CTkFrame(dados_frame)
        controles_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(controles_frame, text="Visualizar Dados Salvos", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        # Filtros
        filtros_frame = ctk.CTkFrame(controles_frame)
        filtros_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(filtros_frame, text="Filtrar por data:").pack(side="left", padx=10, pady=10)
        self.data_filtro = ctk.CTkEntry(filtros_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.data_filtro.pack(side="left", padx=(0, 20), pady=10)
        
        filtrar_btn = ctk.CTkButton(filtros_frame, text="Filtrar", 
                                   command=self.filtrar_dados,
                                   width=100)
        filtrar_btn.pack(side="left", padx=(0, 20), pady=10)
        
        atualizar_btn = ctk.CTkButton(filtros_frame, text="Atualizar Tudo", 
                                     command=self.atualizar_dados,
                                     width=120)
        atualizar_btn.pack(side="right", padx=20, pady=10)
        
        # Frame de dados
        self.dados_frame = ctk.CTkScrollableFrame(dados_frame)
        self.dados_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Mostrar dados iniciais
        self.atualizar_dados()
    
    def registrar_venda(self):
        """Registra uma nova venda"""
        tipo = self.tipo_ingresso.get()
        
        if not tipo:
            messagebox.showerror("Erro", "Selecione um tipo de ingresso!")
            return
        
        # Determinar preço baseado no tipo
        if "Inteira" in tipo:
            preco = 10.0
            tipo_ingresso = "Inteira"
        elif "Meia" in tipo:
            preco = 5.0
            tipo_ingresso = "Meia"
        else:  # Gratuito
            preco = 0.0
            tipo_ingresso = "Gratuito"
        
        # Obter dados do cliente (opcionais)
        nome = self.nome_entry.get().strip() or None
        estado = self.estado_entry.get().strip() or None
        cidade = self.cidade_entry.get().strip() or None
        
        try:
            # Registrar no banco de dados
            venda_id = self.db.registrar_venda(
                tipo_ingresso=tipo_ingresso,
                preco=preco,
                nome_cliente=nome,
                estado=estado,
                cidade=cidade
            )
            
            # Confirmar sucesso
            mensagem = f"Venda registrada com sucesso!\nID: {venda_id}\nTipo: {tipo_ingresso}\nPreço: R$ {preco:.2f}"
            if nome:
                mensagem += f"\nCliente: {nome}"
            
            messagebox.showinfo("Sucesso", mensagem)
            
            # Limpar formulário
            self.limpar_formulario()
            
            # Atualizar dados se estiver na aba de dados
            if self.notebook.get() == "Dados Salvos":
                self.atualizar_dados()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar venda: {str(e)}")
    
    def limpar_formulario(self):
        """Limpa o formulário de venda"""
        self.tipo_ingresso.set("Inteira (R$ 10,00)")
        self.nome_entry.delete(0, tk.END)
        self.estado_entry.delete(0, tk.END)
        self.cidade_entry.delete(0, tk.END)
    
    def gerar_relatorio(self):
        """Gera relatório de vendas"""
        # Limpar resultados anteriores
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        
        # Obter datas
        data_inicio = self.data_inicio.get().strip()
        data_fim = self.data_fim.get().strip()
        
        try:
            # Gerar relatório
            if data_inicio and data_fim:
                relatorio = self.db.obter_relatorio_vendas(data_inicio, data_fim)
                titulo = f"Relatório: {data_inicio} a {data_fim}"
            else:
                relatorio = self.db.obter_relatorio_vendas()
                titulo = "Relatório Geral"
            
            # Título
            ctk.CTkLabel(self.resultados_frame, text=titulo, 
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 20))
            
            if not relatorio:
                ctk.CTkLabel(self.resultados_frame, text="Nenhuma venda encontrada no período.", 
                            font=ctk.CTkFont(size=14)).pack(pady=20)
                return
            
            # Cabeçalho da tabela
            header_frame = ctk.CTkFrame(self.resultados_frame)
            header_frame.pack(fill="x", pady=(0, 10), padx=10)
            
            headers = ["Data", "Tipo", "Quantidade", "Total (R$)"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(header_frame, text=header, 
                                   font=ctk.CTkFont(size=14, weight="bold"))
                label.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
                header_frame.grid_columnconfigure(i, weight=1)
            
            # Dados do relatório
            total_geral = 0
            for item in relatorio:
                data, tipo, quantidade, total = item
                total_geral += total
                
                item_frame = ctk.CTkFrame(self.resultados_frame)
                item_frame.pack(fill="x", pady=2, padx=10)
                
                # Data
                ctk.CTkLabel(item_frame, text=data, font=ctk.CTkFont(size=12)).grid(
                    row=0, column=0, padx=10, pady=8, sticky="w")
                
                # Tipo
                ctk.CTkLabel(item_frame, text=tipo, font=ctk.CTkFont(size=12)).grid(
                    row=0, column=1, padx=10, pady=8, sticky="w")
                
                # Quantidade
                ctk.CTkLabel(item_frame, text=str(quantidade), font=ctk.CTkFont(size=12)).grid(
                    row=0, column=2, padx=10, pady=8, sticky="w")
                
                # Total
                ctk.CTkLabel(item_frame, text=f"R$ {total:.2f}", font=ctk.CTkFont(size=12)).grid(
                    row=0, column=3, padx=10, pady=8, sticky="w")
                
                item_frame.grid_columnconfigure(0, weight=1)
                item_frame.grid_columnconfigure(1, weight=1)
                item_frame.grid_columnconfigure(2, weight=1)
                item_frame.grid_columnconfigure(3, weight=1)
            
            # Total geral
            total_frame = ctk.CTkFrame(self.resultados_frame)
            total_frame.pack(fill="x", pady=(20, 10), padx=10)
            
            ctk.CTkLabel(total_frame, text=f"TOTAL GERAL: R$ {total_geral:.2f}", 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def filtrar_dados(self):
        """Filtra dados por data"""
        data_filtro = self.data_filtro.get().strip()
        self.atualizar_dados(data_filtro if data_filtro else None)
    
    def atualizar_dados(self, data_filtro=None):
        """Atualiza a exibição dos dados salvos"""
        # Limpar dados anteriores
        for widget in self.dados_frame.winfo_children():
            widget.destroy()
        
        try:
            # Obter vendas
            if data_filtro:
                vendas = self.db.obter_vendas_por_dia(data_filtro)
                titulo = f"Dados - {data_filtro}"
            else:
                vendas = self.db.obter_vendas_por_dia()
                titulo = "Todos os Dados Salvos"
            
            # Título
            ctk.CTkLabel(self.dados_frame, text=titulo, 
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 20))
            
            if not vendas:
                ctk.CTkLabel(self.dados_frame, text="Nenhuma venda encontrada.", 
                            font=ctk.CTkFont(size=14)).pack(pady=20)
                return
            
            # Cabeçalho da tabela
            header_frame = ctk.CTkFrame(self.dados_frame)
            header_frame.pack(fill="x", pady=(0, 10), padx=10)
            
            headers = ["ID", "Data/Hora", "Tipo", "Preço", "Cliente", "Estado", "Cidade"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(header_frame, text=header, 
                                   font=ctk.CTkFont(size=12, weight="bold"))
                label.grid(row=0, column=i, padx=5, pady=8, sticky="ew")
                header_frame.grid_columnconfigure(i, weight=1)
            
            # Dados das vendas
            for venda in vendas:
                venda_id, data_venda, tipo, preco, nome, estado, cidade, _ = venda
                
                item_frame = ctk.CTkFrame(self.dados_frame)
                item_frame.pack(fill="x", pady=2, padx=10)
                
                # ID
                ctk.CTkLabel(item_frame, text=str(venda_id), font=ctk.CTkFont(size=11)).grid(
                    row=0, column=0, padx=5, pady=6, sticky="w")
                
                # Data/Hora
                data_formatada = datetime.strptime(data_venda, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
                ctk.CTkLabel(item_frame, text=data_formatada, font=ctk.CTkFont(size=11)).grid(
                    row=0, column=1, padx=5, pady=6, sticky="w")
                
                # Tipo
                ctk.CTkLabel(item_frame, text=tipo, font=ctk.CTkFont(size=11)).grid(
                    row=0, column=2, padx=5, pady=6, sticky="w")
                
                # Preço
                ctk.CTkLabel(item_frame, text=f"R$ {preco:.2f}", font=ctk.CTkFont(size=11)).grid(
                    row=0, column=3, padx=5, pady=6, sticky="w")
                
                # Cliente
                ctk.CTkLabel(item_frame, text=nome or "-", font=ctk.CTkFont(size=11)).grid(
                    row=0, column=4, padx=5, pady=6, sticky="w")
                
                # Estado
                ctk.CTkLabel(item_frame, text=estado or "-", font=ctk.CTkFont(size=11)).grid(
                    row=0, column=5, padx=5, pady=6, sticky="w")
                
                # Cidade
                ctk.CTkLabel(item_frame, text=cidade or "-", font=ctk.CTkFont(size=11)).grid(
                    row=0, column=6, padx=5, pady=6, sticky="w")
                
                # Configurar colunas
                for i in range(7):
                    item_frame.grid_columnconfigure(i, weight=1)
            
            # Estatísticas gerais
            stats = self.db.obter_estatisticas_gerais()
            
            stats_frame = ctk.CTkFrame(self.dados_frame)
            stats_frame.pack(fill="x", pady=(20, 10), padx=10)
            
            stats_text = (f"📊 Estatísticas: {stats['total_vendas']} vendas | "
                         f"Total arrecadado: R$ {stats['total_arrecadado']:.2f}")
            ctk.CTkLabel(stats_frame, text=stats_text, 
                        font=ctk.CTkFont(size=14, weight="bold")).pack(pady=15)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
    
    def logout(self):
        """Realiza logout do usuário"""
        self.usuario_logado = False
        self.mostrar_tela_login()
    
    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BilheteriaApp()
    app.executar()
