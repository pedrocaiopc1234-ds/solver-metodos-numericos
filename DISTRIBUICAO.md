# NumerPy Solver — Como Baixar e Instalar

## Opção 1: Baixar o Aplicativo Pronto (Recomendado)

### Windows (.exe)

1. Acesse a página de [Releases](https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases)
2. Baixe a versão mais recente: `NumerPy-Solver-vX.X.X-windows.zip`
3. Extraia o arquivo ZIP em qualquer pasta
4. Execute `NumerPy Solver.exe`
5. Pronto! O aplicativo abrirá em uma janela nativa

**Requisitos:**
- Windows 10/11
- Nenhum outro software necessário

---

### Linux (binário nativo)

1. Acesse a página de [Releases](https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases)
2. Baixe a versão: `NumerPy-Solver-vX.X.X-linux.tar.gz`
3. Extraia: `tar -xzf NumerPy-Solver-vX.X.X-linux.tar.gz`
4. Execute: `./NumerPy Solver`

**Requisitos:**
- Python 3.8+ (apenas para dependências do sistema)
- GTK3 e WebView instalados

**Instalar dependências no Ubuntu/Debian:**
```bash
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0
```

**Instalar dependências no Fedora:**
```bash
sudo dnf install python3-gobject gtk3 webkit2gtk3
```

---

### macOS (.app)

1. Acesse a página de [Releases](https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases)
2. Baixe a versão: `NumerPy-Solver-vX.X.X-macos.dmg`
3. Monte o arquivo DMG
4. Arraste `NumerPy Solver.app` para a pasta Applications
5. Execute a partir do Launchpad ou Applications

**Requisitos:**
- macOS 10.15 (Catalina) ou superior
- Nenhum outro software necessário

**Se aparecer aviso de aplicativo não verificado:**
1. Vá em Preferências do Sistema > Segurança e Privacidade
2. Clique em "Abrir Mesmo Assim"
3. Ou execute no terminal: `xattr -cr /Applications/NumerPy\ Solver.app`

---

## Opção 2: Rodar via Código Fonte

Funciona em **Windows, Linux e macOS**.

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos.git
cd solver-metodos-numericos

# Crie e ative o ambiente virtual
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

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

# O executável estará em:
# Windows: dist/NumerPy Solver/NumerPy Solver.exe
# Linux:   dist/NumerPy Solver/NumerPy Solver
# macOS:   dist/NumerPy Solver/NumerPy Solver.app
```

---

## Problemas Comuns

### Windows

**"Não foi possível abrir o aplicativo"**
- Verifique se o Windows Defender não bloqueou o executável
- Permissão pode ser necessária na primeira execução

**Aplicativo fecha imediatamente**
- Verifique se todos os arquivos foram extraídos do ZIP
- A pasta deve conter: `NumerPy Solver.exe`, `assets/`, `pages/`, `core/`, etc.

---

### Linux

**Erro ao iniciar: "No module named 'gi'"**
```bash
# Ubuntu/Debian:
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

# Fedora:
sudo dnf install python3-gobject gtk3 webkit2gtk3
```

**Erro: "cannot open display"**
- Certifique-se de estar executando em ambiente gráfico (X11/Wayland)
- Em WSL, instale um servidor X ou use o modo navegador (`python app.py`)

---

### macOS

**"O aplicativo não pode ser aberto porque o desenvolvedor não pode ser verificado"**
1. Vá em Preferências do Sistema > Segurança e Privacidade
2. Clique em "Abrir Mesmo Assim"
3. Ou execute: `xattr -cr /Applications/NumerPy\ Solver.app`

**Aplicativo não aparece no Dock**
- Isso é normal no modo pywebview
- O aplicativo funciona normalmente mesmo sem ícone no Dock

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
