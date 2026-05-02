# NumerPy Solver — Como Baixar e Instalar

## Opção 1: Baixar o Aplicativo Pronto (Recomendado)

### Para Windows (.exe)

1. Acesse a página de [Releases](https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases)
2. Baixe a versão mais recente: `NumerPy-Solver-vX.X.X.zip`
3. Extraia o arquivo ZIP em qualquer pasta
4. Execute `NumerPy Solver.exe`
5. Pronto! O aplicativo abrirá em uma janela nativa

**Requisitos:**
- Windows 10/11
- Nenhum outro software necessário (Python, etc.)

---

## Opção 2: Rodar via Código Fonte

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos.git
cd solver-metodos-numericos

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo (modo desktop)
python main.py
```

### Ou execute no navegador:

```bash
python app.py
# Acesse http://127.0.0.1:8050
```

---

## Opção 3: Criar seu Próprio Executável

Se quiser compilar o executável você mesmo:

```bash
# Instale o PyInstaller
pip install pyinstaller pywebview

# Execute o build
python build.py

# O executável estará em: dist/NumerPy Solver/NumerPy Solver.exe
```

---

## Problemas Comuns

### "Não foi possível abrir o aplicativo"

Verifique se o Windows Defender não bloqueou o executável. Permissão pode ser necessária na primeira execução.

### "Erro ao iniciar servidor"

A porta 8050 pode estar em uso. Feche outros aplicativos Dash ou modifique a porta no arquivo `main.py`.

### Aplicativo fecha imediatamente

Verifique se todos os arquivos foram extraídos corretamente do ZIP. A pasta deve conter:
- `NumerPy Solver.exe`
- Pasta `assets/`
- Pasta `pages/`
- Pasta `core/`
- Entre outras...

---

## Funcionalidades

O NumerPy Solver resolve problemas de métodos numéricos:

- **Raízes de Funções**: Bisseção, Newton, Secante
- **Sistemas Lineares**: LU, Gauss, Gauss-Seidel, Gauss-Jacobi
- **Interpolação**: Newton, Lagrange
- **Integração Numérica**: Simpson 1/3, Trapézio, Simpson 3/8
- **EDOs**: Euler, Runge-Kutta 4

---

## Suporte

Para bugs ou sugestões, abra uma [issue no GitHub](https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/issues).
