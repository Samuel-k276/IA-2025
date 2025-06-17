# IA-2025

## Descrição
Este projeto tem como objetivo resolver o problema NURUOMINO (também conhecido como LITS), utilizando técnicas de Inteligência Artificial. O problema consiste em preencher uma grelha com tetraminos de forma a respeitar regras específicas, como evitar tetraminos adjacentes iguais e garantir que todas as células preenchidas formem um único polinômio válido.

## Estrutura do Projeto

- **`src/`**: Contém os scripts principais do projeto.
  - `nuruomino.py`: Script principal que implementa a solução do problema NURUOMINO.
  - `search.py`: Implementa algoritmos de busca como A*, busca em largura e profundidade.
  - `utils.py`: Funções utilitárias para manipulação de dados e suporte ao projeto.
  - `test.sh`: Script para executar testes automatizados.
- **`sample-nuruominoboards/`**: Contém exemplos de entrada e saída para testes.
  - Arquivos de entrada (`.txt`) e saída esperada (`.out`) para diferentes casos de teste.
- **`Enunciado.pdf`**: Documento com a descrição detalhada do problema e requisitos do projeto.
- **`__pycache__/`**: Diretório gerado automaticamente pelo Python para armazenar arquivos compilados.

## Como Usar
1. Certifique-se de ter Python 3.12 ou superior instalado.
2. Para resolver uma instância do problema, execute o seguinte comando:

```bash
python nuruomino.py < sample-nuruominoboards/test-01.txt
```

3. Para rodar todos os testes automaticamente, utilize o script:

```bash
bash test.sh
```

## Regras do Problema
- Cada região da grelha deve conter exatamente um tetramino.
- Tetraminos adjacentes não podem ser iguais (considerando rotações e reflexões).
- Todas as células preenchidas devem formar um único polinômio conectado.
- Não é permitido formar tetraminos 2x2.