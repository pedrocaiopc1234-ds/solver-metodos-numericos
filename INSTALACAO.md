# Instalação do NumerPy Solver

Aplicação desktop para resolução de métodos numéricos.

---

## Windows — Instalação com um clique

1. Baixe o arquivo `NumerPy.Solver.zip` da última release
2. Extraia para qualquer pasta
3. Clique duas vezes em `NumerPy Solver.exe`

Pronto. Não precisa instalar Python.

---

## Executar pelo código (desenvolvedores)

Requisito: Python 3.10+

```bash
# 1. Clone o repositório
git clone https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos.git
cd solver-metodos-numericos

# 2. Crie o ambiente virtual
python -m venv venv

# 3. Ative o ambiente
venv\Scripts\activate        # Windows
# source venv/bin/activate  # macOS/Linux

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute
python main.py              # App desktop
python app.py               # Navegador web
```

---

## Criar o executável (.exe)

Para gerar o arquivo de instalação:

```bash
pip install pyinstaller
python build.py
```

O executável será criado em `dist/NumerPy Solver/`.

---

## Suporte

Encontrou algum problema? Abra uma issue em:
https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/issues
