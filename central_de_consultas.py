"""
Central de Consultas — projeto de API um pouco mais completo.

Funcionalidades:
- Consulta de CEP (ViaCEP)
- Cotação de moedas (AwesomeAPI - Economia)
- Histórico de buscas salvo em arquivo JSON (persiste entre execuções)
- Menu interativo em loop, com tratamento de erro em cada chamada

Nenhuma das APIs usadas aqui precisa de chave/API key.
"""

import json
import os
from datetime import datetime

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_HISTORICO = os.path.join(BASE_DIR, "historico.json")

TIMEOUT = 5
LIMITE_EXIBICAO = 10


class CentralConsultas:
    def __init__(self):
        self.historico = self.carregar_historico()

    def carregar_historico(self):
        if not os.path.exists(ARQUIVO_HISTORICO):
            return []

        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Aviso: não consegui ler o histórico salvo. Começando um novo.")
            return []

        if not isinstance(dados, list):
            return []
        return dados

    def salvar_historico(self):
        try:
            with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
                json.dump(self.historico, f, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: não consegui salvar o histórico em disco.")

    def registrar(self, tipo, consulta, resultado):
        self.historico.append({
            "tipo": tipo,
            "consulta": consulta,
            "resultado": resultado,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
        self.salvar_historico()

    def buscar_json(self, url):
        try:
            response = requests.get(url, timeout=TIMEOUT)
        except requests.exceptions.Timeout:
            return None, "A API demorou demais pra responder. Tenta de novo."
        except requests.exceptions.RequestException:
            return None, "Erro de conexão. Confere sua internet e tenta de novo."

        if response.status_code == 404:
            return None, "Não encontrado (404). Confere o que você digitou."
        if response.status_code != 200:
            return None, f"Erro inesperado: status {response.status_code}"

        try:
            return response.json(), None
        except ValueError:
            return None, "A API respondeu em um formato inesperado. Tenta mais tarde."

    def consultar_cep(self, cep):
        cep_limpo = "".join(c for c in cep if c.isdigit())

        if len(cep_limpo) != 8:
            print("CEP inválido. Digite 8 números, ex: 01310930")
            return

        dados, erro = self.buscar_json(f"https://viacep.com.br/ws/{cep_limpo}/json/")
        if erro:
            print(erro)
            return

        if dados.get("erro"):
            print("CEP não encontrado.")
            return

        logradouro = dados.get("logradouro") or "(sem logradouro)"
        bairro = dados.get("bairro") or "(sem bairro)"
        cidade = dados.get("localidade", "?")
        uf = dados.get("uf", "?")

        print(f"\n{logradouro}, {bairro}")
        print(f"   {cidade} - {uf}")
        print(f"   CEP: {dados.get('cep', cep_limpo)}")

        self.registrar("CEP", cep_limpo, f"{logradouro}, {cidade}/{uf}")

    def consultar_cotacao(self, moeda_origem, moeda_destino):
        origem = moeda_origem.strip().upper()
        destino = moeda_destino.strip().upper()

        if not origem.isalpha() or not destino.isalpha():
            print("Use apenas letras nas siglas, ex: USD, BRL, EUR, BTC.")
            return

        par = f"{origem}-{destino}"
        dados, erro = self.buscar_json(f"https://economia.awesomeapi.com.br/json/last/{par}")
        if erro:
            print(erro)
            return

        chave = f"{origem}{destino}"
        if chave not in dados:
            print("Par de moedas não encontrado. Confere as siglas (ex: USD, BRL, EUR, BTC).")
            return

        info = dados[chave]

        try:
            valor = float(info["bid"])
        except (KeyError, TypeError, ValueError):
            print("A API não retornou uma cotação válida pra esse par.")
            return

        resultado = f"1 {origem} = {valor:.4f} {destino}"
        print(f"\n{resultado}")
        print(f"   Atualizado em: {info.get('create_date', 'data não informada')}")

        self.registrar("Cotação", par, resultado)

    def mostrar_historico(self):
        if not self.historico:
            print("\nNenhuma consulta feita ainda.")
            return

        total = len(self.historico)
        print(f"\nHistórico ({total} consultas, mostrando as {min(total, LIMITE_EXIBICAO)} últimas):")
        for i, item in enumerate(self.historico[-LIMITE_EXIBICAO:], 1):
            print(f"   {i}. [{item.get('tipo', '?')}] {item.get('consulta', '?')} "
                  f"-> {item.get('resultado', '?')} ({item.get('data', '?')})")


def menu():
    app = CentralConsultas()

    while True:
        print("\n" + "=" * 40)
        print("CENTRAL DE CONSULTAS")
        print("=" * 40)
        print("1. Consultar CEP")
        print("2. Consultar cotação de moeda")
        print("3. Ver histórico")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            app.consultar_cep(input("Digite o CEP (ex: 01310930): "))

        elif opcao == "2":
            origem = input("Moeda de origem (ex: USD): ")
            destino = input("Moeda de destino (ex: BRL): ")
            app.consultar_cotacao(origem, destino)

        elif opcao == "3":
            app.mostrar_historico()

        elif opcao == "0":
            print("Até mais!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    try:
        menu()
    except (KeyboardInterrupt, EOFError):
        print("\n\nEncerrado pelo usuário. Até mais!")