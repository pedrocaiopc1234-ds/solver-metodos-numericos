# Instalação do NumerPy Solver

Aplicação desktop para resolução de métodos numéricos.

---

## Windows

### Opção 1 — Baixar da Release (mais simples)

1. Acesse a página de releases do projeto:
   **https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/releases**

2. Na última release, clique em `NumerPy.Solver.zip` para baixar

3. Extraia o arquivo `.zip` para qualquer pasta

4. Clique duas vezes em `NumerPy Solver.exe`

> Não precisa instalar Python.

---

### Opção 2 — Gerar o executável localmente

Requisito: Python 3.10+

```bash
# 1. Clone o repositório
git clone https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos.git
cd solver-metodos-numericos

# 2. Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
pip install pyinstaller

# 4. Gere o executável
python build.py
```

O `.exe` será criado em:
```
dist/NumerPy Solver/NumerPy Solver.exe
```

Para criar um atalho na área de trabalho:
- Clique com o botão direito em `NumerPy Solver.exe`
- **Enviar para > Área de Trabalho (criar atalho)**

---

### Opção 3 — Navegador (sem executável)

```bash
python app.py
```

Acesse no navegador: **http://127.0.0.1:8050**

---

## Publicar uma nova release

Para disponibilizar o `.exe` para download:

1. Gere o executável com `python build.py`
2. Compacte a pasta `dist/NumerPy Solver/` em um `.zip`
3. No GitHub, vá em **Releases > Draft a new release**
4. Faça upload do `.zip` e publique

---

## Suporte

Encontrou algum problema? Abra uma issue em:
https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/issues
