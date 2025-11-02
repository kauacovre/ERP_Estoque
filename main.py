import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class ERPEstoque:
    def __init__(self):
        self.arquivo_produtos = "produtos.json"
        self.arquivo_movimentacoes = "movimentacoes.json"
        self.produtos = self.carregar_dados(self.arquivo_produtos)
        self.movimentacoes = self.carregar_dados(self.arquivo_movimentacoes)
        
    def carregar_dados(self, arquivo: str) -> Dict:
        """Carrega dados do arquivo JSON"""
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def salvar_dados(self, arquivo: str, dados: Dict):
        """Salva dados no arquivo JSON"""
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    
    def gerar_id(self) -> str:
        """Gera um ID único para produtos"""
        if not self.produtos:
            return "P001"
        ultimo_id = max([int(pid[1:]) for pid in self.produtos.keys()])
        return f"P{str(ultimo_id + 1).zfill(3)}"
    
    def cadastrar_produto(self):
        """Cadastra um novo produto"""
        print("\n=== CADASTRAR NOVO PRODUTO ===")
        
        nome = input("Nome do produto: ").strip()
        if not nome:
            print("❌ Nome não pode ser vazio!")
            return
        
        try:
            preco = float(input("Preço unitário (R$): "))
            quantidade = int(input("Quantidade inicial: "))
            estoque_minimo = int(input("Estoque mínimo: "))
        except ValueError:
            print("❌ Valores inválidos!")
            return
        
        categoria = input("Categoria: ").strip()
        fornecedor = input("Fornecedor: ").strip()
        
        produto_id = self.gerar_id()
        self.produtos[produto_id] = {
            "nome": nome,
            "preco": preco,
            "quantidade": quantidade,
            "estoque_minimo": estoque_minimo,
            "categoria": categoria,
            "fornecedor": fornecedor,
            "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        self.salvar_dados(self.arquivo_produtos, self.produtos)
        
        # Registrar movimentação inicial
        self.registrar_movimentacao(produto_id, "ENTRADA", quantidade, "Estoque inicial")
        
        print(f"\n✅ Produto cadastrado com sucesso! ID: {produto_id}")
    
    def listar_produtos(self):
        """Lista todos os produtos"""
        if not self.produtos:
            print("\n❌ Nenhum produto cadastrado!")
            return
        
        print("\n=== LISTA DE PRODUTOS ===")
        print(f"{'ID':<6} {'Nome':<25} {'Qtd':<8} {'Preço':<12} {'Categoria':<15}")
        print("-" * 70)
        
        for pid, produto in self.produtos.items():
            print(f"{pid:<6} {produto['nome']:<25} {produto['quantidade']:<8} "
                  f"R$ {produto['preco']:<9.2f} {produto['categoria']:<15}")
    
    def buscar_produto(self, produto_id: str) -> Optional[Dict]:
        """Busca um produto pelo ID"""
        return self.produtos.get(produto_id)
    
    def atualizar_produto(self):
        """Atualiza informações de um produto"""
        self.listar_produtos()
        
        produto_id = input("\nDigite o ID do produto: ").strip().upper()
        produto = self.buscar_produto(produto_id)
        
        if not produto:
            print("❌ Produto não encontrado!")
            return
        
        print(f"\n=== ATUALIZANDO: {produto['nome']} ===")
        print("(Deixe em branco para manter o valor atual)")
        
        nome = input(f"Nome [{produto['nome']}]: ").strip()
        preco = input(f"Preço [R$ {produto['preco']:.2f}]: ").strip()
        estoque_min = input(f"Estoque mínimo [{produto['estoque_minimo']}]: ").strip()
        categoria = input(f"Categoria [{produto['categoria']}]: ").strip()
        fornecedor = input(f"Fornecedor [{produto['fornecedor']}]: ").strip()
        
        if nome:
            produto['nome'] = nome
        if preco:
            try:
                produto['preco'] = float(preco)
            except ValueError:
                print("⚠️ Preço inválido, mantendo valor anterior")
        if estoque_min:
            try:
                produto['estoque_minimo'] = int(estoque_min)
            except ValueError:
                print("⚠️ Estoque mínimo inválido, mantendo valor anterior")
        if categoria:
            produto['categoria'] = categoria
        if fornecedor:
            produto['fornecedor'] = fornecedor
        
        self.salvar_dados(self.arquivo_produtos, self.produtos)
        print("\n✅ Produto atualizado com sucesso!")
    
    def excluir_produto(self):
        """Exclui um produto"""
        self.listar_produtos()
        
        produto_id = input("\nDigite o ID do produto a excluir: ").strip().upper()
        produto = self.buscar_produto(produto_id)
        
        if not produto:
            print("❌ Produto não encontrado!")
            return
        
        confirmacao = input(f"Confirma exclusão de '{produto['nome']}'? (S/N): ").strip().upper()
        
        if confirmacao == 'S':
            del self.produtos[produto_id]
            self.salvar_dados(self.arquivo_produtos, self.produtos)
            print("✅ Produto excluído com sucesso!")
        else:
            print("❌ Operação cancelada")
    
    def registrar_movimentacao(self, produto_id: str, tipo: str, quantidade: int, observacao: str = ""):
        """Registra uma movimentação de estoque"""
        mov_id = f"M{len(self.movimentacoes) + 1:04d}"
        self.movimentacoes[mov_id] = {
            "produto_id": produto_id,
            "tipo": tipo,
            "quantidade": quantidade,
            "observacao": observacao,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        self.salvar_dados(self.arquivo_movimentacoes, self.movimentacoes)
    
    def entrada_estoque(self):
        """Registra entrada de produtos no estoque"""
        self.listar_produtos()
        
        produto_id = input("\nDigite o ID do produto: ").strip().upper()
        produto = self.buscar_produto(produto_id)
        
        if not produto:
            print("❌ Produto não encontrado!")
            return
        
        try:
            quantidade = int(input("Quantidade de entrada: "))
            if quantidade <= 0:
                print("❌ Quantidade deve ser maior que zero!")
                return
        except ValueError:
            print("❌ Quantidade inválida!")
            return
        
        observacao = input("Observação (opcional): ").strip()
        
        produto['quantidade'] += quantidade
        self.salvar_dados(self.arquivo_produtos, self.produtos)
        self.registrar_movimentacao(produto_id, "ENTRADA", quantidade, observacao)
        
        print(f"\n✅ Entrada registrada! Estoque atual: {produto['quantidade']}")
    
    def saida_estoque(self):
        """Registra saída de produtos do estoque"""
        self.listar_produtos()
        
        produto_id = input("\nDigite o ID do produto: ").strip().upper()
        produto = self.buscar_produto(produto_id)
        
        if not produto:
            print("❌ Produto não encontrado!")
            return
        
        try:
            quantidade = int(input("Quantidade de saída: "))
            if quantidade <= 0:
                print("❌ Quantidade deve ser maior que zero!")
                return
            if quantidade > produto['quantidade']:
                print(f"❌ Estoque insuficiente! Disponível: {produto['quantidade']}")
                return
        except ValueError:
            print("❌ Quantidade inválida!")
            return
        
        observacao = input("Observação (opcional): ").strip()
        
        produto['quantidade'] -= quantidade
        self.salvar_dados(self.arquivo_produtos, self.produtos)
        self.registrar_movimentacao(produto_id, "SAÍDA", quantidade, observacao)
        
        print(f"\n✅ Saída registrada! Estoque atual: {produto['quantidade']}")
        
        if produto['quantidade'] <= produto['estoque_minimo']:
            print(f"⚠️ ALERTA: Estoque abaixo do mínimo ({produto['estoque_minimo']})!")
    
    def relatorio_estoque_baixo(self):
        """Gera relatório de produtos com estoque baixo"""
        print("\n=== PRODUTOS COM ESTOQUE BAIXO ===")
        
        produtos_baixos = [(pid, p) for pid, p in self.produtos.items() 
                          if p['quantidade'] <= p['estoque_minimo']]
        
        if not produtos_baixos:
            print("✅ Nenhum produto com estoque baixo!")
            return
        
        print(f"{'ID':<6} {'Nome':<25} {'Qtd':<8} {'Mínimo':<8} {'Status':<15}")
        print("-" * 70)
        
        for pid, produto in produtos_baixos:
            status = "CRÍTICO" if produto['quantidade'] == 0 else "BAIXO"
            print(f"{pid:<6} {produto['nome']:<25} {produto['quantidade']:<8} "
                  f"{produto['estoque_minimo']:<8} {status:<15}")
    
    def relatorio_movimentacoes(self):
        """Exibe relatório de movimentações"""
        if not self.movimentacoes:
            print("\n❌ Nenhuma movimentação registrada!")
            return
        
        print("\n=== HISTÓRICO DE MOVIMENTAÇÕES ===")
        print(f"{'ID':<6} {'Produto':<10} {'Tipo':<10} {'Qtd':<8} {'Data':<20}")
        print("-" * 70)
        
        for mov_id, mov in sorted(self.movimentacoes.items(), 
                                 key=lambda x: x[1]['data'], reverse=True)[:20]:
            produto_nome = self.produtos.get(mov['produto_id'], {}).get('nome', 'N/A')[:10]
            print(f"{mov_id:<6} {produto_nome:<10} {mov['tipo']:<10} "
                  f"{mov['quantidade']:<8} {mov['data']:<20}")
    
    def relatorio_valor_estoque(self):
        """Calcula o valor total do estoque"""
        print("\n=== VALOR TOTAL DO ESTOQUE ===")
        
        valor_total = sum(p['preco'] * p['quantidade'] for p in self.produtos.values())
        quantidade_total = sum(p['quantidade'] for p in self.produtos.values())
        
        print(f"Total de produtos: {len(self.produtos)}")
        print(f"Quantidade total de itens: {quantidade_total}")
        print(f"Valor total em estoque: R$ {valor_total:,.2f}")
        
        print("\n=== DETALHAMENTO POR PRODUTO ===")
        print(f"{'ID':<6} {'Nome':<25} {'Qtd':<8} {'Valor Unit.':<15} {'Valor Total':<15}")
        print("-" * 80)
        
        for pid, produto in self.produtos.items():
            valor_produto = produto['preco'] * produto['quantidade']
            print(f"{pid:<6} {produto['nome']:<25} {produto['quantidade']:<8} "
                  f"R$ {produto['preco']:<12.2f} R$ {valor_produto:<12.2f}")
    
    def menu_principal(self):
        """Menu principal do sistema"""
        while True:
            print("\n" + "="*50)
            print("          ERP DE ESTOQUE - MENU PRINCIPAL")
            print("="*50)
            print("1.  Cadastrar Produto")
            print("2.  Listar Produtos")
            print("3.  Atualizar Produto")
            print("4.  Excluir Produto")
            print("5.  Entrada de Estoque")
            print("6.  Saída de Estoque")
            print("7.  Relatório - Estoque Baixo")
            print("8.  Relatório - Movimentações")
            print("9.  Relatório - Valor do Estoque")
            print("0.  Sair")
            print("="*50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.cadastrar_produto()
            elif opcao == "2":
                self.listar_produtos()
            elif opcao == "3":
                self.atualizar_produto()
            elif opcao == "4":
                self.excluir_produto()
            elif opcao == "5":
                self.entrada_estoque()
            elif opcao == "6":
                self.saida_estoque()
            elif opcao == "7":
                self.relatorio_estoque_baixo()
            elif opcao == "8":
                self.relatorio_movimentacoes()
            elif opcao == "9":
                self.relatorio_valor_estoque()
            elif opcao == "0":
                print("\n👋 Encerrando o sistema. Até logo!")
                break
            else:
                print("\n❌ Opção inválida!")
            
            input("\nPressione ENTER para continuar...")

# Executar o sistema
if __name__ == "__main__":
    erp = ERPEstoque()
    erp.menu_principal()