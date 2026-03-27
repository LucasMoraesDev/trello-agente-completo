"""
TRELLO AGENTE COMPLETO - Sistema Avançado de Gerenciamento
Funcionalidades: Criar cards, datas, labels, mover cards, checklists, relatórios
"""

import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class TrelloAgenteCompleto:
    """Agente completo para gerenciamento do Trello"""
    
    def __init__(self):
        """Inicializa o agente com as credenciais"""
        self.api_key = os.getenv('TRELLO_API_KEY')
        self.token = os.getenv('TRELLO_TOKEN')
        
        if not self.api_key or not self.token:
            raise ValueError("❌ Credenciais não encontradas! Configure o arquivo .env")
        
        self.base_url = "https://api.trello.com/1"
        print("✅ Agente Trello inicializado com sucesso!")
    
    def _fazer_requisicao(self, endpoint, method='GET', data=None):
        """Faz requisição à API do Trello"""
        url = f"{self.base_url}{endpoint}"
        params = {
            'key': self.api_key,
            'token': self.token
        }
        
        if method == 'GET':
            response = requests.get(url, params=params)
        elif method == 'POST':
            response = requests.post(url, params=params, data=data)
        elif method == 'PUT':
            response = requests.put(url, params=params, data=data)
        else:
            raise ValueError(f"Método {method} não suportado")
        
        if response.status_code in [200, 201]:
            return response.json() if response.text else None
        else:
            raise Exception(f"Erro {response.status_code}: {response.text[:200]}")
    
    def listar_boards(self):
        """Lista todos os boards"""
        boards = self._fazer_requisicao("/members/me/boards")
        
        if not boards:
            print("📭 Nenhum board encontrado.")
            return []
        
        print(f"\n{'='*60}")
        print(f"📋 BOARDS DISPONÍVEIS ({len(boards)})")
        print('='*60)
        for i, board in enumerate(boards, 1):
            print(f"{i}. 📌 {board['name']}")
            print(f"   🆔 ID: {board['id']}")
            print(f"   🔗 URL: {board['url']}")
            print()
        
        return boards
    
    def listar_listas(self, board_id):
        """Lista todas as listas de um board"""
        lists = self._fazer_requisicao(f"/boards/{board_id}/lists")
        
        print(f"\n{'='*60}")
        print(f"📋 LISTAS DO BOARD")
        print('='*60)
        for i, lista in enumerate(lists, 1):
            print(f"{i}. 📑 {lista['name']}")
            print(f"   🆔 ID: {lista['id']}")
            print()
        
        return lists
    
    # ==================== FUNÇÃO 1: CRIAR CARD SIMPLES ====================
    def criar_card_simples(self, board_id, lista_nome, titulo, descricao=""):
        """Cria um card simples sem funcionalidades extras"""
        try:
            lists = self._fazer_requisicao(f"/boards/{board_id}/lists")
            
            lista_id = None
            for lista in lists:
                if lista['name'].lower() == lista_nome.lower():
                    lista_id = lista['id']
                    break
            
            if not lista_id:
                print(f"❌ Lista '{lista_nome}' não encontrada!")
                return None
            
            data = {
                'name': titulo,
                'desc': descricao,
                'idList': lista_id
            }
            
            card = self._fazer_requisicao("/cards", method='POST', data=data)
            
            print(f"\n✅ CARD CRIADO COM SUCESSO!")
            print(f"📌 Título: {card['name']}")
            print(f"🔗 URL: {card['url']}")
            
            return card
        except Exception as e:
            print(f"❌ Erro ao criar card: {e}")
            return None
    
    # ==================== FUNÇÃO 2: CRIAR CARD COM DATA ====================
    def criar_card_com_data(self, board_id, lista_nome, titulo, descricao="", data_vencimento=None):
        """Cria um card com data de vencimento"""
        try:
            lists = self._fazer_requisicao(f"/boards/{board_id}/lists")
            
            lista_id = None
            for lista in lists:
                if lista['name'].lower() == lista_nome.lower():
                    lista_id = lista['id']
                    break
            
            if not lista_id:
                print(f"❌ Lista '{lista_nome}' não encontrada!")
                return None
            
            # Formatar data para ISO 8601
            if data_vencimento:
                if isinstance(data_vencimento, str):
                    due_date = data_vencimento
                else:
                    due_date = data_vencimento.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            else:
                due_date = None
            
            data = {
                'name': titulo,
                'desc': descricao,
                'idList': lista_id,
                'due': due_date
            }
            
            card = self._fazer_requisicao("/cards", method='POST', data=data)
            
            print(f"\n✅ CARD CRIADO COM DATA!")
            print(f"📌 Título: {card['name']}")
            print(f"📅 Vence em: {data_vencimento}")
            print(f"🔗 URL: {card['url']}")
            
            return card
        except Exception as e:
            print(f"❌ Erro ao criar card: {e}")
            return None
    
    # ==================== FUNÇÃO 3: CRIAR CARD COM LABELS ====================
    def criar_card_com_labels(self, board_id, lista_nome, titulo, descricao="", labels=None):
        """Cria um card com etiquetas/labels"""
        try:
            # Primeiro cria o card
            lists = self._fazer_requisicao(f"/boards/{board_id}/lists")
            
            lista_id = None
            for lista in lists:
                if lista['name'].lower() == lista_nome.lower():
                    lista_id = lista['id']
                    break
            
            if not lista_id:
                print(f"❌ Lista '{lista_nome}' não encontrada!")
                return None
            
            data = {
                'name': titulo,
                'desc': descricao,
                'idList': lista_id
            }
            
            card = self._fazer_requisicao("/cards", method='POST', data=data)
            
            # Adicionar labels se fornecidas
            if labels:
                cores_validas = ['green', 'yellow', 'orange', 'red', 'purple', 'blue']
                
                for label_nome in labels:
                    # Buscar ou criar label
                    board_labels = self._fazer_requisicao(f"/boards/{board_id}/labels")
                    
                    label_id = None
                    for label in board_labels:
                        if label['name'].lower() == label_nome.lower():
                            label_id = label['id']
                            break
                    
                    # Se label não existe, criar uma nova
                    if not label_id:
                        # Definir cor padrão baseada no índice
                        cor = cores_validas[len(labels) % len(cores_validas)]
                        label_data = {
                            'name': label_nome,
                            'color': cor
                        }
                        nova_label = self._fazer_requisicao(f"/boards/{board_id}/labels", method='POST', data=label_data)
                        label_id = nova_label['id']
                    
                    # Adicionar label ao card
                    self._fazer_requisicao(f"/cards/{card['id']}/idLabels", method='POST', data={'value': label_id})
            
            print(f"\n✅ CARD CRIADO COM LABELS!")
            print(f"📌 Título: {card['name']}")
            print(f"🏷️  Labels: {', '.join(labels) if labels else 'Nenhuma'}")
            print(f"🔗 URL: {card['url']}")
            
            return card
        except Exception as e:
            print(f"❌ Erro ao criar card: {e}")
            return None
    
    # ==================== FUNÇÃO 4: MOVER CARD ====================
    def mover_card(self, card_id, lista_destino_nome):
        """Move um card para outra lista"""
        try:
            # Buscar informações do card
            card = self._fazer_requisicao(f"/cards/{card_id}")
            board_id = card['idBoard']
            
            # Buscar listas do board
            lists = self._fazer_requisicao(f"/boards/{board_id}/lists")
            
            # Encontrar lista de destino
            lista_id = None
            for lista in lists:
                if lista['name'].lower() == lista_destino_nome.lower():
                    lista_id = lista['id']
                    break
            
            if not lista_id:
                print(f"❌ Lista '{lista_destino_nome}' não encontrada!")
                return None
            
            # Mover o card
            data = {'idList': lista_id}
            card_atualizado = self._fazer_requisicao(f"/cards/{card_id}", method='PUT', data=data)
            
            print(f"\n✅ CARD MOVIDO COM SUCESSO!")
            print(f"📌 Título: {card_atualizado['name']}")
            print(f"➡️  Nova lista: {lista_destino_nome}")
            print(f"🔗 URL: {card_atualizado['url']}")
            
            return card_atualizado
        except Exception as e:
            print(f"❌ Erro ao mover card: {e}")
            return None
    
    # ==================== FUNÇÃO 5: ADICIONAR CHECKLIST ====================
    def adicionar_checklist(self, card_id, checklist_nome, itens=None):
        """Adiciona um checklist ao card"""
        try:
            # Criar checklist
            data = {'name': checklist_nome}
            checklist = self._fazer_requisicao(f"/cards/{card_id}/checklists", method='POST', data=data)
            
            # Adicionar itens
            if itens:
                for item in itens:
                    item_data = {'name': item}
                    self._fazer_requisicao(f"/checklists/{checklist['id']}/checkItems", method='POST', data=item_data)
            
            print(f"\n✅ CHECKLIST ADICIONADO!")
            print(f"📋 Nome: {checklist_nome}")
            print(f"📝 Itens: {len(itens) if itens else 0}")
            
            return checklist
        except Exception as e:
            print(f"❌ Erro ao adicionar checklist: {e}")
            return None
    
    # ==================== FUNÇÃO 6: GERAR RELATÓRIO ====================
    def gerar_relatorio(self, board_id):
        """Gera um relatório de progresso do board"""
        try:
            # Buscar informações do board
            board = self._fazer_requisicao(f"/boards/{board_id}")
            lists = self._fazer_requisicao(f"/boards/{board_id}/lists")
            
            print(f"\n{'='*60}")
            print(f"📊 RELATÓRIO DO BOARD: {board['name']}")
            print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            print('='*60)
            
            total_cards = 0
            estatisticas = {}
            
            for lista in lists:
                cards = self._fazer_requisicao(f"/lists/{lista['id']}/cards")
                qtd = len(cards)
                total_cards += qtd
                estatisticas[lista['name']] = qtd
                
                print(f"\n📑 {lista['name']}: {qtd} cards")
                if qtd > 0:
                    for card in cards[:3]:  # Mostrar apenas os 3 primeiros
                        print(f"   - {card['name']}")
                    if qtd > 3:
                        print(f"   ... e mais {qtd - 3} cards")
            
            print(f"\n{'='*60}")
            print(f"📈 TOTAL DE CARDS: {total_cards}")
            
            # Calcular porcentagens
            if total_cards > 0:
                concluidos = estatisticas.get('Concluído', 0) + estatisticas.get('Done', 0)
                progresso = (concluidos / total_cards) * 100
                print(f"🎯 PROGRESSO: {progresso:.1f}%")
            
            return estatisticas
        except Exception as e:
            print(f"❌ Erro ao gerar relatório: {e}")
            return None
    
    # ==================== FUNÇÃO 7: BUSCAR CARDS ====================
    def buscar_cards(self, board_id, termo_busca):
        """Busca cards por palavra-chave"""
        try:
            lists = self._fazer_requisicao(f"/boards/{board_id}/lists")
            cards_encontrados = []
            
            for lista in lists:
                cards = self._fazer_requisicao(f"/lists/{lista['id']}/cards")
                
                for card in cards:
                    if termo_busca.lower() in card['name'].lower() or \
                       termo_busca.lower() in card.get('desc', '').lower():
                        cards_encontrados.append({
                            'card': card,
                            'lista': lista['name']
                        })
            
            print(f"\n{'='*60}")
            print(f"🔍 RESULTADOS DA BUSCA: '{termo_busca}'")
            print('='*60)
            
            if not cards_encontrados:
                print("📭 Nenhum card encontrado.")
                return []
            
            for i, item in enumerate(cards_encontrados, 1):
                print(f"\n{i}. 🎯 {item['card']['name']}")
                print(f"   📋 Lista: {item['lista']}")
                if item['card'].get('desc'):
                    print(f"   📝 {item['card']['desc'][:100]}")
                print(f"   🔗 {item['card']['url']}")
            
            return cards_encontrados
        except Exception as e:
            print(f"❌ Erro ao buscar cards: {e}")
            return []

def main():
    """Menu principal interativo"""
    
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║     TRELLO AGENTE COMPLETO - Sistema Avançado        ║
    ║     Gerencie suas tarefas com Python                 ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    try:
        agente = TrelloAgenteCompleto()
        
        while True:
            print("\n" + "="*60)
            print("📌 MENU PRINCIPAL")
            print("="*60)
            print("1. 📋 Listar boards")
            print("2. 📑 Ver listas de um board")
            print("3. ✨ Criar card simples")
            print("4. 📅 Criar card com data de vencimento")
            print("5. 🏷️  Criar card com labels")
            print("6. 🔄 Mover card para outra lista")
            print("7. ✅ Adicionar checklist a um card")
            print("8. 📊 Gerar relatório de progresso")
            print("9. 🔍 Buscar cards por palavra-chave")
            print("10.🚪 Sair")
            
            opcao = input("\n👉 Escolha uma opção (1-10): ").strip()
            
            if opcao == "1":
                agente.listar_boards()
                
            elif opcao == "2":
                boards = agente.listar_boards()
                if boards:
                    try:
                        idx = int(input("\n🔢 Número do board: ")) - 1
                        if 0 <= idx < len(boards):
                            agente.listar_listas(boards[idx]['id'])
                        else:
                            print("❌ Número inválido!")
                    except ValueError:
                        print("❌ Digite um número válido!")
            
            elif opcao == "3":
                boards = agente.listar_boards()
                if boards:
                    try:
                        idx = int(input("\n🔢 Número do board: ")) - 1
                        if 0 <= idx < len(boards):
                            board = boards[idx]
                            listas = agente.listar_listas(board['id'])
                            
                            if listas:
                                lista_idx = int(input("\n🔢 Número da lista: ")) - 1
                                if 0 <= lista_idx < len(listas):
                                    titulo = input("📌 Título do card: ").strip()
                                    descricao = input("📝 Descrição (opcional): ").strip()
                                    
                                    agente.criar_card_simples(
                                        board['id'],
                                        listas[lista_idx]['name'],
                                        titulo,
                                        descricao
                                    )
                    except ValueError:
                        print("❌ Digite números válidos!")
            
            elif opcao == "4":
                boards = agente.listar_boards()
                if boards:
                    try:
                        idx = int(input("\n🔢 Número do board: ")) - 1
                        if 0 <= idx < len(boards):
                            board = boards[idx]
                            listas = agente.listar_listas(board['id'])
                            
                            if listas:
                                lista_idx = int(input("\n🔢 Número da lista: ")) - 1
                                if 0 <= lista_idx < len(listas):
                                    titulo = input("📌 Título do card: ").strip()
                                    descricao = input("📝 Descrição (opcional): ").strip()
                                    
                                    print("\n📅 Opções de data:")
                                    print("1. Hoje")
                                    print("2. Amanhã")
                                    print("3. Próximos 7 dias")
                                    print("4. Data personalizada (AAAA-MM-DD)")
                                    
                                    data_opcao = input("Escolha (1-4): ").strip()
                                    
                                    if data_opcao == "1":
                                        data = datetime.now()
                                    elif data_opcao == "2":
                                        data = datetime.now() + timedelta(days=1)
                                    elif data_opcao == "3":
                                        data = datetime.now() + timedelta(days=7)
                                    elif data_opcao == "4":
                                        data_str = input("Digite a data (AAAA-MM-DD): ").strip()
                                        data = datetime.strptime(data_str, "%Y-%m-%d")
                                    else:
                                        data = None
                                    
                                    agente.criar_card_com_data(
                                        board['id'],
                                        listas[lista_idx]['name'],
                                        titulo,
                                        descricao,
                                        data.strftime("%Y-%m-%d") if data else None
                                    )
                    except ValueError:
                        print("❌ Digite números válidos!")
            
            elif opcao == "5":
                boards = agente.listar_boards()
                if boards:
                    try:
                        idx = int(input("\n🔢 Número do board: ")) - 1
                        if 0 <= idx < len(boards):
                            board = boards[idx]
                            listas = agente.listar_listas(board['id'])
                            
                            if listas:
                                lista_idx = int(input("\n🔢 Número da lista: ")) - 1
                                if 0 <= lista_idx < len(listas):
                                    titulo = input("📌 Título do card: ").strip()
                                    descricao = input("📝 Descrição (opcional): ").strip()
                                    
                                    print("\n🏷️  Labels disponíveis:")
                                    print("Cores: green, yellow, orange, red, purple, blue")
                                    labels_input = input("Digite os labels separados por vírgula: ").strip()
                                    labels = [l.strip() for l in labels_input.split(",")] if labels_input else []
                                    
                                    agente.criar_card_com_labels(
                                        board['id'],
                                        listas[lista_idx]['name'],
                                        titulo,
                                        descricao,
                                        labels
                                    )
                    except ValueError:
                        print("❌ Digite números válidos!")
            
            elif opcao == "6":
                # Primeiro listar boards e cards
                boards = agente.listar_boards()
                if boards:
                    try:
                        board_idx = int(input("\n🔢 Número do board: ")) - 1
                        if 0 <= board_idx < len(boards):
                            board = boards[board_idx]
                            listas = agente.listar_listas(board['id'])
                            
                            if listas:
                                lista_idx = int(input("\n🔢 Número da lista com o card: ")) - 1
                                if 0 <= lista_idx < len(listas):
                                    # Listar cards da lista
                                    cards = agente._fazer_requisicao(f"/lists/{listas[lista_idx]['id']}/cards")
                                    
                                    if not cards:
                                        print("📭 Nenhum card nesta lista!")
                                    else:
                                        print("\n📝 Cards disponíveis:")
                                        for i, card in enumerate(cards, 1):
                                            print(f"{i}. {card['name']}")
                                        
                                        card_idx = int(input("\n🔢 Número do card: ")) - 1
                                        if 0 <= card_idx < len(cards):
                                            # Listar listas de destino
                                            print("\n📋 Listas disponíveis para mover:")
                                            for i, lista in enumerate(listas, 1):
                                                print(f"{i}. {lista['name']}")
                                            
                                            destino_idx = int(input("\n🔢 Número da lista de destino: ")) - 1
                                            if 0 <= destino_idx < len(listas):
                                                agente.mover_card(
                                                    cards[card_idx]['id'],
                                                    listas[destino_idx]['name']
                                                )
                    except ValueError:
                        print("❌ Digite números válidos!")
            
            elif opcao == "7":
                # Similar à opção 6, mas para adicionar checklist
                print("\n⚠️  Funcionalidade em desenvolvimento - escolha primeiro um card")
                # Implementação similar à opção 6
            
            elif opcao == "8":
                boards = agente.listar_boards()
                if boards:
                    try:
                        idx = int(input("\n🔢 Número do board para relatório: ")) - 1
                        if 0 <= idx < len(boards):
                            agente.gerar_relatorio(boards[idx]['id'])
                    except ValueError:
                        print("❌ Digite um número válido!")
            
            elif opcao == "9":
                boards = agente.listar_boards()
                if boards:
                    try:
                        idx = int(input("\n🔢 Número do board para buscar: ")) - 1
                        if 0 <= idx < len(boards):
                            termo = input("🔍 Digite a palavra-chave: ").strip()
                            agente.buscar_cards(boards[idx]['id'], termo)
                    except ValueError:
                        print("❌ Digite um número válido!")
            
            elif opcao == "10":
                print("\n👋 Até logo! Obrigado por usar o Trello Agente Completo!")
                break
            
            else:
                print("❌ Opção inválida! Escolha 1-10.")
            
            input("\n⏎ Pressione Enter para continuar...")
    
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()