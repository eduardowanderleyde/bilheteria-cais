import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from database import DatabaseManager
from datetime import datetime, date
import os
from sistema_politicas import SistemaPoliticas
from venda_multipla import VendaMultipla
from nota_fiscal import NotaFiscal

# Configuração do tema
ctk.set_appearance_mode("dark")  # "system", "dark", "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class BilheteriaApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sistema de Bilheteria - Museu")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Inicializar banco de dados e sistema de políticas
        self.db = DatabaseManager()
        self.sistema_politicas = SistemaPoliticas()
        
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
        
        # Aba de Pagamentos
        self.notebook.add("Pagamentos")
        self.configurar_aba_pagamentos()
        
        # Aba de Dados
        self.notebook.add("Dados Salvos")
        self.configurar_aba_dados()
        
        # Aba de Informações do Banco
        self.notebook.add("Informações do Banco")
        self.configurar_aba_banco()
    
    def configurar_aba_vendas(self):
        """Configura a aba de vendas"""
        vendas_frame = self.notebook.tab("Vendas")
        
        # Sistema de navegação
        nav_frame = ctk.CTkFrame(vendas_frame)
        nav_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        # Botões de navegação
        venda_btn = ctk.CTkButton(nav_frame, text="💰 Nova Venda", 
                                 command=lambda: self.mostrar_tela_venda("nova"),
                                 width=150, height=35)
        venda_btn.pack(side="left", padx=5, pady=10)
        
        multipla_btn = ctk.CTkButton(nav_frame, text="👥 Venda Múltipla", 
                                    command=lambda: self.mostrar_tela_venda("multipla"),
                                    width=150, height=35)
        multipla_btn.pack(side="left", padx=5, pady=10)
        
        nota_btn = ctk.CTkButton(nav_frame, text="🧾 Ver Nota", 
                                command=lambda: self.mostrar_tela_venda("nota"),
                                width=150, height=35)
        nota_btn.pack(side="right", padx=5, pady=10)
        
        # Frame principal de vendas
        self.venda_main_frame = ctk.CTkFrame(vendas_frame)
        self.venda_main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Inicializar com venda simples
        self.mostrar_tela_venda("nova")
    
    def mostrar_tela_venda(self, tipo):
        """Mostra diferentes telas de venda"""
        # Limpar frame principal
        for widget in self.venda_main_frame.winfo_children():
            widget.destroy()
        
        if tipo == "nova":
            self.configurar_venda_simples()
        elif tipo == "multipla":
            self.configurar_venda_multipla()
        elif tipo == "nota":
            self.configurar_visualizacao_nota()
    
    def configurar_venda_multipla(self):
        """Configura tela de venda múltipla"""
        # Limpar frame principal
        for widget in self.venda_main_frame.winfo_children():
            widget.destroy()
        
        # Inicializar sistema de venda múltipla
        self.venda_multipla = VendaMultipla(
            self.venda_main_frame, 
            self.db, 
            self.atualizar_dados_callback
        )
    
    def configurar_visualizacao_nota(self):
        """Configura tela de visualização de nota"""
        # Limpar frame principal
        for widget in self.venda_main_frame.winfo_children():
            widget.destroy()
        
        # Inicializar sistema de nota fiscal
        self.nota_fiscal = NotaFiscal(self.venda_main_frame, self.db)
    
    def atualizar_dados_callback(self):
        """Callback para atualizar dados após venda"""
        if hasattr(self, 'atualizar_dados'):
            self.atualizar_dados()
    
    def configurar_venda_simples(self):
        """Configura tela de venda simples"""
        # Título
        titulo = ctk.CTkLabel(self.venda_main_frame, text="Venda Individual", 
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
        
        # Frame para justificativa (inicialmente oculto)
        self.justificativa_frame = ctk.CTkFrame(form_frame)
        self.justificativa_frame.pack(fill="x", padx=20, pady=(10, 10))
        
        self.justificativa_label = ctk.CTkLabel(self.justificativa_frame, text="Justificativa:", 
                                              font=ctk.CTkFont(size=12))
        self.justificativa_label.pack(anchor="w", pady=(10, 5), padx=20)
        
        self.justificativa_entry = ctk.CTkEntry(self.justificativa_frame, placeholder_text="Ex: Estudante, Idoso 65 anos, Professor rede pública...",
                                               width=400, height=35)
        self.justificativa_entry.pack(pady=(0, 10), padx=20)
        
        # Inicialmente oculto
        self.justificativa_frame.pack_forget()
        
        # Seção de pagamento
        ctk.CTkLabel(form_frame, text="💳 Forma de Pagamento:", 
                    font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(20, 5), padx=20)
        
        self.forma_pagamento = ctk.CTkSegmentedButton(form_frame, 
                                                     values=["Dinheiro", "Cartão Débito", "Cartão Crédito", "PIX", "Gratuito"],
                                                     width=400, height=35)
        self.forma_pagamento.pack(pady=(0, 10), padx=20)
        self.forma_pagamento.set("Dinheiro")
        
        # Frame para valores de pagamento
        self.pagamento_frame = ctk.CTkFrame(form_frame)
        self.pagamento_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Valor pago e troco
        valores_frame = ctk.CTkFrame(self.pagamento_frame)
        valores_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(valores_frame, text="Valor Pago:", 
                    font=ctk.CTkFont(size=12)).pack(side="left", padx=5, pady=5)
        self.valor_pago_entry = ctk.CTkEntry(valores_frame, placeholder_text="0.00",
                                            width=100, height=30)
        self.valor_pago_entry.pack(side="left", padx=5, pady=5)
        
        ctk.CTkLabel(valores_frame, text="Troco:", 
                    font=ctk.CTkFont(size=12)).pack(side="left", padx=(20, 5), pady=5)
        self.troco_label = ctk.CTkLabel(valores_frame, text="R$ 0,00", 
                                       font=ctk.CTkFont(size=12, weight="bold"),
                                       text_color="green")
        self.troco_label.pack(side="left", padx=5, pady=5)
        
        # Botão para calcular troco
        calc_troco_btn = ctk.CTkButton(valores_frame, text="Calcular Troco", 
                                      command=self.calcular_troco,
                                      width=120, height=30)
        calc_troco_btn.pack(side="right", padx=5, pady=5)
        
        # Bind para calcular troco automaticamente e mostrar justificativa
        self.valor_pago_entry.bind('<KeyRelease>', lambda e: self.calcular_troco())
        self.forma_pagamento.bind('<Button-1>', lambda e: self.atualizar_campos_pagamento())
        self.tipo_ingresso.bind('<Button-1>', lambda e: self.atualizar_campo_justificativa())
        
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
        
        # Informações sobre preços e políticas
        info_frame = ctk.CTkFrame(vendas_frame)
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Criar frame expansível para políticas
        politicas_frame = ctk.CTkFrame(info_frame)
        politicas_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(politicas_frame, text="📋 Políticas de Ingresso - Cais do Sertão", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        # Preços básicos
        precos_text = "💰 Preços: Inteira R$ 10,00 | Meia R$ 5,00 | Gratuito (conforme política)"
        ctk.CTkLabel(politicas_frame, text=precos_text, 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(pady=5)
        
        # Políticas de meia entrada
        meia_text = ("🎫 MEIA ENTRADA (R$ 5,00):\n"
                    "• Pessoas com idade a partir de 60 anos\n"
                    "• Pessoas com deficiência e 1 acompanhante\n"
                    "• Estudantes de escolas e universidades particulares\n"
                    "• Professores de escolas e universidades particulares")
        ctk.CTkLabel(politicas_frame, text=meia_text, 
                    font=ctk.CTkFont(size=11),
                    text_color="blue").pack(anchor="w", padx=10, pady=5)
        
        # Políticas de gratuidade
        gratuito_text = ("🎁 GRATUIDADE:\n"
                        "• Às terças-feiras: gratuito para TODOS\n"
                        "• Demais dias:\n"
                        "  - Crianças com até 5 anos de idade\n"
                        "  - Alunos e professores de rede pública de ensino\n"
                        "  - Funcionários de museus\n"
                        "  - Guias de turismo\n"
                        "⚠️ Mediante comprovação")
        ctk.CTkLabel(politicas_frame, text=gratuito_text, 
                    font=ctk.CTkFont(size=11),
                    text_color="green").pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(politicas_frame, text="💡 Todos os campos do cliente são opcionais", 
                    font=ctk.CTkFont(size=11),
                    text_color="gray").pack(pady=(5, 10))
    
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
        
        # Usar sistema inteligente de políticas
        justificativa_input = self.justificativa_entry.get().strip() or ""
        
        # Aplicar políticas automaticamente
        resultado_politica = self.sistema_politicas.aplicar_desconto_automatico({
            'justificativa': justificativa_input,
            'data_venda': datetime.now()
        })
        
        tipo_ingresso = resultado_politica['tipo']
        preco = resultado_politica['preco']
        justificativa = resultado_politica['justificativa']
        
        # Obter dados do cliente (opcionais)
        nome = self.nome_entry.get().strip() or None
        estado = self.estado_entry.get().strip() or None
        cidade = self.cidade_entry.get().strip() or None
        
        # Obter dados de pagamento
        forma_pagamento = self.forma_pagamento.get()
        valor_pago_str = self.valor_pago_entry.get().strip()
        
        # Validar pagamento
        if forma_pagamento == "Gratuito":
            valor_pago = 0.0
            troco = 0.0
        else:
            if not valor_pago_str:
                messagebox.showerror("Erro", "Informe o valor pago!")
                return
            
            try:
                valor_pago = float(valor_pago_str.replace(',', '.'))
                if valor_pago < preco:
                    messagebox.showerror("Erro", f"Valor pago (R$ {valor_pago:.2f}) é menor que o preço (R$ {preco:.2f})!")
                    return
                troco = valor_pago - preco
            except ValueError:
                messagebox.showerror("Erro", "Valor pago inválido! Use apenas números.")
                return
        
        try:
            # Registrar no banco de dados
            venda_id = self.db.registrar_venda(
                tipo_ingresso=tipo_ingresso,
                preco=preco,
                forma_pagamento=forma_pagamento,
                valor_pago=valor_pago,
                troco=troco,
                nome_cliente=nome,
                estado=estado,
                cidade=cidade,
                observacoes=justificativa
            )
            
            # Confirmar sucesso
            mensagem = f"Venda registrada com sucesso!\nID: {venda_id}\nTipo: {tipo_ingresso}\nPreço: R$ {preco:.2f}"
            mensagem += f"\nPagamento: {forma_pagamento}"
            if valor_pago > 0:
                mensagem += f"\nValor pago: R$ {valor_pago:.2f}"
                if troco > 0:
                    mensagem += f"\nTroco: R$ {troco:.2f}"
            if nome:
                mensagem += f"\nCliente: {nome}"
            if justificativa:
                mensagem += f"\nJustificativa: {justificativa}"
            
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
        self.justificativa_frame.pack_forget()  # Ocultar campo de justificativa
        self.justificativa_entry.delete(0, tk.END)
        self.forma_pagamento.set("Dinheiro")
        self.valor_pago_entry.delete(0, tk.END)
        self.troco_label.configure(text="R$ 0,00", text_color="white")
        self.nome_entry.delete(0, tk.END)
        self.estado_entry.delete(0, tk.END)
        self.cidade_entry.delete(0, tk.END)
    
    def calcular_troco(self):
        """Calcula o troco baseado no preço do ingresso e valor pago"""
        try:
            # Obter preço do ingresso
            tipo = self.tipo_ingresso.get()
            if "Inteira" in tipo:
                preco = 10.0
            elif "Meia" in tipo:
                preco = 5.0
            else:  # Gratuito
                preco = 0.0
            
            # Obter valor pago
            valor_pago_str = self.valor_pago_entry.get().strip()
            if not valor_pago_str:
                self.troco_label.configure(text="R$ 0,00")
                return
            
            valor_pago = float(valor_pago_str.replace(',', '.'))
            troco = max(0, valor_pago - preco)
            
            # Atualizar label do troco
            self.troco_label.configure(text=f"R$ {troco:.2f}")
            
            # Mudar cor baseada no troco
            if troco > 0:
                self.troco_label.configure(text_color="green")
            else:
                self.troco_label.configure(text_color="white")
                
        except ValueError:
            self.troco_label.configure(text="R$ 0,00", text_color="red")
    
    def atualizar_campos_pagamento(self):
        """Atualiza os campos de pagamento baseado na forma selecionada"""
        forma = self.forma_pagamento.get()
        
        if forma == "Gratuito":
            self.valor_pago_entry.delete(0, tk.END)
            self.valor_pago_entry.insert(0, "0.00")
            self.troco_label.configure(text="R$ 0,00", text_color="green")
        else:
            self.troco_label.configure(text="R$ 0,00", text_color="white")
    
    def atualizar_campo_justificativa(self):
        """Mostra ou oculta o campo de justificativa baseado no tipo de ingresso"""
        tipo = self.tipo_ingresso.get()
        
        # Aguardar um pouco para o valor ser atualizado
        self.root.after(100, lambda: self._atualizar_justificativa_delayed())
    
    def _atualizar_justificativa_delayed(self):
        """Atualiza o campo de justificativa após um pequeno delay"""
        tipo = self.tipo_ingresso.get()
        
        if "Meia" in tipo or "Gratuito" in tipo:
            # Mostrar campo de justificativa
            self.justificativa_frame.pack(fill="x", padx=20, pady=(10, 10))
            
            # Atualizar placeholder baseado no tipo
            if "Meia" in tipo:
                placeholder = "Ex: Estudante, Idoso 60+, Professor particular, Pessoa com deficiência..."
                self.justificativa_label.configure(text="Justificativa para Meia Entrada:")
            else:  # Gratuito
                placeholder = "Ex: Terça-feira, Criança até 5 anos, Professor rede pública, Funcionário museu..."
                self.justificativa_label.configure(text="Justificativa para Gratuidade:")
            
            self.justificativa_entry.configure(placeholder_text=placeholder)
        else:
            # Ocultar campo de justificativa
            self.justificativa_frame.pack_forget()
            self.justificativa_entry.delete(0, tk.END)
    
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
    
    def configurar_aba_pagamentos(self):
        """Configura a aba de relatórios de pagamento"""
        pagamentos_frame = self.notebook.tab("Pagamentos")
        
        # Frame de filtros
        filtros_frame = ctk.CTkFrame(pagamentos_frame)
        filtros_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(filtros_frame, text="💳 Relatórios de Pagamento", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        # Filtros de data
        datas_frame = ctk.CTkFrame(filtros_frame)
        datas_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(datas_frame, text="Data Início:").pack(side="left", padx=10, pady=10)
        self.data_inicio_pag = ctk.CTkEntry(datas_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.data_inicio_pag.pack(side="left", padx=(0, 20), pady=10)
        
        ctk.CTkLabel(datas_frame, text="Data Fim:").pack(side="left", padx=10, pady=10)
        self.data_fim_pag = ctk.CTkEntry(datas_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.data_fim_pag.pack(side="left", padx=(0, 20), pady=10)
        
        gerar_pag_btn = ctk.CTkButton(datas_frame, text="📊 Gerar Relatório", 
                                     command=self.gerar_relatorio_pagamentos,
                                     width=150)
        gerar_pag_btn.pack(side="right", padx=20, pady=10)
        
        # Frame de resultados
        self.resultados_pag_frame = ctk.CTkScrollableFrame(pagamentos_frame)
        self.resultados_pag_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Mostrar relatório inicial
        self.gerar_relatorio_pagamentos()
    
    def gerar_relatorio_pagamentos(self):
        """Gera relatório de pagamentos"""
        # Limpar resultados anteriores
        for widget in self.resultados_pag_frame.winfo_children():
            widget.destroy()
        
        # Obter datas
        data_inicio = self.data_inicio_pag.get().strip()
        data_fim = self.data_fim_pag.get().strip()
        
        try:
            # Gerar relatório
            if data_inicio and data_fim:
                relatorio = self.db.obter_relatorio_pagamentos(data_inicio, data_fim)
                titulo = f"Relatório de Pagamentos: {data_inicio} a {data_fim}"
            else:
                relatorio = self.db.obter_relatorio_pagamentos()
                titulo = "Relatório de Pagamentos - Geral"
            
            # Título
            ctk.CTkLabel(self.resultados_pag_frame, text=titulo, 
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 20))
            
            if not relatorio:
                ctk.CTkLabel(self.resultados_pag_frame, text="Nenhuma venda encontrada no período.", 
                            font=ctk.CTkFont(size=14)).pack(pady=20)
                return
            
            # Cabeçalho da tabela
            header_frame = ctk.CTkFrame(self.resultados_pag_frame)
            header_frame.pack(fill="x", pady=(0, 10), padx=10)
            
            headers = ["Forma de Pagamento", "Quantidade", "Total Vendido", "Total Recebido", "Total Troco"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(header_frame, text=header, 
                                   font=ctk.CTkFont(size=14, weight="bold"))
                label.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
                header_frame.grid_columnconfigure(i, weight=1)
            
            # Dados do relatório
            total_vendido = 0
            total_recebido = 0
            total_troco = 0
            
            for item in relatorio:
                forma, quantidade, vendido, recebido, troco = item
                total_vendido += vendido
                total_recebido += recebido
                total_troco += troco
                
                item_frame = ctk.CTkFrame(self.resultados_pag_frame)
                item_frame.pack(fill="x", pady=2, padx=10)
                
                # Forma de pagamento
                pagamento_label = ctk.CTkLabel(item_frame, text=forma, font=ctk.CTkFont(size=12))
                if forma == "Gratuito":
                    pagamento_label.configure(text_color="green")
                elif "Cartão" in forma:
                    pagamento_label.configure(text_color="blue")
                pagamento_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")
                
                # Quantidade
                ctk.CTkLabel(item_frame, text=str(quantidade), font=ctk.CTkFont(size=12)).grid(
                    row=0, column=1, padx=10, pady=8, sticky="w")
                
                # Total vendido
                ctk.CTkLabel(item_frame, text=f"R$ {vendido:.2f}", font=ctk.CTkFont(size=12)).grid(
                    row=0, column=2, padx=10, pady=8, sticky="w")
                
                # Total recebido
                ctk.CTkLabel(item_frame, text=f"R$ {recebido:.2f}", font=ctk.CTkFont(size=12)).grid(
                    row=0, column=3, padx=10, pady=8, sticky="w")
                
                # Total troco
                ctk.CTkLabel(item_frame, text=f"R$ {troco:.2f}", font=ctk.CTkFont(size=12)).grid(
                    row=0, column=4, padx=10, pady=8, sticky="w")
                
                item_frame.grid_columnconfigure(0, weight=1)
                item_frame.grid_columnconfigure(1, weight=1)
                item_frame.grid_columnconfigure(2, weight=1)
                item_frame.grid_columnconfigure(3, weight=1)
                item_frame.grid_columnconfigure(4, weight=1)
            
            # Totais gerais
            total_frame = ctk.CTkFrame(self.resultados_pag_frame)
            total_frame.pack(fill="x", pady=(20, 10), padx=10)
            
            # Métricas principais
            metricas_frame = ctk.CTkFrame(total_frame)
            metricas_frame.pack(fill="x", padx=10, pady=10)
            
            col1, col2, col3 = ctk.CTkFrame(metricas_frame), ctk.CTkFrame(metricas_frame), ctk.CTkFrame(metricas_frame)
            col1.pack(side="left", fill="x", expand=True, padx=5, pady=10)
            col2.pack(side="left", fill="x", expand=True, padx=5, pady=10)
            col3.pack(side="left", fill="x", expand=True, padx=5, pady=10)
            
            ctk.CTkLabel(col1, text="Total Vendido", font=ctk.CTkFont(size=12)).pack(pady=(10, 5))
            ctk.CTkLabel(col1, text=f"R$ {total_vendido:.2f}", 
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0, 10))
            
            ctk.CTkLabel(col2, text="Total Recebido", font=ctk.CTkFont(size=12)).pack(pady=(10, 5))
            ctk.CTkLabel(col2, text=f"R$ {total_recebido:.2f}", 
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0, 10))
            
            ctk.CTkLabel(col3, text="Total Troco", font=ctk.CTkFont(size=12)).pack(pady=(10, 5))
            ctk.CTkLabel(col3, text=f"R$ {total_troco:.2f}", 
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(0, 10))
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório de pagamentos: {str(e)}")
    
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
            
            headers = ["ID", "Data/Hora", "Tipo", "Preço", "Pagamento", "Valor Pago", "Troco", "Cliente", "Estado", "Cidade", "Justificativa"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(header_frame, text=header, 
                                   font=ctk.CTkFont(size=12, weight="bold"))
                label.grid(row=0, column=i, padx=5, pady=8, sticky="ew")
                header_frame.grid_columnconfigure(i, weight=1)
            
            # Dados das vendas
            for venda in vendas:
                venda_id, data_venda, tipo, preco, forma_pagamento, valor_pago, troco, nome, estado, cidade, observacoes = venda
                
                item_frame = ctk.CTkFrame(self.dados_frame)
                item_frame.pack(fill="x", pady=2, padx=10)
                
                # ID
                ctk.CTkLabel(item_frame, text=str(venda_id), font=ctk.CTkFont(size=11)).grid(
                    row=0, column=0, padx=5, pady=6, sticky="w")
                
                # Data/Hora
                data_formatada = datetime.strptime(data_venda, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
                ctk.CTkLabel(item_frame, text=data_formatada, font=ctk.CTkFont(size=11)).grid(
                    row=0, column=1, padx=5, pady=6, sticky="w")
                
                # Tipo com cor
                tipo_label = ctk.CTkLabel(item_frame, text=tipo, font=ctk.CTkFont(size=11))
                if tipo == "Inteira":
                    tipo_label.configure(text_color="white")
                elif tipo == "Meia":
                    tipo_label.configure(text_color="blue")
                else:  # Gratuito
                    tipo_label.configure(text_color="green")
                tipo_label.grid(row=0, column=2, padx=5, pady=6, sticky="w")
                
                # Preço
                preco_text = f"R$ {preco:.2f}" if preco > 0 else "GRATUITO"
                preco_label = ctk.CTkLabel(item_frame, text=preco_text, font=ctk.CTkFont(size=11))
                if preco == 0:
                    preco_label.configure(text_color="green")
                preco_label.grid(row=0, column=3, padx=5, pady=6, sticky="w")
                
                # Forma de Pagamento
                pagamento_label = ctk.CTkLabel(item_frame, text=forma_pagamento, font=ctk.CTkFont(size=11))
                if forma_pagamento == "Gratuito":
                    pagamento_label.configure(text_color="green")
                elif "Cartão" in forma_pagamento:
                    pagamento_label.configure(text_color="blue")
                pagamento_label.grid(row=0, column=4, padx=5, pady=6, sticky="w")
                
                # Valor Pago
                valor_pago_text = f"R$ {valor_pago:.2f}" if valor_pago > 0 else "GRATUITO"
                ctk.CTkLabel(item_frame, text=valor_pago_text, font=ctk.CTkFont(size=11)).grid(
                    row=0, column=5, padx=5, pady=6, sticky="w")
                
                # Troco
                troco_text = f"R$ {troco:.2f}" if troco > 0 else "R$ 0,00"
                troco_label = ctk.CTkLabel(item_frame, text=troco_text, font=ctk.CTkFont(size=11))
                if troco > 0:
                    troco_label.configure(text_color="green")
                troco_label.grid(row=0, column=6, padx=5, pady=6, sticky="w")
                
                # Cliente
                cliente_text = nome or "-"
                ctk.CTkLabel(item_frame, text=cliente_text, font=ctk.CTkFont(size=11)).grid(
                    row=0, column=7, padx=5, pady=6, sticky="w")
                
                # Estado
                ctk.CTkLabel(item_frame, text=estado or "-", font=ctk.CTkFont(size=11)).grid(
                    row=0, column=8, padx=5, pady=6, sticky="w")
                
                # Cidade
                ctk.CTkLabel(item_frame, text=cidade or "-", font=ctk.CTkFont(size=11)).grid(
                    row=0, column=9, padx=5, pady=6, sticky="w")
                
                # Justificativa
                justificativa_text = observacoes or "-"
                if justificativa_text != "-":
                    justificativa_label = ctk.CTkLabel(item_frame, text=justificativa_text, 
                                                     font=ctk.CTkFont(size=10),
                                                     text_color="orange")
                else:
                    justificativa_label = ctk.CTkLabel(item_frame, text=justificativa_text, 
                                                     font=ctk.CTkFont(size=11))
                justificativa_label.grid(row=0, column=10, padx=5, pady=6, sticky="w")
                
                # Configurar colunas
                for i in range(11):
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
    
    def configurar_aba_banco(self):
        """Configura a aba de informações do banco"""
        banco_frame = self.notebook.tab("Informações do Banco")
        
        # Frame principal com scroll
        main_scroll = ctk.CTkScrollableFrame(banco_frame)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(main_scroll, text="📊 Informações Detalhadas do Banco de Dados", 
                             font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=(0, 20))
        
        # Estatísticas gerais
        stats_frame = ctk.CTkFrame(main_scroll)
        stats_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        ctk.CTkLabel(stats_frame, text="📈 Estatísticas Gerais", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        try:
            stats = self.db.obter_estatisticas_gerais()
            
            # Métricas principais
            metricas_frame = ctk.CTkFrame(stats_frame)
            metricas_frame.pack(fill="x", padx=20, pady=10)
            
            # Métricas em layout horizontal
            
            # Total de vendas
            vendas_frame = ctk.CTkFrame(metricas_frame)
            vendas_frame.pack(side="left", fill="x", expand=True, padx=5, pady=10)
            ctk.CTkLabel(vendas_frame, text="Total de Vendas", font=ctk.CTkFont(size=12)).pack(pady=(10, 5))
            ctk.CTkLabel(vendas_frame, text=str(stats['total_vendas']), 
                        font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 10))
            
            # Total arrecadado
            arrecadado_frame = ctk.CTkFrame(metricas_frame)
            arrecadado_frame.pack(side="left", fill="x", expand=True, padx=5, pady=10)
            ctk.CTkLabel(arrecadado_frame, text="Total Arrecadado", font=ctk.CTkFont(size=12)).pack(pady=(10, 5))
            ctk.CTkLabel(arrecadado_frame, text=f"R$ {stats['total_arrecadado']:.2f}", 
                        font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 10))
            
            # Média por venda
            media_frame = ctk.CTkFrame(metricas_frame)
            media_frame.pack(side="left", fill="x", expand=True, padx=5, pady=10)
            ctk.CTkLabel(media_frame, text="Média por Venda", font=ctk.CTkFont(size=12)).pack(pady=(10, 5))
            media = stats['total_arrecadado'] / stats['total_vendas'] if stats['total_vendas'] > 0 else 0
            ctk.CTkLabel(media_frame, text=f"R$ {media:.2f}", 
                        font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 10))
            
        except Exception as e:
            ctk.CTkLabel(stats_frame, text=f"Erro ao carregar estatísticas: {str(e)}", 
                        font=ctk.CTkFont(size=12), text_color="red").pack(pady=10)
        
        # Vendas por tipo
        tipo_frame = ctk.CTkFrame(main_scroll)
        tipo_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        ctk.CTkLabel(tipo_frame, text="🎫 Vendas por Tipo de Ingresso", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        try:
            vendas_por_tipo = self.db.obter_estatisticas_gerais()['vendas_por_tipo']
            
            if vendas_por_tipo:
                for tipo, quantidade, total in vendas_por_tipo:
                    item_frame = ctk.CTkFrame(tipo_frame)
                    item_frame.pack(fill="x", padx=20, pady=5)
                    
                    col1, col2, col3 = ctk.CTkFrame(item_frame), ctk.CTkFrame(item_frame), ctk.CTkFrame(item_frame)
                    col1.pack(side="left", fill="x", expand=True, padx=5, pady=10)
                    col2.pack(side="left", fill="x", expand=True, padx=5, pady=10)
                    col3.pack(side="left", fill="x", expand=True, padx=5, pady=10)
                    
                    ctk.CTkLabel(col1, text=f"Tipo: {tipo}", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
                    ctk.CTkLabel(col2, text=f"Quantidade: {quantidade}", font=ctk.CTkFont(size=12)).pack(pady=5)
                    ctk.CTkLabel(col3, text=f"Total: R$ {total:.2f}", font=ctk.CTkFont(size=12)).pack(pady=5)
            else:
                ctk.CTkLabel(tipo_frame, text="Nenhuma venda registrada ainda.", 
                            font=ctk.CTkFont(size=12)).pack(pady=20)
                
        except Exception as e:
            ctk.CTkLabel(tipo_frame, text=f"Erro ao carregar vendas por tipo: {str(e)}", 
                        font=ctk.CTkFont(size=12), text_color="red").pack(pady=10)
        
        # Informações do arquivo do banco
        arquivo_frame = ctk.CTkFrame(main_scroll)
        arquivo_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        ctk.CTkLabel(arquivo_frame, text="💾 Informações do Arquivo de Banco", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        try:
            import os
            db_path = "bilheteria.db"
            if os.path.exists(db_path):
                file_size = os.path.getsize(db_path)
                file_size_mb = file_size / (1024 * 1024)
                
                info_text = f"""
📁 Localização: {os.path.abspath(db_path)}
📏 Tamanho: {file_size_mb:.2f} MB ({file_size:,} bytes)
🗄️ Tipo: SQLite Database
🔒 Segurança: Arquivo local, sem acesso externo
💾 Backup: Copie o arquivo bilheteria.db para backup
                """
                
                ctk.CTkLabel(arquivo_frame, text=info_text, 
                            font=ctk.CTkFont(size=11),
                            justify="left").pack(padx=20, pady=10)
                
                # Botão de backup
                backup_btn = ctk.CTkButton(arquivo_frame, text="📋 Copiar Caminho do Arquivo", 
                                          command=lambda: self.copiar_caminho_banco(),
                                          width=200)
                backup_btn.pack(pady=(0, 15))
            else:
                ctk.CTkLabel(arquivo_frame, text="Arquivo de banco não encontrado.", 
                            font=ctk.CTkFont(size=12), text_color="red").pack(pady=20)
                
        except Exception as e:
            ctk.CTkLabel(arquivo_frame, text=f"Erro ao obter informações do arquivo: {str(e)}", 
                        font=ctk.CTkFont(size=12), text_color="red").pack(pady=10)
        
        # Informações técnicas
        tech_frame = ctk.CTkFrame(main_scroll)
        tech_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        ctk.CTkLabel(tech_frame, text="🔧 Informações Técnicas", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        
        tech_text = """
🗃️ Banco de Dados: SQLite 3
📊 Capacidade: Até 281 TB (suficiente para milhões de vendas)
⚡ Performance: Otimizado para consultas locais
🔄 Transações: ACID compliant (seguro e confiável)
📱 Compatibilidade: Funciona em qualquer sistema operacional
🔐 Segurança: Dados locais, sem exposição externa
💾 Backup: Arquivo único (.db) - fácil backup
        """
        
        ctk.CTkLabel(tech_frame, text=tech_text, 
                    font=ctk.CTkFont(size=11),
                    justify="left").pack(padx=20, pady=10)
    
    def copiar_caminho_banco(self):
        """Copia o caminho do arquivo de banco para área de transferência"""
        import os
        import pyperclip
        
        try:
            db_path = os.path.abspath("bilheteria.db")
            pyperclip.copy(db_path)
            messagebox.showinfo("Sucesso", f"Caminho copiado para área de transferência:\n{db_path}")
        except ImportError:
            messagebox.showinfo("Caminho do Banco", f"Caminho do arquivo de banco:\n{os.path.abspath('bilheteria.db')}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar caminho: {str(e)}")
    
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
