# Central de Consultas

Aplicação de linha de comando em Python que reúne, em um único menu, consultas a duas APIs públicas brasileiras — busca de endereço por CEP e cotação de moedas em tempo real — com histórico persistente entre execuções.

Nenhuma das APIs utilizadas exige chave de acesso.

## Funcionalidades

- **Consulta de CEP** — retorna logradouro, bairro, cidade e UF a partir de um CEP, com validação da entrada antes de chamar a API.
- **Cotação de moedas** — retorna a cotação atual de qualquer par suportado (USD-BRL, EUR-BRL, BTC-BRL, entre outros) com a data da última atualização.
- **Histórico persistente** — todas as consultas são gravadas em `historico.json` e continuam disponíveis ao reabrir o programa.
- **Tratamento de erros** — falha de conexão, timeout, resposta fora do formato esperado, CEP inexistente e entrada inválida são tratados com mensagem clara, sem interromper a execução.

## Tecnologias

| Recurso | Uso no projeto |
|---|---|
| Python 3.8+ | Linguagem base |
| [requests](https://pypi.org/project/requests/) | Requisições HTTP |
| [ViaCEP](https://viacep.com.br/) | API de consulta de CEP |
| [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas) | API de cotação de moedas |
| `json` / `os` / `datetime` | Persistência em disco e formatação de datas |

## Como executar

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/central-de-consultas.git
cd central-de-consultas
```

(Opcional, mas recomendado) crie um ambiente virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

Instale a dependência e rode:

```bash
pip install -r requirements.txt
python central_consultas.py
```

## Exemplo de uso

```
========================================
CENTRAL DE CONSULTAS
========================================
1. Consultar CEP
2. Consultar cotação de moeda
3. Ver histórico
0. Sair

Escolha uma opção: 1
Digite o CEP (ex: 01310930): 01310930

Avenida Paulista, Bela Vista
   São Paulo - SP
   CEP: 01310-930
```

## Estrutura do projeto

```
central-de-consultas/
├── central_consultas.py   # Código principal
├── requirements.txt       # Dependências
├── .gitignore
└── README.md
```

O arquivo `historico.json` é gerado automaticamente na primeira consulta e fica de fora do controle de versão.

## Decisões de implementação

- As chamadas HTTP foram centralizadas em um único método (`buscar_json`) que devolve `(dados, erro)`, evitando repetir blocos de `try/except` em cada consulta.
- O caminho do arquivo de histórico é resolvido a partir da localização do script, e não do diretório de trabalho atual, para que o histórico não se perca quando o programa é executado de outra pasta.
- O acesso aos campos da resposta usa `.get()` em vez de indexação direta, já que a API do ViaCEP retorna campos vazios para CEPs de cidades sem logradouro definido.

## Próximos passos

Adicionar consulta de CNPJ (BrasilAPI)
Exportar o histórico para CSV
Cobrir as funções de consulta com testes automatizados
Migrar a interface para uma versão web

---

Desenvolvido por Kauê H.G de Barros (https://github.com/Kaue18-py)