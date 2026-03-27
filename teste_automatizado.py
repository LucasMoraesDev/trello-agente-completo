"""
TESTE AUTOMATIZADO - Trello Agente Completo
Testa todas as funcionalidades e gera relatório
"""

import sys
import time
from datetime import datetime, timedelta
from trello_agente_completo import TrelloAgenteCompleto

class TesteAutomatizado:
    """Classe para executar testes automatizados"""
    
    def __init__(self):
        self.agente = None
        self.board_teste = None
        self.lista_teste = None
        self.cards_criados = []
        self.testes = []
        self.passed = 0
        self.failed = 0
        
    def log(self, mensagem, tipo="INFO"):
        """Exibe mensagem formatada"""
        cores = {
            "INFO": "\033[94m",    # Azul
            "SUCESSO": "\033[92m",  # Verde
            "ERRO": "\033[91m",     # Vermelho
            "AVISO": "\033[93m",    # Amarelo
            "FIM": "\033[0m"        # Reset
        }
        
        cor = cores.get(tipo, cores["FIM"])
        print(f"{cor}[{tipo}]{cores['FIM']} {mensagem}")
    
    def iniciar(self):
        """Inicia o agente e configura ambiente de teste"""
        self.log("Iniciando teste automatizado...", "INFO")
        self.log("=" * 60, "INFO")
        
        try:
            self.agente = TrelloAgenteCompleto()
            self.log("✅ Agente inicializado com sucesso!", "SUCESSO")
            return True
        except Exception as e:
            self.log(f"❌ Falha ao inicializar agente: {e}", "ERRO")
            return False
    
    def encontrar_board_teste(self):
        """Encontra ou cria um board para testes"""
        self.log("\n📋 Procurando board para testes...", "INFO")
        
        boards = self.agente.listar_boards()
        
        # Procurar board específico de teste
        for board in boards:
            if board['name'] == "Teste Python":
                self.board_teste = board
                self.log(f"✅ Board 'Teste Python' encontrado!", "SUCESSO")
                return True
        
        # Se não encontrar, usar o primeiro board
        if boards:
            self.board_teste = boards[0]
            self.log(f"⚠️  Board de teste não encontrado. Usando: {self.board_teste['name']}", "AVISO")
            return True
        
        self.log("❌ Nenhum board disponível para testes!", "ERRO")
        return False
    
    def encontrar_lista_teste(self):
        """Encontra lista para testes"""
        self.log("\n📑 Procurando lista para testes...", "INFO")
        
        listas = self.agente.listar_listas(self.board_teste['id'])
        
        # Procurar lista "A fazer"
        for lista in listas:
            if lista['name'] == "A fazer":
                self.lista_teste = lista
                self.log(f"✅ Lista 'A fazer' encontrada!", "SUCESSO")
                return True
        
        # Se não encontrar, usar primeira lista
        if listas:
            self.lista_teste = listas[0]
            self.log(f"⚠️  Lista 'A fazer' não encontrada. Usando: {self.lista_teste['name']}", "AVISO")
            return True
        
        self.log("❌ Nenhuma lista disponível para testes!", "ERRO")
        return False
    
    def registrar_teste(self, nome, status, detalhes=""):
        """Registra resultado de um teste"""
        resultado = {
            "nome": nome,
            "status": status,
            "detalhes": detalhes,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.testes.append(resultado)
        
        if status:
            self.passed += 1
            self.log(f"✅ {nome}: SUCESSO - {detalhes}", "SUCESSO")
        else:
            self.failed += 1
            self.log(f"❌ {nome}: FALHA - {detalhes}", "ERRO")
    
    def test_criar_card_simples(self):
        """Teste 1: Criar card simples"""
        self.log("\n🧪 TESTE 1: Criar card simples", "INFO")
        
        titulo = f"🧪 Teste Card Simples - {datetime.now().strftime('%H:%M:%S')}"
        descricao = "Este card foi criado automaticamente pelo teste automatizado"
        
        try:
            card = self.agente.criar_card_simples(
                self.board_teste['id'],
                self.lista_teste['name'],
                titulo,
                descricao
            )
            
            if card and card['name'] == titulo:
                self.cards_criados.append(card)
                self.registrar_teste("Criar card simples", True, f"Card ID: {card['id']}")
                return card
            else:
                self.registrar_teste("Criar card simples", False, "Card não foi criado corretamente")
                return None
        except Exception as e:
            self.registrar_teste("Criar card simples", False, str(e))
            return None
    
    def test_criar_card_com_data(self):
        """Teste 2: Criar card com data de vencimento"""
        self.log("\n🧪 TESTE 2: Criar card com data", "INFO")
        
        titulo = f"📅 Card com Data - {datetime.now().strftime('%H:%M:%S')}"
        descricao = "Este card tem data de vencimento"
        data_vencimento = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        try:
            card = self.agente.criar_card_com_data(
                self.board_teste['id'],
                self.lista_teste['name'],
                titulo,
                descricao,
                data_vencimento
            )
            
            if card:
                self.cards_criados.append(card)
                # Verificar se a data foi salva
                card_detalhes = self.agente._fazer_requisicao(f"/cards/{card['id']}")
                if card_detalhes.get('due'):
                    self.registrar_teste("Criar card com data", True, f"Data definida: {data_vencimento}")
                else:
                    self.registrar_teste("Criar card com data", False, "Data não foi salva")
                return card
            else:
                self.registrar_teste("Criar card com data", False, "Card não foi criado")
                return None
        except Exception as e:
            self.registrar_teste("Criar card com data", False, str(e))
            return None
    
    def test_criar_card_com_labels(self):
        """Teste 3: Criar card com labels"""
        self.log("\n🧪 TESTE 3: Criar card com labels", "INFO")
        
        titulo = f"🏷️ Card com Labels - {datetime.now().strftime('%H:%M:%S')}"
        descricao = "Este card tem etiquetas coloridas"
        labels = ["teste", "automatizado", "python"]
        
        try:
            card = self.agente.criar_card_com_labels(
                self.board_teste['id'],
                self.lista_teste['name'],
                titulo,
                descricao,
                labels
            )
            
            if card:
                self.cards_criados.append(card)
                # Verificar se labels foram adicionadas
                card_labels = self.agente._fazer_requisicao(f"/cards/{card['id']}/labels")
                if len(card_labels) > 0:
                    self.registrar_teste("Criar card com labels", True, f"{len(card_labels)} labels adicionadas")
                else:
                    self.registrar_teste("Criar card com labels", False, "Labels não foram adicionadas")
                return card
            else:
                self.registrar_teste("Criar card com labels", False, "Card não foi criado")
                return None
        except Exception as e:
            self.registrar_teste("Criar card com labels", False, str(e))
            return None
    
    def test_mover_card(self):
        """Teste 4: Mover card entre listas"""
        self.log("\n🧪 TESTE 4: Mover card para outra lista", "INFO")
        
        if not self.cards_criados:
            self.log("⚠️  Nenhum card disponível para mover", "AVISO")
            self.registrar_teste("Mover card", False, "Nenhum card criado anteriormente")
            return False
        
        # Encontrar lista "Em andamento" ou outra lista
        listas = self.agente.listar_listas(self.board_teste['id'])
        lista_destino = None
        
        for lista in listas:
            if lista['id'] != self.lista_teste['id']:
                lista_destino = lista
                break
        
        if not lista_destino:
            self.log("⚠️  Nenhuma lista de destino encontrada", "AVISO")
            self.registrar_teste("Mover card", False, "Lista de destino não encontrada")
            return False
        
        try:
            card_para_mover = self.cards_criados[0]
            card_movido = self.agente.mover_card(
                card_para_mover['id'],
                lista_destino['name']
            )
            
            if card_movido:
                self.registrar_teste("Mover card", True, f"Movido para: {lista_destino['name']}")
                return True
            else:
                self.registrar_teste("Mover card", False, "Falha ao mover card")
                return False
        except Exception as e:
            self.registrar_teste("Mover card", False, str(e))
            return False
    
    def test_buscar_cards(self):
        """Teste 5: Buscar cards por palavra-chave"""
        self.log("\n🧪 TESTE 5: Buscar cards", "INFO")
        
        try:
            resultados = self.agente.buscar_cards(
                self.board_teste['id'],
                "teste"
            )
            
            if resultados is not None:
                quantidade = len(resultados)
                self.registrar_teste("Buscar cards", True, f"Encontrados {quantidade} cards")
                return True
            else:
                self.registrar_teste("Buscar cards", False, "Falha na busca")
                return False
        except Exception as e:
            self.registrar_teste("Buscar cards", False, str(e))
            return False
    
    def test_gerar_relatorio(self):
        """Teste 6: Gerar relatório"""
        self.log("\n🧪 TESTE 6: Gerar relatório", "INFO")
        
        try:
            relatorio = self.agente.gerar_relatorio(self.board_teste['id'])
            
            if relatorio is not None:
                self.registrar_teste("Gerar relatório", True, "Relatório gerado com sucesso")
                return True
            else:
                self.registrar_teste("Gerar relatório", False, "Falha ao gerar relatório")
                return False
        except Exception as e:
            self.registrar_teste("Gerar relatório", False, str(e))
            return False
    
    def test_adicionar_checklist(self):
        """Teste 7: Adicionar checklist"""
        self.log("\n🧪 TESTE 7: Adicionar checklist", "INFO")
        
        if not self.cards_criados:
            self.log("⚠️  Nenhum card disponível para checklist", "AVISO")
            self.registrar_teste("Adicionar checklist", False, "Nenhum card criado")
            return False
        
        try:
            card_para_checklist = self.cards_criados[-1] if self.cards_criados else None
            if not card_para_checklist:
                self.registrar_teste("Adicionar checklist", False, "Card não encontrado")
                return False
            
            itens = ["Item 1 do checklist", "Item 2 do checklist", "Item 3 do checklist"]
            checklist = self.agente.adicionar_checklist(
                card_para_checklist['id'],
                "Checklist de Teste",
                itens
            )
            
            if checklist:
                self.registrar_teste("Adicionar checklist", True, f"{len(itens)} itens adicionados")
                return True
            else:
                self.registrar_teste("Adicionar checklist", False, "Falha ao criar checklist")
                return False
        except Exception as e:
            self.registrar_teste("Adicionar checklist", False, str(e))
            return False
    
    def limpar_cards_teste(self):
        """Limpa os cards criados durante os testes"""
        self.log("\n🧹 Limpando cards de teste...", "INFO")
        
        if not self.cards_criados:
            self.log("Nenhum card para limpar", "INFO")
            return
        
        try:
            for card in self.cards_criados:
                # Arquiva os cards em vez de deletar
                self.agente._fazer_requisicao(
                    f"/cards/{card['id']}/closed",
                    method='PUT',
                    data={'value': 'true'}
                )
                self.log(f"   Card arquivado: {card['name'][:50]}", "INFO")
            
            self.log(f"✅ {len(self.cards_criados)} cards arquivados com sucesso!", "SUCESSO")
        except Exception as e:
            self.log(f"⚠️  Erro ao limpar cards: {e}", "AVISO")
    
    def gerar_relatorio_final(self):
        """Gera relatório final dos testes"""
        self.log("\n" + "="*60, "INFO")
        self.log("📊 RELATÓRIO FINAL DE TESTES", "INFO")
        self.log("="*60, "INFO")
        
        self.log(f"\n📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", "INFO")
        self.log(f"🎯 Total de testes: {len(self.testes)}", "INFO")
        self.log(f"✅ Testes passaram: {self.passed}", "SUCESSO")
        self.log(f"❌ Testes falharam: {self.failed}", "ERRO" if self.failed > 0 else "INFO")
        
        if len(self.testes) > 0:
            taxa_sucesso = (self.passed / len(self.testes)) * 100
            self.log(f"📈 Taxa de sucesso: {taxa_sucesso:.1f}%", "INFO")
        
        self.log("\n" + "-"*60, "INFO")
        self.log("📋 DETALHES DOS TESTES:", "INFO")
        self.log("-"*60, "INFO")
        
        for i, teste in enumerate(self.testes, 1):
            status = "✅" if teste['status'] else "❌"
            self.log(f"{i}. {status} {teste['nome']} [{teste['timestamp']}]", 
                    "SUCESSO" if teste['status'] else "ERRO")
            if teste['detalhes']:
                self.log(f"   📝 {teste['detalhes']}", "INFO")
        
        self.log("\n" + "="*60, "INFO")
        
        if self.failed == 0:
            self.log("🎉 PARABÉNS! Todos os testes passaram com sucesso!", "SUCESSO")
        else:
            self.log("⚠️  Alguns testes falharam. Verifique os detalhes acima.", "AVISO")
        
        self.log("="*60, "INFO")
    
    def executar_todos_testes(self):
        """Executa todos os testes"""
        self.log("🚀 INICIANDO BATERIA DE TESTES", "INFO")
        self.log("="*60, "INFO")
        
        # Fase 1: Configuração
        if not self.iniciar():
            self.log("❌ Falha na inicialização. Testes abortados!", "ERRO")
            return
        
        if not self.encontrar_board_teste():
            self.log("❌ Não foi possível encontrar board para testes!", "ERRO")
            return
        
        if not self.encontrar_lista_teste():
            self.log("❌ Não foi possível encontrar lista para testes!", "ERRO")
            return
        
        # Fase 2: Execução dos testes
        time.sleep(1)  # Pequena pausa entre testes
        
        # Teste 1: Criar card simples
        card1 = self.test_criar_card_simples()
        time.sleep(0.5)
        
        # Teste 2: Criar card com data
        card2 = self.test_criar_card_com_data()
        time.sleep(0.5)
        
        # Teste 3: Criar card com labels
        card3 = self.test_criar_card_com_labels()
        time.sleep(0.5)
        
        # Teste 4: Mover card
        self.test_mover_card()
        time.sleep(0.5)
        
        # Teste 5: Buscar cards
        self.test_buscar_cards()
        time.sleep(0.5)
        
        # Teste 6: Gerar relatório
        self.test_gerar_relatorio()
        time.sleep(0.5)
        
        # Teste 7: Adicionar checklist
        self.test_adicionar_checklist()
        
        # Fase 3: Limpeza e relatório
        self.limpar_cards_teste()
        self.gerar_relatorio_final()

def main():
    """Função principal"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║     TESTE AUTOMATIZADO - Trello Agente Completo       ║
    ║     Verificando todas as funcionalidades              ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    testador = TesteAutomatizado()
    
    try:
        testador.executar_todos_testes()
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
    
    print("\n✨ Teste concluído!")

if __name__ == "__main__":
    main()