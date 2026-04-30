# 📱 NumerPy Solver — Guia de Instalação

## Aplicação Multiplataforma

O NumerPy Solver funciona em **qualquer dispositivo**: PCs, notebooks, celulares e tablets.

---

## 🖥️ Desktop (Windows, macOS, Linux)

### Opção 1: Aplicação Desktop com pywebview (Recomendado)

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o aplicativo:**
   ```bash
   python main.py
   ```

3. **O app abrirá em uma janela nativa** com a interface completa do solver.

### Opção 2: Navegador Web

1. **Inicie o servidor:**
   ```bash
   python app.py
   ```

2. **Acesse no navegador:**
   ```
   http://127.0.0.1:8050
   ```

### Opção 3: Executável (.exe no Windows)

1. **Crie o executável:**
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed --name="NumerPy Solver" main.py
   ```

2. **Encontre o .exe** na pasta `dist/` e distribua para usuários.

---

## 📱 Mobile (Celular e Tablet)

### iOS (iPhone/iPad)

1. **Abra Safari** e acesse a URL do servidor (ex: `https://seu-solver.onrender.com`)

2. **Toque no botão Compartilhar** (ícone de caixa com seta)

3. **Selecione "Adicionar à Tela de Início"**

4. **Pronto!** O ícone do NumerPy aparecerá na sua tela inicial como um app nativo.

### Android

1. **Abra o Chrome** e acesse a URL do servidor

2. **Toque no menu (⋮)** e selecione **"Instalar aplicativo"** ou **"Adicionar à tela inicial"**

3. **Confirme a instalação**

4. **Pronto!** O app estará disponível na sua tela inicial.

---

## 🌐 Hospedagem Online (Para acesso mobile remoto)

Para que usuários mobile acessem o app de qualquer lugar, faça deploy em:

### Render (Gratuito)
1. Crie conta em https://render.com
2. Conecte seu repositório GitHub
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
4. Deploy automático!

### Hugging Face Spaces (Gratuito)
1. Crie um Space em https://huggingface.co/spaces
2. Selecione "Docker" como SDK
3. Crie um `Dockerfile`:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "app.py"]
   ```
4. Deploy automático!

### Railway (Gratuito com limites)
1. Acesse https://railway.app
2. Conecte seu GitHub
3. Deploy automático detectando `requirements.txt`

---

## 📋 Resumo das Plataformas

| Dispositivo | Método | Instalação |
|-------------|--------|------------|
| Windows | .exe ou navegador | Baixe .exe ou acesse URL |
| macOS | App ou navegador | `python main.py` ou URL |
| Linux | App ou navegador | `python main.py` ou URL |
| iOS (iPhone/iPad) | PWA via Safari | "Adicionar à Tela de Início" |
| Android | PWA via Chrome | "Instalar aplicativo" |

---

## 🔧 Solução de Problemas

### O app não abre no desktop
- Verifique se o Python 3.10+ está instalado
- Execute `pip install -r requirements.txt` novamente
- Tente `python app.py` e acesse via navegador

### Não consigo instalar no celular
- Verifique se está usando Safari (iOS) ou Chrome (Android)
- O servidor precisa estar acessível via HTTPS para PWA
- Use uma das opções de hospedagem acima

### Erro de porta já em uso
- Mude a porta no `app.py`: `app.run(port=8051)`

---

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no GitHub:
https://github.com/pedrocaiopc1234-ds/solver-metodos-numericos/issues
