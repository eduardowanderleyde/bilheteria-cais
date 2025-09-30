"""
Sistema Inteligente de Políticas de Ingresso - Cais do Sertão
Aplica automaticamente as regras de meia entrada e gratuidade
"""

from datetime import datetime, date
import re

class SistemaPoliticas:
    def __init__(self):
        self.politicas = {
            'gratuito_terca': True,
            'gratuito_criancas': True,
            'gratuito_rede_publica': True,
            'gratuito_funcionarios': True,
            'gratuito_guias': True,
            'meia_idosos': True,
            'meia_deficiencia': True,
            'meia_estudantes': True,
            'meia_professores': True
        }
    
    def determinar_tipo_ingresso(self, idade=None, justificativa="", data_venda=None):
        """
        Determina automaticamente o tipo de ingresso baseado nas políticas
        """
        if not data_venda:
            data_venda = datetime.now()
        
        # Verificar se é terça-feira (gratuito para todos)
        if data_venda.weekday() == 1:  # Terça-feira
            return "Gratuito", "Terça-feira - Gratuito para todos", 0.0
        
        # Verificar gratuidade por idade
        if idade is not None and idade <= 5:
            return "Gratuito", f"Criança {idade} anos - Gratuito até 5 anos", 0.0
        
        # Verificar gratuidade por justificativa
        justificativa_lower = justificativa.lower()
        
        if any(palavra in justificativa_lower for palavra in ['rede pública', 'rede publica', 'escola pública', 'escola publica']):
            return "Gratuito", "Professor/Aluno rede pública", 0.0
        
        if any(palavra in justificativa_lower for palavra in ['funcionário', 'funcionario', 'museu']):
            return "Gratuito", "Funcionário de museu", 0.0
        
        if any(palavra in justificativa_lower for palavra in ['guia', 'turismo']):
            return "Gratuito", "Guia de turismo", 0.0
        
        # Verificar meia entrada
        if idade is not None and idade >= 60:
            return "Meia", f"Idoso {idade} anos - Meia entrada 60+", 5.0
        
        if any(palavra in justificativa_lower for palavra in ['deficiência', 'deficiencia', 'pcd']):
            return "Meia", "Pessoa com deficiência + acompanhante", 5.0
        
        if any(palavra in justificativa_lower for palavra in ['estudante', 'universidade', 'escola particular']):
            return "Meia", "Estudante escola/universidade particular", 5.0
        
        if any(palavra in justificativa_lower for palavra in ['professor particular', 'prof particular']):
            return "Meia", "Professor escola/universidade particular", 5.0
        
        # Se não se enquadra em nenhuma política, é inteira
        return "Inteira", "Ingresso inteiro", 10.0
    
    def validar_idade(self, idade_str):
        """Valida e converte string de idade para número"""
        if not idade_str:
            return None
        
        try:
            idade = int(re.findall(r'\d+', idade_str)[0])
            return idade if 0 <= idade <= 120 else None
        except:
            return None
    
    def extrair_idade_justificativa(self, justificativa):
        """Extrai idade de uma justificativa como 'Idoso 65 anos'"""
        if not justificativa:
            return None, justificativa
        
        # Procurar padrões de idade
        padroes_idade = [
            r'(\d+)\s*anos?',
            r'idade\s*(\d+)',
            r'(\d+)\s*aninhos?'
        ]
        
        for padrao in padroes_idade:
            match = re.search(padrao, justificativa.lower())
            if match:
                idade = int(match.group(1))
                if 0 <= idade <= 120:
                    return idade, justificativa
        
        return None, justificativa
    
    def gerar_justificativa_automatica(self, tipo, detalhes, idade=None):
        """Gera justificativa automática baseada no tipo"""
        if tipo == "Gratuito":
            if "Terça" in detalhes:
                return "Terça-feira - Gratuito para todos"
            elif idade and idade <= 5:
                return f"Criança {idade} anos - Gratuito até 5 anos"
            else:
                return detalhes
        elif tipo == "Meia":
            if idade and idade >= 60:
                return f"Idoso {idade} anos - Meia entrada 60+"
            else:
                return detalhes
        else:
            return "Ingresso inteiro"
    
    def aplicar_desconto_automatico(self, entrada_dados):
        """
        Aplica desconto automático baseado nos dados fornecidos
        entrada_dados = {
            'justificativa': str,
            'idade': int (opcional),
            'data_venda': datetime (opcional)
        }
        """
        justificativa = entrada_dados.get('justificativa', '')
        idade = entrada_dados.get('idade')
        data_venda = entrada_dados.get('data_venda')
        
        # Se não tem idade, tentar extrair da justificativa
        if idade is None:
            idade, justificativa = self.extrair_idade_justificativa(justificativa)
        
        # Determinar tipo de ingresso
        tipo, detalhes, preco = self.determinar_tipo_ingresso(idade, justificativa, data_venda)
        
        return {
            'tipo': tipo,
            'preco': preco,
            'justificativa': self.gerar_justificativa_automatica(tipo, detalhes, idade),
            'idade_detectada': idade
        }

# Exemplo de uso
if __name__ == "__main__":
    sistema = SistemaPoliticas()
    
    # Testes
    testes = [
        {"justificativa": "Idoso 65 anos", "idade": None},
        {"justificativa": "Estudante universidade particular", "idade": 22},
        {"justificativa": "Professor rede pública", "idade": 35},
        {"justificativa": "Criança 4 anos", "idade": 4},
        {"justificativa": "", "idade": 25},
        {"justificativa": "Terça-feira", "idade": None}
    ]
    
    for teste in testes:
        resultado = sistema.aplicar_desconto_automatico(teste)
        print(f"Entrada: {teste}")
        print(f"Resultado: {resultado}")
        print("-" * 50)
