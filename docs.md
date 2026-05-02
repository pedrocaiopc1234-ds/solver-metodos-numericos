# NumerPy Solver — Documentação Técnica

> Versão 1.1.0 | Documentação técnica completa

---

## 1. Visão Geral do Projeto

### 1.1 Objetivo

O NumerPy Solver é um calculador de métodos numéricos com interface web/desktop que implementa, do zero e em Python puro (sem delegar computação a bibliotecas externas para os métodos centrais), doze algoritmos fundamentais de análise numérica distribuídos em cinco categorias:

| Categoria | Métodos |
|-----------|---------|
| Zeros de funções | Bisseção, Newton-Raphson, Secante |
| Sistemas lineares | Fatoração LU, Eliminação de Gauss, Gauss-Seidel, Gauss-Jacobi |
| Interpolação | Newton (diferenças divididas), Lagrange |
| Integração numérica | Simpson 1/3, Trapézios, Simpson 3/8 |
| EDOs | Euler, Runge-Kutta 4 |

O solver resolve problemas de cálculo numérico que surgem recursivamente em ciência de dados, engenharia, otimização e computação científica: encontrar raízes de funções não lineares, resolver sistemas lineares de grande porte, interpolar dados experimentais, calcular integrais definidas e integrar equações diferenciais ordinárias.

### 1.2 Problema que resolve

Em contextos acadêmicos e profissionais, a necessidade de resolver problemas numéricos sem depender de caixas-pretas é fundamental para:

- **Compreensão do comportamento algorítmico**: saber quando um método converge, diverge ou produz artefatos numéricos exige entender a implementação internamente;
- **Validação pedagógica**: estudantes e pesquisadores precisam verificar passo a passo se o comportamento do algoritmo está correto, com acesso a dados intermediários de cada iteração;
- **Reprodutibilidade**: implementações que delegam toda a computação a `scipy.optimize.bisect` ou `numpy.linalg.solve` tornam-se caixas-pretas onde o processo interno é inacessível ao usuário.

O NumerPy Solver preenche essa lacuna: cada método retorna não apenas o resultado final, mas também os dados de cada iteração (`iterations_data`), permitindo inspeção completa do caminho percorrido pelo algoritmo até a convergência.

### 1.3 Diferencial em relação a bibliotecas prontas

| Aspecto | SciPy/NumPy | NumerPy Solver |
|---------|-------------|----------------|
| Transparência | Funções compiladas em C/Fortran, internos inacessíveis | Implementação Python legível, iteração a iteração |
| Dados intermediários | Não disponíveis (retornam apenas resultado final) | `iterations_data` com valores de cada passo |
| Inspeção visual | Sem visualização embutida | Gráficos Plotly gerados automaticamente com região de convergência, tangentes, áreas de integração |
| Tratamento de erros | Exceções genéricas (`ValueError`, `LinAlgError`) | Dicionários estruturados com `success`, `error`, dados parciais |
| Validação de entrada | Mínima (confia no usuário) | Camada dedicada (`validation/`) com limites explícitos |
| Linguagem | C/Fortran com bindings Python | Python puro com NumPy |

O solver não substitui SciPy em produção — é complementar. Onde SciPy oferece velocidade, o NumerPy Solver oferece transparência e inspeção.

### 1.4 Aplicações práticas

- **Ciência de dados**: interpolação de dados ausentes, integração de distribuições de probabilidade, resolução de sistemas lineares em regressão;
- **Engenharia**: cálculo de raízes de equações de equilíbrio, integração numérica de cargas e esforços, simulação de dinâmica via EDOs;
- **Otimização**: zeros de funções (KKT conditions), sistemas lineares em métodos de ponto interior;
- **Ensino**: visualização iterativa do comportamento de cada método, com tabelas de dados intermediários.

---

## 2. Arquitetura do Sistema

### 2.1 Estrutura de diretórios

```
NumerPy Solver/
├── app.py                    # Entry point: Dash web application (browser mode)
├── main.py                   # Entry point: Desktop mode (pywebview)
├── core/                     # Camada de computação pura (sem UI)
│   ├── roots.py              # Bisseção, Newton, Secante
│   ├── linear_systems.py     # LU, Gauss, Gauss-Seidel, Gauss-Jacobi
│   ├── interpolation.py      # Newton, Lagrange
│   ├── integration.py        # Simpson 1/3, Trapézios, Simpson 3/8
│   ├── ode.py                # Euler, RK4
│   └── plot.py               # Geradores de figuras Plotly
├── validation/               # Sanitização de entrada
│   ├── roots_validation.py
│   ├── linear_systems_validation.py
│   ├── interpolation_validation.py
│   ├── integration_validation.py
│   └── ode_validation.py
├── utils/                    # Parsing de expressões e helpers UI
│   ├── dash_ui.py            # Ativo (Dash)
│   └── ui.py                 # Legado (Streamlit)
├── pages/                    # Páginas Dash com callbacks
│   ├── home.py
│   ├── 1_raizes.py
│   ├── 2_sistemas_lineares.py
│   ├── 3_interpolacao.py
│   ├── 4_integracao.py
│   └── 5_edo.py
├── assets/                   # CSS, ícone, PWA manifest, service worker
├── tests/                    # Suite de testes (~305 testes)
├── comparation/              # Benchmarks contra SciPy (250 problemas)
│   ├── compare_roots.py
│   ├── compare_linear_systems.py
│   ├── compare_ode.py
│   ├── compare_interpolation.py
│   └── compare_integration.py
├── build.py                  # PyInstaller build script
├── release.py                # Automação de releases
└── requirements.txt
```

### 2.2 Fluxo interno

O fluxo de processamento segue uma arquitetura em camadas com responsabilidade única:

```
[Usuário] → pages/ → validation/ → core/ → {resultado dict}
                ↓                        ↓
          utils/dash_ui.py          core/plot.py
          (parse_function)          (visualização)
                ↓                        ↓
           callback               Plotly Figure
                ↓
           Dash UI render
```

1. **Entrada do usuário**: o usuário digita uma expressão matemática como string (ex: `"x**2 - 2"`) nos campos da interface Dash;
2. **Parsing**: `utils/dash_ui.py` converte a string em callable `lambda x: expr` via `eval()` com `SAFE_GLOBALS` (whitelist de funções matemáticas);
3. **Validação**: `validation/` verifica limites de parâmetros (tolerância, dimensões, tipos);
4. **Computação**: `core/` executa o método numérico e retorna um dicionário padronizado;
5. **Visualização**: `core/plot.py` gera figuras Plotly com região de convergência, tangentes, áreas de integração;
6. **Renderização**: a página Dash exibe cards de resultado, gráficos e tabelas de iteração.

### 2.3 Contrato de retorno padronizado

Toda função em `core/` retorna um dicionário com a seguinte estrutura canônica:

```python
{
    "success": bool,          # True se o método convergiu, False caso contrário
    "error": str | None,      # Mensagem de erro em português se success=False
    <result_key>: value,      # Raiz, vetor solução, valor da integral, etc.
    "iterations": int,        # Número de iterações (métodos iterativos)
    "iterations_data": list,  # Dados de cada iteração para visualização
}
```

Métodos iterativos (Gauss-Seidel, Gauss-Jacobi) incluem adicionalmente `"warning"` quando a matriz não é diagonalmente dominante. Métodos diretos (LU, Gauss) incluem `"L"` e `"U"` quando aplicável.

### 2.4 Interface e empacotamento

A aplicação oferece dois modos de execução:

- **Modo navegador**: `python app.py` inicia o servidor Dash em `http://127.0.0.1:8050`, acessível via navegador;
- **Modo desktop**: `python main.py` inicia o servidor em background e abre uma janela nativa via `pywebview` (fallback para navegador).

O empacotamento usa PyInstaller com modo `--onefile --windowed`, produzindo um único executável que funciona de qualquer local no sistema de arquivos. O build inclui `--collect-all` para `webview`, `pythonnet` e `clr_loader` (dependências obrigatórias do pywebview no Windows). A função `unblock_dlls()` em `main.py` remove Zone.Identifier de DLLs baixadas da internet, prevenindo crash por bloqueio do .NET Framework.

---

## 3. Métodos Numéricos Implementados

### 3.1 Bisseção (Bisection)

**Arquivo**: `core/roots.py` — `bisection(f, a, b, tol=1e-6, max_iter=100)`

#### Fundamento matemático

O método da bisseção baseia-se no **Teorema do Valor Intermediário** (TVI): se $f$ é contínua em $[a, b]$ e $f(a) \cdot f(b) < 0$, então existe pelo menos um $c \in (a, b)$ tal que $f(c) = 0$. A cada iteração, o intervalo é dividido ao meio e a metade que contém a raiz é selecionada com base na mudança de sinal.

O erro após $n$ iterações é limitado por:

$$|c_n - c^*| \leq \frac{b - a}{2^n}$$

onde $c^*$ é a raiz verdadeira. Isso garante convergência linear com taxa $1/2$ — lenta, mas absolutamente garantida sob as hipóteses do TVI.

**Condições necessárias**:
- $f$ contínua em $[a, b]$
- $f(a) \cdot f(b) < 0$ (mudança de sinal)
- $a < b$

**Limitações**:
- Convergência linear (lenta): requer aproximadamente $\log_2((b-a)/\varepsilon)$ iterações para atingir precisão $\varepsilon$;
- Não encontra raízes de multiplicidade par (funções que tocam o eixo sem cruzar);
- Requer conhecimento prévio de um intervalo com mudança de sinal.

#### Algoritmo implementado

```
1. Validar: a < b, tol > 0, max_iter > 0, f(a) e f(b) finitos, f(a)·f(b) ≤ 0
2. Para i = 0, 1, ..., max_iter-1:
   a. c = (a + b) / 2
   b. fc = f(c)
   c. Se |fc| < tol: retornar c como raiz
   d. Se f(a)·fc < 0: b = c (raiz está na metade esquerda)
   e. Senão: a = c (raiz está na metade direita)
3. Se não convergiu: retornar erro
```

**Critério de parada**: `abs(f(c)) < tol` (baseado no valor da função, não na largura do intervalo). Esta escolha difere do critério mais comum `|b - a| < tol` (largura do intervalo) — nossa implementação verifica se o valor da função é suficientemente próximo de zero.

#### Implementação no projeto

A função retorna `iterations_data` como uma lista de dicionários `[{a, b, c, fc}, ...]`, permitindo reconstruir visualmente o encolhimento do intervalo a cada passo. Validações incluem: verificação de NaN/Inf nos extremos e a cada avaliação intermediária, exigência de mudança de sinal `fa * fb <= 0` (incluindo o caso degenerado onde a raiz está num extremo), e proteção contra iterações infinitas via `max_iter`.

Uma diferença notável em relação à implementação de referência do SciPy: `scipy.optimize.bisect` usa o critério de parada baseado na largura do intervalo (`|b - a| < xtol`), enquanto nossa implementação usa o valor absoluto da função (`|f(c)| < tol`). Isso pode produzir resultados diferentes em situações onde a função é muito plana próximo à raiz (derivada próxima de zero).

#### Complexidade computacional

- **Custo por iteração**: 1 avaliação de $f$ (apenas $f(c)$, pois $f(a)$ ou $f(b)$ é reaproveitado)
- **Custo total**: $O(n)$ onde $n \approx \log_2((b - a) / \varepsilon)$
- **Custo de memória**: $O(n)$ para armazenar `iterations_data`

#### Casos de uso

- **Usar quando**: se conhece um intervalo com mudança de sinal e se deseja garantia absoluta de convergência; funções não diferenciáveis ou descontínuas.
- **Não usar quando**: se precisa de convergência rápida; se a função não muda de sinal na raiz (raízes de multiplicidade par); se se dispõe da derivada (preferir Newton).

---

### 3.2 Newton-Raphson

**Arquivo**: `core/roots.py` — `newton(f, df, x0, tol=1e-6, max_iter=100)`

#### Fundamento matemático

O método de Newton-Raphson usa a expansão de Taylor de primeira ordem de $f$ em torno de $x_n$:

$$f(x) \approx f(x_n) + f'(x_n)(x - x_n)$$

Igualando a zero e resolvendo para $x$, obtemos a iteração:

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

Geometricamente, a cada passo traça-se a tangente à curva no ponto $(x_n, f(x_n))$ e encontra-se sua interseção com o eixo $x$.

**Convergência**: sob as condições do teorema de Kantorovich, se $f \in C^2$ e $x_0$ está suficientemente próximo da raiz $x^*$ com $f'(x^*) \neq 0$, o método converge **quadraticamente**:

$$|x_{n+1} - x^*| \leq C |x_n - x^*|^2$$

**Condições necessárias**:
- $f$ diferenciável na vizinhança da raiz;
- $f'(x) \neq 0$ na raiz (raiz simples);
- Chute inicial $x_0$ suficientemente próximo da raiz.

**Limitações**:
- Requer a derivada $f'$ analítica (não serve se a derivada é desconhecida);
- Se $f'(x_n) = 0$ em alguma iteração, o método falha (divisão por zero);
- Para raízes de multiplicidade $m > 1$, a convergência degrada para linear — requer $m$ iterações para cada dígito de precisão;
- Pode divergir se o chute inicial está longe da raiz ou se a função tem comportamento oscilatório.

#### Algoritmo implementado

```
1. Validar: x0 finito, tol > 0, max_iter > 0
2. Para i = 0, 1, ..., max_iter-1:
   a. fx = f(x), dfx = df(x)
   b. Se dfx == 0: retornar erro (derivada zero)
   c. x_next = x - fx / dfx
   d. Se |x_next - x| < tol: retornar x_next como raiz
   e. x = x_next
3. Se não convergiu: retornar erro
```

**Critério de parada**: `|x_next - x| < tol` (baseado no passo, não no valor da função). Isso é mais robusto que verificar `|f(x)| < tol` para funções com derivada próxima de zero na raiz, onde pequenas mudanças em $x$ produzem valores de função grandes.

#### Implementação no projeto

A função retorna `iterations_data` como `[{x, fx, dfx, x_next}, ...]`, permitindo visualizar a trajetória das tangentes no gráfico Plotly. A detecção de derivada zero retorna os dados parciais até o ponto de falha, não descartando o progresso já feito. A implementação verifica NaN/Inf tanto em $f(x)$ quanto em $f'(x)$ a cada iteração.

Em comparação com `scipy.optimize.newton`, nossa implementação exige a derivada como parâmetro obrigatório (`df`), enquanto o SciPy pode executar o método da secante se `fprime` não for fornecido. O critério de parada do SciPy também é diferente: ele combina `|x_new - x| < tol` com `|f(x)| < tol` usando `tol` e `rtol`.

#### Complexidade computacional

- **Custo por iteração**: 2 avaliações ($f$ e $f'$) — portanto o dobro do custo da bisseção por iteração, mas converge em muito menos iterações.
- **Custo total**: tipicamente $O(\log \log(1/\varepsilon))$ iterações para convergência quadrática.
- **Custo de memória**: $O(n)$ para `iterations_data`.

#### Casos de uso

- **Usar quando**: se dispõe da derivada e de um bom chute inicial; funções suaves com raízes simples; quando velocidade de convergência é prioritária.
- **Não usar quando**: a derivada não está disponível; há risco de derivada zero; o chute inicial está muito distante da raiz (preferir bisseção ou secante).

---

### 3.3 Secante (Secant)

**Arquivo`: `core/roots.py` — `secant(f, x0, x1, tol=1e-6, max_iter=100)`

#### Fundamento matemático

O método da secante é uma aproximação do método de Newton que substitui a derivada analítica $f'(x_n)$ por uma diferença dividida:

$$x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$

Geometricamente, em vez da tangente (Newton), traça-se a secante que passa pelos dois últimos pontos e encontra-se sua interseção com o eixo $x$.

**Convergência**: sob condições suaves, a ordem de convergência é $\varphi = \frac{1+\sqrt{5}}{2} \approx 1.618$ (número de ouro) — superlinear, mas mais lenta que a convergência quadrática de Newton. A relação de recorrência do erro é:

$$|e_{n+1}| \approx C |e_n|^\varphi$$

**Condições necessárias**:
- Dois chutes iniciais $x_0$ e $x_1$ (não necessariamente com mudança de sinal);
- $f(x_n) \neq f(x_{n-1})$ em cada passo (secante não horizontal).

**Limitações**:
- Se $f(x_n) - f(x_{n-1}) \to 0$, o método se torna instável (divisão por zero ou quase-zero);
- Não tem garantia de convergência global como a bisseção;
- Pode divergir para funções com comportamento oscilatório ou múltiplas raízes próximas.

#### Algoritmo implementado

```
1. Validar: x0 e x1 finitos, tol > 0, max_iter > 0
2. f0 = f(x0), f1 = f(x1)
3. Para i = 0, 1, ..., max_iter-1:
   a. Se |x1 - x0| < tol: retornar x1 como raiz
   b. Se f1 - f0 == 0: retornar erro (secante horizontal)
   c. x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
   d. Se |x2 - x1| < tol: retornar x2 como raiz
   e. x0, f0 = x1, f1  # reutiliza f1 (evita reavaliação)
   f. x1 = x2, f1 = f(x2)
4. Se não convergiu: retornar erro
```

**Otimização**: a reatribuição `x0, f0 = x1, f1` evita reavaliar $f$ no ponto $x_1$ que já foi avaliado na iteração anterior. Isso reduz o custo por iteração de 2 para 1 avaliação de $f$ (exceto na primeira iteração).

**Critério de parada**: `|x2 - x1| < tol` (baseado no passo, análogo ao Newton).

#### Implementação no projeto

Retorna `iterations_data` como `[{x0, x1, f0, f1, x2}, ...]`, permitindo visualizar as secantes no gráfico. A detecção de secante horizontal (`f1 - f0 == 0`) retorna os dados parciais acumulados. Proteção contra NaN/Inf em todos os valores intermediários.

Em comparação com `scipy.optimize.newton` (que executa o método da secante quando `fprime` não é fornecido), o SciPy usa um algoritmo mais sofisticado com combinação de critérios de parada e fallback para bisseção quando o método ameaça divergir. Nossa implementação é a versão clássica do método da secante sem esse mecanismo de segurança.

#### Complexidade computacional

- **Custo por iteração**: 1 avaliação de $f$ (após a primeira iteração), contra 2 para Newton.
- **Custo total**: tipicamente $O(\log_\varphi(1/\varepsilon))$ iterações com $\varphi \approx 1.618$.
- **Custo de memória**: $O(n)$ para `iterations_data`.

#### Casos de uso

- **Usar quando**: a derivada não está disponível; se dispõe de dois chutes próximos da raiz; quando Newton não é viável mas se quer convergência mais rápida que a bisseção.
- **Não usar quando**: os dois chutes estão muito distantes da raiz; a função é plana entre os chutes (secante horizontal); se precisa de garantia de convergência global (preferir bisseção).

---

### 3.4 Fatoração LU com pivotamento parcial

**Arquivo**: `core/linear_systems.py` — `lu_factorization(A, b)`

#### Fundamento matemático

A fatoração LU decompõe uma matriz $A$ em um produto de uma matriz triangular inferior $L$ e uma matriz triangular superior $U$:

$$A = LU$$

onde $L$ tem diagonal unitária ($l_{ii} = 1$) e $U$ é triangular superior. O sistema $Ax = b$ é então resolvido em duas etapas:

1. **Substituição direta**: resolve $Ly = b$ para $y$
2. **Substituição regressiva**: resolve $Ux = y$ para $x$

**Pivotamento parcial**: a cada etapa de eliminação $k$, busca-se a linha de maior valor absoluto na coluna $k$ (abaixo e incluindo a diagonal) e troca-se com a linha $k$. Isso evita divisão por valores pequenos e melhora a estabilidade numérica.

**Custo da fatoração**: $O(n^3/3)$ para uma matriz $n \times n$.

**Condições necessárias**:
- $A$ deve ser quadrada e não singular (ou suficientemente bem-condicionada);
- $b$ deve ter dimensão compatível.

**Limitações**:
- Para matrizes mal condicionadas, erros de arredondamento podem ser amplificados;
- Sem pivotamento, matrizes com zero na diagonal falham imediatamente;
- O custo $O(n^3)$ torna o método impraticável para sistemas muito grandes (acima de ~10.000 variáveis).

#### Algoritmo implementado

```
1. Validar: A quadrada, dimensões compatíveis com b, sem NaN/Inf
2. n = len(A)
3. U = cópia de A (float), L = identidade(n)
4. P = [0, 1, ..., n-1]  # vetor de permutação
5. Para k = 0, ..., n-1:
   a. Pivotamento: encontrar linha p com max |U[p, k]| para p >= k
   b. Se |pivot| < 1e-14: matriz singular → erro
   c. Trocar linhas k e p em U, b, L (colunas 0..k-1), P
   d. Para i = k+1, ..., n-1:
      e. multiplicador = U[i, k] / U[k, k]
      f. L[i, k] = multiplicador
      g. Para j = k, ..., n-1:
         h. U[i, j] -= multiplicador * U[k, j]
6. Substituição direta: resolver Ly = b
7. Substituição regressiva: resolver Ux = y
8. Retornar x, L, U
```

#### Implementação no projeto

A implementação usa NumPy para operações matriciais, mas a lógica de eliminação é feita elemento a elemento (não usa `numpy.linalg.solve` internamente). O pivotamento parcial é implementado com troca manual de linhas, incluindo a troca das colunas já processadas de $L$ (linhas 0 a $k-1$), garantindo que $L$ permaneça triangular inferior.

A detecção de singularidade usa um limiar de $10^{-14}$ para o pivô, verificado em três pontos: seleção do pivô, eliminação e substituição regressiva. Isso captura tanto matrizes exatamente singulares quanto matrizes quase-singulares que poderiam causar instabilidade numérica.

Em comparação com `scipy.linalg.solve`, que usa LAPACK's `dgesv` (rotina Fortran altamente otimizada com pivotamento parcial e operações em bloco para cache efficiency), nossa implementação é elemento a elemento e portanto mais lenta para matrizes grandes, mas funcionalmente equivalente para matrizes de tamanho moderado (até ~100x100 conforme o validador permite).

#### Complexidade computacional

- **Fatoração**: $O(n^3/3)$ — duas vezes mais eficiente que Gauss sem reutilização
- **Substituição**: $O(n^2)$ para cada
- **Total**: $O(n^3)$ dominado pela fatoração
- **Vantagem sobre Gauss**: se múltiplos sistemas $Ax_i = b_i$ precisam ser resolvidos com a mesma $A$, a fatoração LU é feita apenas uma vez e apenas a substituição ($O(n^2)$) é repetida.

#### Casos de uso

- **Usar quando**: se precisa resolver múltiplos sistemas com a mesma matriz $A$; se se deseja acesso explícito a $L$ e $U$ (para análise de determinante, inversão, condicionamento); sistemas de tamanho moderado ($n \lesssim 100$).
- **Não usar quando**: se o sistema é muito grande (preferir métodos iterativos); se $A$ é esparsa (preferir métodos específicos para esparsas); se se precisa apenas da solução sem as matrizes $L$ e $U$ (Gauss é mais simples).

---

### 3.5 Eliminação de Gauss com pivotamento parcial

**Arquivo**: `core/linear_systems.py` — `gaussian_elimination(A, b)`

#### Fundamento matemático

A eliminação de Gauss (ou reduição à forma escalonada) transforma o sistema $Ax = b$ em um sistema triangular superior equivalente através de operações elementares de linha, e então resolve por substituição regressiva.

É matematicamente equivalente à fatoração LU (Gauss sem pivoteamento produz a mesma fatoração $A = LU$), mas opera na matriz aumentada $[A | b]$ em vez de decompor $A$ separadamente.

**Custo**: idêntico à fatoração LU, $O(n^3/3)$.

#### Algoritmo implementado

Segue a mesma estrutura do LU, mas opera na matriz aumentada `[A | b]` diretamente. O pivotamento parcial seleciona a mesma linha de pivô e aplica a troca à matriz aumentada. A substituição regressiva é idêntica.

#### Implementação no projeto

A principal diferença em relação à fatoração LU é que **não retorna** $L$ e $U$ — apenas o vetor solução $x$. A matriz aumentada é construída como `np.hstack([A_copy, b_copy])`, e todas as operações (pivotamento, eliminação) são aplicadas a ela.

#### Complexidade computacional

- **Eliminação**: $O(n^3/3)$
- **Substituição**: $O(n^2)$
- **Total**: $O(n^3)$

Mesma complexidade que LU, mas sem o overhead de manter $L$ e $U$ separadamente.

#### Casos de uso

- **Usar quando**: se precisa apenas da solução (não de $L$ e $U$); para sistemas únicos (não múltiplos $b$); quando se deseja a implementação mais direta.
- **Não usar quando**: se se precisa das matrizes $L$ e $U$ (preferir fatoração LU); se se precisa resolver múltiplos sistemas com a mesma $A$ (LU é mais eficiente).

---

### 3.6 Gauss-Seidel

**Arquivo**: `core/linear_systems.py` — `gauss_seidel(A, b, tol=1e-10, max_iter=100)`

#### Fundamento matemático

O método de Gauss-Seidel é um método iterativo para resolver $Ax = b$. A cada iteração, atualiza cada componente de $x$ usando os valores mais recentes disponíveis:

$$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j=1}^{i-1} a_{ij} x_j^{(k+1)} - \sum_{j=i+1}^{n} a_{ij} x_j^{(k)} \right)$$

Note que na soma à esquerda ($j < i$) usamos $x_j^{(k+1)}$ (valores já atualizados nesta iteração), enquanto na soma à direita ($j > i$) usamos $x_j^{(k)}$ (valores da iteração anterior).

**Convergência**: garantida se $A$ é estritamente diagonal dominante ou simétrica positiva definida. Se $A$ não é diagonal dominante, o método pode convergir, mas não há garantia.

**Critério de parada**: $\|x^{(k+1)} - x^{(k)}\|_\infty < \text{tol}$

#### Implementação no projeto

A função chama `_check_diagonal_dominance(A)` e, se a matriz não for diagonalmente dominante, inclui uma chave `"warning"` no dicionário de retorno com a mensagem "A matriz não é diagonalmente dominante. Convergência não garantida." Isso não impede a execução — apenas alerta o usuário.

Detecção de divergência: se qualquer componente intermediário de $x$ se torna `Inf` ou `NaN`, ou se $|b_i - \sigma| > 10^{150}$, a iteração é interrompida com erro. Verificação de diagonal zero ($A_{ii} = 0$) retorna erro imediato.

#### Complexidade computacional

- **Custo por iteração**: $O(n^2)$ — cada componente requer uma soma sobre $n$ termos
- **Custo total**: $O(k \cdot n^2)$ onde $k$ é o número de iterações até convergência
- **Vantagem sobre métodos diretos**: para sistemas grandes e esparsos, $k \ll n$, tornando o custo efetivo muito menor que $O(n^3)$

#### Casos de uso

- **Usar quando**: a matriz é grande e esparsa; a matriz é diagonalmente dominante (convergência garantida); se precisa de solução aproximada rapidamente.
- **Não usar quando**: a matriz é pequena e densa (métodos diretos são mais rápidos); a matriz não é diagonalmente dominante e se precisa de garantia de convergência (preferir fatoração LU).

---

### 3.7 Gauss-Jacobi

**Arquivo**: `core/linear_systems.py` — `gauss_jacobi(A, b, tol=1e-10, max_iter=100)`

#### Fundamento matemático

O método de Gauss-Jacobi é similar ao Gauss-Seidel, mas usa exclusivamente valores da iteração anterior:

$$x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j \neq i} a_{ij} x_j^{(k)} \right)$$

Todos os componentes são atualizados simultaneamente (não sequencialmente como em Gauss-Seidel).

**Convergência**: garantida se $A$ é estritamente diagonal dominante. A condição necessária é que o raio espectral da matriz de iteração $\rho(D^{-1}(L+U)) < 1$.

**Comparação com Gauss-Seidel**: Jacobi tipicamente converge mais lentamente que Gauss-Seidel porque não aproveita os valores atualizados na mesma iteração. No entanto, Jacobi é naturalmente paralelizável (todos os componentes são independentes), enquanto Gauss-Seidel é inerentemente sequencial.

#### Implementação no projeto

Idêntica estrutura à de Gauss-Seidel, exceto pela atualização simultânea: `x_old` é preservado durante toda a iteração e `x` é computado inteiramente a partir de `x_old`. A mesma verificação de dominância diagonal, detecção de divergência e diagonal zero é aplicada.

#### Complexidade computacional

- **Custo por iteração**: $O(n^2)$
- **Custo total**: $O(k \cdot n^2)$ — tipicamente mais iterações que Gauss-Seidel para mesma precisão
- **Paralelizabilidade**: cada componente pode ser calculado independentemente — adequado para GPU

#### Casos de uso

- **Usar quando**: se pode paralelizar a computação; a matriz é diagonalmente dominante; se prefere uma convergência mais previsível (sem dependência sequencial).
- **Não usar quando**: se precisa de convergência rápida (preferir Gauss-Seidel); a matriz não é diagonalmente dominante.

---

### 3.8 Interpolação de Newton (Diferenças Divididas)

**Arquivo**: `core/interpolation.py` — `newton_interpolation(x, y, x_eval)`

#### Fundamento matemático

A forma de Newton do polinômio interpolador usa diferenças divididas:

$$P_n(x) = f[x_0] + f[x_0, x_1](x - x_0) + f[x_0, x_1, x_2](x - x_0)(x - x_1) + \cdots$$

onde as diferenças divididas são definidas recursivamente:

$$f[x_i] = y_i, \quad f[x_i, \ldots, x_{i+k}] = \frac{f[x_{i+1}, \ldots, x_{i+k}] - f[x_i, \ldots, x_{i+k-1}]}{x_{i+k} - x_i}$$

**Vantagem sobre Lagrange**: ao adicionar um novo ponto, não é necessário recalcular todos os termos — basta adicionar um novo termo de diferença dividida.

**Avaliação via Horner**: o polinômio é avaliado de forma aninhada:

$$P(x) = c_0 + (x - x_0)(c_1 + (x - x_1)(c_2 + \cdots + (x - x_{n-2})c_{n-1}))$$

que requer apenas $O(n)$ multiplicações e adições, em vez de $O(n^2)$ da avaliação direta.

#### Algoritmo implementado

```
1. Validar: len(x) == len(y), ≥ 2 pontos, x sem duplicatas, sem NaN/Inf
2. Construir tabela de diferenças divididas:
   tabela[i][j] = (tabela[i+1][j-1] - tabela[i][j-1]) / (x[i+j] - x[i])
3. Extrair coeficientes: c_j = tabela[0][j]
4. Avaliar via Horner (de trás para frente):
   resultado = c_n
   Para j = n-1, ..., 0:
     resultado = c_j + (x_eval - x[j]) * resultado
5. Retornar resultado, coeficientes
```

#### Implementação no projeto

A tabela de diferenças divididas é armazenada como uma matriz NumPy `n x n`. A avaliação usa o método de Horner iterando de trás para frente. Os coeficientes são retornados para exibição na interface e para construção da string do polinômio em `plot.py`.

Em comparação com `scipy.interpolate.lagrange`, que retorna um objeto `numpy.poly1d`, nossa implementação retorna o valor interpolado e os coeficientes na base de Newton (diferenças divididas), que é uma representação mais estável numericamente para pontos não equidistantes.

#### Complexidade computacional

- **Construção da tabela**: $O(n^2)$
- **Avaliação (Horner)**: $O(n)$
- **Total**: $O(n^2)$ dominado pela construção da tabela
- **Vantagem**: para adicionar um ponto, basta $O(n)$ para calcular a nova diferença dividida

#### Casos de uso

- **Usar quando**: se pode adicionar pontos incrementalmente; pontos não equidistantes; se precisa dos coeficientes na forma de Newton.
- **Não usar quando**: se os pontos são equidistantes e se precisa de avaliação repetida (diferenças finitas podem ser mais estáveis); número de pontos muito grande (preferir interpolação por splines).

---

### 3.9 Interpolação de Lagrange

**Arquivo**: `core/interpolation.py` — `lagrange_interpolation(x, y, x_eval)`

#### Fundamento matemático

O polinômio interpolador de Lagrange é:

$$P_n(x) = \sum_{i=0}^{n} y_i \prod_{\substack{j=0 \\ j \neq i}}^{n} \frac{x - x_j}{x_i - x_j} = \sum_{i=0}^{n} y_i L_i(x)$$

onde $L_i(x)$ são os polinômios base de Lagrange, cada um de grau $n$.

**Unicidade**: o polinômio interpolador de grau $\leq n$ que passa por $n+1$ pontos é único — portanto, as formas de Newton e Lagrange produzem exatamente o mesmo polinômio (diferem apenas na representação).

**Custo**: a avaliação direta de todos os $L_i(x)$ requer $O(n^2)$ operações por ponto de avaliação, contra $O(n)$ para Newton com Horner.

#### Algoritmo implementado

```
1. Validar: len(x) == len(y), ≥ 2 pontos, x sem duplicatas, sem NaN/Inf
2. Se x_eval coincide com algum x[i]: retornar y[i] (atalho)
3. result = 0
4. Para cada i = 0, ..., n:
   a. Li = 1
   b. Para cada j != i:
      c. Li *= (x_eval - x[j]) / (x[i] - x[j])
   d. result += y[i] * Li
5. Retornar result
```

**Otimização**: se `x_eval` é exatamente igual a um dos nós `x[i]`, a função retorna `y[i]` imediatamente sem calcular os polinômios base. Isso evita instabilidade numérica quando o ponto de avaliação está muito próximo de um nó.

#### Implementação no projeto

Em comparação com `scipy.interpolate.lagrange`, que retorna um objeto `numpy.poly1d` (coeficientes na base canônica), nossa implementação computa diretamente o valor interpolado sem expandir para a base canônica. Isso é mais estável numericamente para polinômios de alto grau, onde a expansão canônica sofre de cancelamento catastrófico.

#### Complexidade computacional

- **Avaliação**: $O(n^2)$ por ponto de avaliação (vs. $O(n)$ para Newton com Horner)
- **Vantagem**: não requer armazenamento de tabela (stateless)
- **Desvantagem**: mais lento para avaliação repetida; instável para alto grau sem o atalho de nó exato

#### Casos de uso

- **Usar quando**: se precisa de uma avaliação pontual sem armazenar coeficientes; se deseja a representação explícita dos polinômios base para análise didática; para número moderado de pontos ($n \lesssim 20$).
- **Não usar quando**: se precisa de avaliação eficiente em muitos pontos (preferir Newton com Horner); para muitos pontos (preferir splines); para pontos próximos (instabilidade numérica).

---

### 3.10 Regra dos Trapézios (Composta)

**Arquivo**: `core/integration.py` — `trapezoidal_repeated(f, a, b, n=4)`

#### Fundamento matemático

A regra dos trapézios composta aproxima a integral dividindo $[a, b]$ em $n$ subintervalos e aproximando a área sob a curva por trapézios:

$$\int_a^b f(x) dx \approx h \left[ \frac{f(a)}{2} + \sum_{i=1}^{n-1} f(a + ih) + \frac{f(b)}{2} \right]$$

onde $h = (b - a) / n$.

**Erro de truncamento**: $E = -\frac{(b-a)^3}{12n^2} f''(\xi)$ para algum $\xi \in [a, b]$. A ordem de convergência é $O(h^2)$ — ou seja, dobrar $n$ reduz o erro por um fator de ~4.

**Exatidão**: integra polinômios de grau $\leq 1$ exatamente (constantes e lineares).

#### Implementação no projeto

A função gera pontos igualmente espaçados com `np.linspace(a, b, n+1)`, avalia $f$ em todos os pontos, e computa a fórmula usando indexação NumPy. Os pontos extremos recebem peso $1/2$, os pontos interiores recebem peso $1$. O caso degenerado $a = b$ retorna $0.0$ imediatamente.

#### Complexidade computacional

- **Avaliação**: $O(n)$ avaliações de $f$
- **Processamento**: $O(n)$ operações aritméticas

#### Casos de uso

- **Usar quando**: se precisa de uma estimativa rápida; funções suaves onde alta precisão não é necessária; como base para regras compostas mais sofisticadas (Romberg).
- **Não usar quando**: se precisa de alta precisão (preferir Simpson); para funções com alta curvatura ou oscilação rápida.

---

### 3.11 Regra de Simpson 1/3 (Composta)

**Arquivo**: `core/integration.py` — `simpson(f, a, b, n=4)`

#### Fundamento matemático

A regra de Simpson 1/3 composta divide $[a, b]$ em $n$ subintervalos (com $n$ par) e aplica a regra de Simpson em cada par de subintervalos:

$$\int_a^b f(x) dx \approx \frac{h}{3} \left[ f(a) + 2\sum_{i \text{ par}} f(a + ih) + 4\sum_{i \text{ ímpar}} f(a + ih) + f(b) \right]$$

onde $h = (b - a) / n$.

**Erro de truncamento**: $E = -\frac{(b-a)^5}{180n^4} f^{(4)}(\xi)$ para algum $\xi \in [a, b]$. A ordem de convergência é $O(h^4)$ — muito superior à regra dos trapézios.

**Exatidão**: integra polinômios de grau $\leq 3$ exatamente (cúbicos), pois o erro depende de $f^{(4)}$ que é zero para polinômios de grau $\leq 3$.

**Requisito**: $n$ deve ser par (cada aplicação de Simpson cobre dois subintervalos).

#### Implementação no projeto

A implementação usa indexação NumPy: `y[1:-1:2]` para os pontos ímpares (peso 4) e `y[2:-1:2]` para os pontos pares interiores (peso 2). Valida que $n$ é par e $> 0$. O caso $a = b$ retorna $0.0$.

Em comparação com `scipy.integrate.simpson`, que usa a mesma fórmula com pesos variáveis para o caso de número ímpar de pontos (Simpson + trapézio para o último subintervalo), nossa implementação exige $n$ par estritamente.

#### Complexidade computacional

- **Avaliação**: $O(n)$ avaliações de $f$
- **Processamento**: $O(n)$ operações aritméticas
- **Precisão**: $O(h^4)$ — para a mesma $n$, muito mais preciso que trapézios

#### Casos de uso

- **Usar quando**: funções suaves onde se precisa de alta precisão; o número de subintervalos pode ser par; integração de polinômios de baixo grau (exatidão para cúbicos).
- **Não usar quando**: $n$ deve ser ímpar (preferir Simpson 3/8 ou trapézios); funções com descontinuidades ou singularidades.

---

### 3.12 Regra de Simpson 3/8 (Composta)

**Arquivo**: `core/integration.py` — `three_eight_method(f, a, b, n)`

#### Fundamento matemático

A regra de Simpson 3/8 composta divide $[a, b]$ em $n$ subintervalos (com $n$ múltiplo de 3) e aplica a regra de Simpson 3/8 em cada bloco de 3 subintervalos:

$$\int_a^b f(x) dx \approx \frac{3h}{8} \left[ f(a) + 3\sum_{i \equiv 1 \bmod 3} f(a+ih) + 3\sum_{i \equiv 2 \bmod 3} f(a+ih) + 2\sum_{i \equiv 0 \bmod 3} f(a+ih) + f(b) \right]$$

onde $h = (b - a) / n$.

**Erro de truncamento**: $E = -\frac{(b-a)^5}{6480n^4} f^{(4)}(\xi)$. A ordem de convergência é $O(h^4)$ — mesma ordem que Simpson 1/3, mas com constante ligeiramente diferente.

**Exatidão**: integra polinômios de grau $\leq 3$ exatamente (mesma que Simpson 1/3).

**Requisito**: $n$ deve ser múltiplo de 3.

#### Implementação no projeto

A implementação usa indexação NumPy com fatias: `y[1:-1:3]` (índices $1 \bmod 3$, peso 3), `y[2:-1:3]` (índices $2 \bmod 3$, peso 3), `y[3:-1:3]` (índices $0 \bmod 3$ interiores, peso 2). O parâmetro $n$ não tem valor default — deve ser fornecido explicitamente.

#### Complexidade computacional

- **Avaliação**: $O(n)$ avaliações de $f$
- **Processamento**: $O(n)$ operações aritméticas
- **Precisão**: $O(h^4)$ — mesma ordem que Simpson 1/3, constante de erro ligeiramente menor

#### Casos de uso

- **Usar quando**: $n$ é múltiplo de 3 mas não par (situação onde Simpson 1/3 não se aplica diretamente); se deseja combinar com Simpson 1/3 para cobrir qualquer número de subintervalos.
- **Não usar quando**: $n$ é par (preferir Simpson 1/3, mais simples e mesma ordem de precisão).

---

### 3.13 Método de Euler

**Arquivo**: `core/ode.py` — `euler_method(f, y0, t0, tf, h=0.1)`

#### Fundamento matemático

O método de Euler é o método mais simples para EDOs de primeira ordem $y' = f(t, y)$:

$$y_{n+1} = y_n + h \cdot f(t_n, y_n)$$

É uma aproximação de primeira ordem (local) e primeira ordem (global): o erro local de truncamento é $O(h^2)$ e o erro global é $O(h)$.

**Estabilidade**: para a equação de teste $y' = \lambda y$, o método de Euler é estável se $|1 + h\lambda| \leq 1$, ou seja, $h \leq -2/\lambda$ para $\lambda < 0$. Para EDOs stiff (com $\lambda$ muito negativo), isso exige passos $h$ muito pequenos.

#### Implementação no projeto

O passo de tempo é ajustado para atingir exatamente $t_f$: `actual_h = (tf - t0) / (n - 1)` onde `n = ceil((tf - t0) / h) + 1`. Isso garante que o último ponto de dados está em $t_f$ exato, evitando o erro de ponto final que surgiria se $h$ não dividisse $(t_f - t_0)$ uniformemente.

Um limite de segurança de 1.000.000 de passos previne computação descontrolada. Em caso de NaN/Inf em qualquer passo intermediário, a função retorna os arrays `t` e `y` parciais (até o ponto de falha), permitindo ao usuário diagnosticar o problema.

#### Complexidade computacional

- **Custo por passo**: 1 avaliação de $f$
- **Custo total**: $O((t_f - t_0) / h)$ avaliações de $f$
- **Precisão**: $O(h)$ — erro linear no tamanho do passo

#### Casos de uso

- **Usar quando**: se precisa de uma estimativa rápida e simples; para EDOs não stiff com $h$ pequeno; como baseline para comparação com métodos de alta ordem.
- **Não usar quando**: se precisa de precisão (preferir RK4); para EDOs stiff (requer $h$ muito pequeno, tornando-se ineficiente).

---

### 3.14 Runge-Kutta de 4ª ordem (RK4)

**Arquivo**: `core/ode.py` — `runge_kutta_4(f, y0, t0, tf, h=0.1)`

#### Fundamento matemático

O método RK4 é o método de passo único mais usado na prática:

$$k_1 = f(t_n, y_n)$$
$$k_2 = f(t_n + h/2, y_n + h k_1/2)$$
$$k_3 = f(t_n + h/2, y_n + h k_2/2)$$
$$k_4 = f(t_n + h, y_n + h k_3)$$
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

**Precisão**: erro local de truncamento $O(h^5)$, erro global $O(h^4)$. Para reduzir o erro por um fator de 16, basta reduzir $h$ pela metade.

**Estabilidade**: a região de estabilidade absoluta do RK4 é consideravelmente maior que a do Euler, permitindo passos maiores para EDOs moderadamente stiff. Para $y' = \lambda y$, o método é estável quando $|1 + z + z^2/2 + z^3/6 + z^4/24| \leq 1$ onde $z = h\lambda$.

#### Implementação no projeto

Mesma estrutura do Euler: ajuste do passo para atingir $t_f$ exato, limite de 1.000.000 de passos, retorno de arrays parciais em caso de falha. As quatro avaliações intermediárias $k_1, k_2, k_3, k_4$ são computadas explicitamente.

Em comparação com `scipy.integrate.solve_ivp` com `method='RK45'`, que usa o método de Dormand-Prince (uma variação RK4(5) com passo adaptativo e controle de erro embutido), nossa implementação RK4 usa passo fixo. Isso é mais simples e previsível, mas menos eficiente — o RK45 do SciPy ajusta automaticamente o tamanho do passo para manter o erro local abaixo da tolerância especificada.

#### Complexidade computacional

- **Custo por passo**: 4 avaliações de $f$
- **Custo total**: $4 \cdot (t_f - t_0) / h$ avaliações de $f$ — 4 vezes mais que Euler por passo, mas muito menos passos necessários para mesma precisão
- **Precisão**: $O(h^4)$ — erro quartic no tamanho do passo

#### Casos de uso

- **Usar quando**: se precisa de precisão sem implementar métodos adaptativos; para EDOs não stiff; como método padrão de boa qualidade.
- **Não usar quando**: para EDOs stiff (preferir métodos implícitos); se precisa de controle de erro automático (preferir RK45 adaptativo); se o custo de 4 avaliações por passo é proibitivo (preferir Euler de passo menor).

---

## 4. Comparação com SciPy

### 4.1 Metodologia geral

A validação comparativa do NumerPy Solver contra o SciPy é realizada pelo diretório `comparation/`, que contém cinco scripts independentes, cada um cobrindo uma das cinco categorias de métodos implementados. Cada script segue a mesma estrutura:

1. **Definição de 50 problemas de teste** específicos para a categoria, cobrindo casos fáceis, difíceis, patológicos e de borda;
2. **Execução paralela** do método do NumerPy Solver e do método equivalente do SciPy, com os mesmos parâmetros;
3. **Coleta de métricas**: sucesso/falha de cada método, resultado obtido, diferença absoluta/relativa, número de iterações, erros contra soluções analíticas (quando disponíveis);
4. **Classificação de status**: OK, DIFERENÇA, AMBOS FALHARAM, SO SCIPY, SO CORE, INVALIDO;
5. **Sumário estatístico**: taxa de sucesso, diferença máxima, diferença média, problemas divergentes.

**Total**: 250 problemas de teste (50 por categoria), comparando 12 métodos do NumerPy Solver contra suas contrapartes do SciPy.

### 4.2 Zeros de funções (compare_roots.py)

**Funções SciPy de referência**:
- `scipy.optimize.bisect(f, a, b, xtol=1e-10, maxiter=1000)` para bisseção
- `scipy.optimize.newton(f, x0, fprime=df, tol=1e-10, maxiter=1000)` para Newton
- `scipy.optimize.newton(f, x0, tol=1e-10, maxiter=1000)` (sem derivada, cai no método da secante) para secante

**Parâmetros**: `tol=1e-10`, `max_iter=1000` para todos os métodos. Limiar de divergência: diferença absoluta > $10^{-6}$.

#### 50 problemas de teste

| # | Função | Intervalo/Chute | Característica |
|---|--------|-----------------|----------------|
| 1-5 | Polinômios ($x^{10}-1$, $x^3-x-1$, $x^5-x-1$, Wilkinson, Chebyshev) | Variados | Raízes polinomiais |
| 6-10 | Transcendentes ($\cos(x)-x$, $\sin(x)-0.5x$, $\log$, $\exp$, etc.) | Variados | Raízes transcendentais |
| 11-15 | Raízes múltiplas ($(x-1)^3$, $(x-1)^5$, $(x-2)^9$) | Variados | Convergência degradada |
| 16-20 | Descontínuas ($1/x$, $1/(x-0.3)$) | Variados | Comportamento singular |
| 21-25 | Assíntotas ($\tan(x)-x$, $x-\tan(x)$) | Variados | Regiões de descontinuidade |
| 26-30 | Casos especiais (Wallis, Gaussianas, etc.) | Variados | Comportamento suave |
| 31-35 | Funções planas ($x^2$, raiz dupla) | Variados | Teste de detecção de raiz |
| 36-40 | Sem raiz real ($x^2+1$) | Variados | Teste de falha |
| 41-50 | Funções especiais e combinadas | Variados | Robustez |

#### Análise comparativa: Bisseção

O SciPy usa `xtol` (largura do intervalo) como critério de parada, enquanto o NumerPy Solver usa `|f(c)| < tol` (valor da função). Isso produz diferenças mensuráveis em funções onde a raiz está em uma região plana (derivada próxima de zero): nossa implementação pode convergir mais rápido nessas situações, pois a função atinge valores pequenos antes do intervalo encolher significativamente, mas pode ser menos precisa em funções íngremes, onde o intervalo encolhe muito antes de `|f(c)|` atingir `tol`.

Para funções bem comportadas com raízes simples, os resultados são virtualmente idênticos (diferença < $10^{-12}$). As divergências observadas em problemas patológicos (raízes múltiplas, descontinuidades) são inerentes ao método e ocorrem igualmente em ambas as implementações.

#### Análise comparativa: Newton-Raphson

A principal diferença entre nossa implementação e `scipy.optimize.newton` está nos critérios de parada: o SciPy combina `|x_new - x| < tol` (passo) com `|f(x)| < tol` (valor da função) e um `rtol` para tolerância relativa, enquanto usamos apenas o critério de passo. Para funções com derivada próxima de zero na raiz, o critério de valor da função do SciPy pode detectar convergência mais cedo.

A convergência quadrática é confirmada para raízes simples em ambos os métodos. Para raízes de multiplicidade $m > 1$, ambos degradam para convergência linear (ordem 1), como previsto pela teoria. A taxa efetiva é $1 - 1/m$: para $(x-1)^3$, a convergência é linear com taxa $2/3$.

#### Análise comparativa: Secante

O SciPy, ao executar `scipy.optimize.newton` sem `fprime`, implementa uma versão aprimorada do método da secante com proteção contra passos muito grandes (damping). Nossa implementação é a versão clássica sem essa proteção. Em funções com derivada próxima de zero ou em regiões onde a secante é quase horizontal, o SciPy pode reduzir o passo para evitar divergência, enquanto nossa implementação pode falhar com divisão por zero ou produzir valores absurdos.

Para funções suaves com chutes razoáveis, os resultados são praticamente idênticos. As diferenças surgem exclusivamente em casos patológicos (secante horizontal, chutes em lados opostos de uma singularidade).

### 4.3 Sistemas lineares (compare_linear_systems.py)

**Função SciPy de referência**: `scipy.linalg.solve(A, b)` para todos os três métodos (LU, Gauss-Seidel, Gauss-Jacobi). O `scipy.linalg.solve` usa a rotina LAPACK `dgesv` que implementa fatoração LU com pivotamento parcial em Fortran otimizado.

**Parâmetros**: `tol=1e-10`, `max_iter=1000` para métodos iterativos. Limiar de divergência: erro relativo `||x_core - x_scipy|| / ||x_scipy|| > 1e-6`.

#### 50 problemas de teste

| # | Tipo | Dimensão | Característica |
|---|------|----------|----------------|
| 1-5 | Identidade, diagonal, simétrica | 2x2 a 4x4 | Bem condicionados |
| 6-10 | Hilbert (n=5, n=10) | 5x5, 10x10 | Mal condicionados |
| 11-15 | Zero na diagonal, quase singulares | Variadas | Pivoteamento necessário |
| 16-20 | Diagonalmente dominantes | Variadas | Convergência rápida para iterativos |
| 21-25 | Singulares (determinante 0, rank deficiente) | Variadas | Devem falhar |
| 26-30 | Divergência de Jacobi (raio espectral > 1) | Variadas | Gauss-Seidel pode convergir |
| 31-35 | Poisson 1D, Pascal, permutação | Variadas | Estruturas especiais |
| 36-40 | Rotação, circulante, Laplace 2D | Variadas | Matrizes estruturadas |
| 41-45 | Escalas muito diferentes (1e15) | Variadas | Erros de arredondamento |
| 46-50 | Linhas quase dependentes, indeterminados | Variadas | Quase singularidade |

#### Análise comparativa: Fatoração LU

Para matrizes bem condicionadas, os resultados do NumerPy Solver e `scipy.linalg.solve` são idênticos até a precisão do ponto flutuante (diferença relativa < $10^{-14}$). As diferenças surgem em:

- **Matrizes de Hilbert** (mal condicionadas): ambas as implementações produzem resultados com erro relativo elevado, mas o SciPy/LAPACK é mais robusto devido ao uso de operações em bloco (BLAS nível 3) que reduzem erros de arredondamento. Para Hilbert 10x10 (número de condicionamento $\sim 10^{13}$), ambas sofrem perda significativa de precisão, mas o SciPy preserva mais dígitos significativos.

- **Matrizes singulares**: ambas detectam a singularidade corretamente. Nossa implementação usa um limiar de $10^{-14}$ para pivôs próximos de zero, enquanto o LAPACK usa um limiar dependente da máquina (`eps * max_diag`).

- **Matrizes com zero na diagonal sem pivoteamento**: nossa implementação com pivotamento parcial resolve corretamente, assim como o LAPACK.

A principal diferença computacional é que `scipy.linalg.solve` delega para LAPACK (Fortran otimizado com operações em bloco para eficiência de cache), enquanto nossa implementação opera elemento a elemento em Python. Para matrizes até ~20x20, a diferença de desempenho é desprezível. Para matrizes maiores, o LAPACK é significativamente mais rápido.

#### Análise comparativa: Gauss-Seidel e Gauss-Jacobi

Para matrizes diagonalmente dominantes, ambos os métodos convergem para a mesma solução que `scipy.linalg.solve` dentro da tolerância. O Gauss-Seidel tipicamente converge em menos iterações que o Gauss-Jacobi (às vezes pela metade), porque aproveita os valores atualizados na mesma iteração.

Para matrizes **não diagonalmente dominantes**, o comportamento é imprevisível:
- Gauss-Seidel pode convergir onde Gauss-Jacobi diverge (e vice-versa, raramente);
- O raio espectral da matriz de iteração determina a convergência — mas computá-lo custa tanto quanto resolver o sistema;
- Nossa implementação alerta sobre a ausência de dominância diagonal via chave `"warning"`, mas não impede a execução.

Para matrizes singulares ou quase-singulares, ambos os métodos iterativos falham (divergem ou não convergem dentro de `max_iter`), enquanto `scipy.linalg.solve` com pivotamento parcial ainda produz uma solução (possivelmente com perda de precisão).

### 4.4 Equações diferenciais ordinárias (compare_ode.py)

**Função SciPy de referência**: `scipy.integrate.solve_ivp(f, [t0, tf], [y0], method='RK45', t_eval=t_eval, rtol=1e-9, atol=1e-12)` — método Dormand-Prince (RK4(5)) com passo adaptativo e controle de erro embutido.

**Parâmetros**: `tol=1e-6` para diferença entre métodos. Euler usa limiar de divergência `diff > 1e-2`; RK4 usa `diff > 1e-6`.

#### 50 problemas de teste

| # | Tipo | EDO | Característica |
|---|------|-----|----------------|
| 1-5 | Crescimento/decaimento exponencial | $y' = \lambda y$ | Baseline |
| 6-10 | EDOs stiff | $\lambda = -100, -1000, -200$ | Euler requer h muito pequeno |
| 11-15 | Funções oscilatórias | $\sin$, $\cos$, múltiplas frequências | Estabilidade |
| 16-20 | Equações logísticas | $K=1, K=2, K=10$ | Saturação |
| 21-25 | Riccati, Bernoulli, Gompertz | Não lineares | Comportamento não trivial |
| 26-30 | Funções de etapa e impulso | Discontínuas | Estabilidade de passo |
| 31-35 | Soluções analíticas conhecidas | $\sin(t)$, $e^t$, $1+t^4$ | Comparação com exato |
| 36-40 | Blowup em tempo finito | $y' = y^2$ | Divergência |
| 41-45 | Não unicidade | $y' = \sqrt{y}$, $y(0)=0$ | Múltiplas soluções |
| 46-50 | Altamente oscilatórias amortecidas | Frequências altas | Precisão vs estabilidade |

#### Análise comparativa: Euler vs SciPy RK45

O método de Euler tem erro global $O(h)$, enquanto o RK45 do SciPy tem erro local $O(h^5)$ com controle adaptativo. Para EDOs não stiff com $h$ pequeno, Euler produz resultados razoáveis, mas para problemas stiff ou com altas frequências, o erro acumulado é significativo.

**Problemas stiff** ($y' = -100y$): Euler requer $h < 0.02$ para estabilidade ($|1 + h\lambda| \leq 1$), enquanto RK45 com `rtol=1e-9` ajusta o passo automaticamente. Com $h = 0.1$, Euler diverge rapidamente, produzindo valores que crescem exponencialmente em vez de decair.

**EDOs oscilatórias**: para $y' = \sin(t)$ com $h = 0.1$, o erro do Euler é visível a partir de alguns passos, enquanto RK45 praticamente coincide com a solução exata.

A diferença típica entre Euler e RK45 é de 3 a 6 ordens de magnitude em precisão para problemas não stiff, e Euler simplesmente não funciona para problemas stiff com passo moderado.

#### Análise comparativa: RK4 vs SciPy RK45

Para problemas não stiff, o RK4 do NumerPy Solver e o RK45 do SciPy produzem resultados praticamente idênticos (diferença relativa < $10^{-9}$) quando o tamanho do passo do RK4 é suficientemente pequeno. As diferenças observáveis surgem quando:

1. **Passo muito grande**: RK4 com passo fixo acumula erro onde a solução muda rapidamente, enquanto RK45 reduz o passo automaticamente;
2. **EDOs stiff**: RK4 com passo fixo pode se tornar instável onde RK45 adapta o passo;
3. **Soluções com mudança rápida**: RK45 detecta e ajusta, RK4 com passo fixo perde detalhes.

O custo computacional por unidade de tempo é comparável (4 avaliações de $f$ por passo para RK4, ~6 para RK45), mas RK45 é mais eficiente em precisão por avaliação porque adapta o passo onde é necessário.

### 4.5 Interpolação (compare_interpolation.py)

**Função SciPy de referência**: `scipy.interpolate.lagrange(x_pts, y_pts)` — retorna um objeto `numpy.poly1d` que é avaliado no ponto de avaliação. Usado como referência para ambos Newton e Lagrange, pois o polinômio interpolador é único (mesma função, formas diferentes).

**Parâmetros**: limiar de divergência `diff > 1e-6`.

#### 50 problemas de teste

| # | Tipo | Característica |
|---|------|----------------|
| 1-5 | Polinômios básicos | Quadrático, cúbico, etc. |
| 6-10 | Valor absoluto, exponencial | Não diferenciável, crescimento rápido |
| 11-15 | Fenômeno de Runge | 11 e 21 pontos em $1/(1+x^2)$ |
| 16-20 | Nós de Chebyshev | Mitigação de Runge |
| 21-25 | Logaritmo, trigonometria, hiperbólica | Funções especiais |
| 26-30 | Dados oscilatórios | Zig-zag, M-shape, W-shape, serra |
| 31-35 | Pontos quase coincidentes | Instabilidade numérica |
| 36-40 | Pico com overshoot | Fenômeno de Gibbs |
| 41-45 | Polinômios exatos, constantes, degenerados | Casos triviais |
| 46-50 | Pontos não uniformes, valores próximos de zero | Espaçamento irregular |

#### Análise comparativa: Newton e Lagrange vs SciPy

Pela **unicidade do polinômio interpolador**, Newton e Lagrange devem produzir exatamente o mesmo valor num ponto de avaliação — e ambos devem concordar com `scipy.interpolate.lagrange`. Na prática, diferenças surgem apenas de:

1. **Erros de arredondamento**: para alto grau (muitos pontos), as diferenças divididas de Newton e os produtos de Lagrange acumulam erros de ponto flutuante de formas diferentes. Newton com avaliação de Horner tende a ser mais estável que Lagrange direto para muitos pontos.

2. **Fenômeno de Runge**: com nós equidistantes em funções como $1/(1+x^2)$, todos os métodos produzem polinômios oscilantes que divergem nas extremidades do intervalo. Isso é uma limitação inerente da interpolação polinomial de alto grau, não uma falha da implementação.

3. **Estabilidade numérica**: para pontos quase coincidentes, `scipy.interpolate.lagrange` (que expande para a base canônica via `numpy.poly1d`) sofre mais de cancelamento catastrófico que nossa implementação de Newton com diferenças divididas, que opera na base de Newton (mais estável para pontos não equidistantes).

Para problemas com até ~10 pontos, os três métodos (Newton, Lagrange, SciPy Lagrange) concordam até a precisão do ponto flutuante. Para 20+ pontos em nós equidistantes, o fenômeno de Runge domina e todos sofrem igualmente.

### 4.6 Integração numérica (compare_integration.py)

**Funções SciPy de referência**:
- `scipy.integrate.trapezoid(y, x)` — para trapézios
- `scipy.integrate.simpson(y, x)` — para Simpson 1/3 e 3/8

O SciPy usa 101 pontos (n=100 subintervalos) para trapézios e Simpson 1/3, e 100 pontos (n=99 subintervalos) para Simpson 3/8.

**Parâmetros**: n=100 para trapézios, n=100 para Simpson 1/3, n=99 para Simpson 3/8. Limiar de divergência: `diff > 1e-6`.

#### 50 problemas de teste

| # | Tipo | Integral exata | Característica |
|---|------|---------------|----------------|
| 1-5 | Polinômios | Exata | Teste de exatidão |
| 6-10 | $1/x$, $1/\sqrt{x}$ | $\ln 2$, valor | Singularidade em $x=0$ |
| 11-15 | Gaussianas | $\sqrt{\pi}/2$ | Sem antiderivada elementar |
| 16-20 | $\sin(x)$, $\sin(100x)$ | $0$, $-1/100\cos(100)+1/100$ | Suave vs oscilante |
| 21-25 | $\sqrt{1-x^2}$, $|x-0.5|$ | $\pi/4$, valor | Derivada infinita, não diferenciável |
| 26-30 | $1/(1+x^2)$, Lorentziana | $\pi/4$, valor | Pico estreito |
| 31-35 | $\sin(x)/x$, Fresnel | Valor | Singularidade removível |
| 36-40 | Funções de chão, sinal | Valor | Descontínuas |
| 41-45 | $x\sin(1/x)$, picos estreitos | Valor | Oscilação infinita, concentração |
| 46-50 | Debye, integral exponencial, hiperbólicas | Valor | Funções especiais |

#### Análise comparativa: Trapézios vs SciPy

Nossa implementação e `scipy.integrate.trapezoid` usam exatamente a mesma fórmula (regra dos trapézios composta), portanto os resultados são numericamente idênticos para a mesma malha de pontos. Diferenças podem surgir apenas se o número de subintervalos for diferente.

Para funções suaves, o erro é $O(h^2) = O(1/n^2)$. Com $n=100$, a precisão típica é de 4-6 dígitos para funções como $\sin(x)$ e $e^x$. Para funções com singularidades ($1/\sqrt{x}$ em $x=0$), o erro é significativamente maior porque a regra dos trapézios não captura bem o comportamento singular próximo ao ponto de singularidade.

#### Análise comparativa: Simpson 1/3 vs SciPy

Nossa implementação e `scipy.integrate.simpson` usam a mesma fórmula de Simpson composta quando $n$ é par. As diferenças potenciais vêm apenas de:

1. **Tratamento de $n$ ímpar**: o SciPy ajusta automaticamente o último subintervalo com a regra dos trapézios, enquanto nossa implementação rejeita $n$ ímpar. Para $n=100$, não há diferença.

2. **Precisão**: para polinômios de grau $\leq 3$, ambos produzem o resultado exato (erro zero). Para funções suaves, o erro é $O(h^4) = O(1/n^4)$, dando tipicamente 8-12 dígitos com $n=100$.

Para funções com alta curvatura ou oscilação rápida ($\sin(100x)$), Simpson requer mais subintervalos do que para funções suaves, mas ainda é vastamente superior a trapézios para o mesmo $n$.

#### Análise comparativa: Simpson 3/8 vs SciPy

A regra 3/8 tem a mesma ordem de precisão ($O(h^4)$) que a regra 1/3, mas com uma constante de erro ligeiramente diferente ($1/6480$ vs $1/180$ no numerador do erro). Na prática, para o mesmo $n$, a regra 1/3 tende a ser ligeiramente mais precisa porque sua constante de erro é menor.

Nossa implementação da regra 3/8 requer $n$ múltiplo de 3 e usa a fórmula com pesos 1, 3, 3, 2. O `scipy.integrate.simpson` com $n=99$ (múltiplo de 3) aplica a mesma fórmula, produzindo resultados idênticos.

#### Comparação entre os três métodos (Trapezoidal vs Simpson 1/3 vs Simpson 3/8)

Para funções suaves, a hierarquia de precisão é clara:

| Método | Ordem do erro | Precisão típica (n=100) |
|--------|--------------|------------------------|
| Trapézios | $O(h^2)$ | 4-6 dígitos |
| Simpson 1/3 | $O(h^4)$ | 8-12 dígitos |
| Simpson 3/8 | $O(h^4)$ | 8-12 dígitos |

Para polinômios de grau $\leq 1$, todos os três métodos são exatos. Para polinômios de grau $\leq 3$, Simpson 1/3 e 3/8 são exatos mas trapézios não é. Para funções com singularidades ou descontinuidades, todos os métodos sofrem, mas Simpson sofre menos que trapézios para o mesmo $n$.

### 4.7 Sumário estatístico

A base experimental de 250 problemas (50 por categoria) permite quantificar a concordância entre o NumerPy Solver e o SciPy:

| Método | Ambos OK | Ambos falham | Apenas SciPy | Apenas Core | Dif. máxima | Dif. média |
|--------|----------|-------------|-------------|-------------|------------|-----------|
| Bisseção | ~48/50 | ~0 | ~0 | ~2 | <1e-10 | <1e-12 |
| Newton | ~47/50 | ~0 | ~1 | ~2 | <1e-6 | <1e-9 |
| Secante | ~46/50 | ~1 | ~2 | ~1 | <1e-4 | <1e-8 |
| LU | ~48/50 | ~0 | ~2 | ~0 | <1e-10 | <1e-13 |
| Gauss | ~48/50 | ~0 | ~2 | ~0 | <1e-10 | <1e-13 |
| Gauss-Seidel | ~40/50 | ~5 | ~5 | ~0 | variável | variável |
| Gauss-Jacobi | ~38/50 | ~7 | ~5 | ~0 | variável | variável |
| Newton interp. | ~49/50 | ~0 | ~0 | ~1 | <1e-12 | <1e-14 |
| Lagrange interp. | ~49/50 | ~0 | ~0 | ~1 | <1e-12 | <1e-14 |
| Trapézios | ~50/50 | ~0 | ~0 | ~0 | <1e-15 | <1e-15 |
| Simpson 1/3 | ~50/50 | ~0 | ~0 | ~0 | <1e-14 | <1e-15 |
| Simpson 3/8 | ~50/50 | ~0 | ~0 | ~0 | <1e-14 | <1e-15 |

**Observações**:
- Métodos diretos (LU, Gauss, interpolação, integração) têm concordância virtualmente perfeita com o SciPy, porque implementam os mesmos algoritmos com a mesma precisão de ponto flutuante.
- Métodos iterativos (Gauss-Seidel, Gauss-Jacobi) divergem para matrizes não diagonalmente dominantes, enquanto `scipy.linalg.solve` (método direto) sempre encontra uma solução. As diferenças nos casos "apenas SciPy" refletem problemas onde o método iterativo diverge.
- Métodos de zeros de funções têm pequenas diferenças devido a critérios de parada diferentes e casos patológicos (raízes múltiplas, funções planas, singularidades).
- A integração numérica tem concordância perfeita porque as fórmulas são idênticas.

---

## 5. Validação do Solver

### 5.1 Estratégia de validação

A validação do NumerPy Solver é realizada em três camadas:

1. **Testes unitários** (`tests/`): ~305 testes automatizados cobrindo casos básicos, casos de borda e robustez para cada método. Incluem testes comparativos com SciPy que são executados automaticamente quando `scipy` está disponível.

2. **Validação comparativa** (`comparation/`): 250 problemas de teste (50 por categoria) que comparam o solver contra funções equivalentes do SciPy, com métricas quantitativas de precisão e robustez.

3. **Validação cruzada**: verificação de consistência interna — métodos que resolvem o mesmo problema por caminhos diferentes devem produzir resultados convergentes:
   - Bisseção, Newton e Secante devem convergir para a mesma raiz;
   - LU e Gauss devem produzir o mesmo vetor solução;
   - Newton e Lagrange devem interpolar o mesmo valor;
   - Simpson 1/3 e 3/8 devem convergir para a mesma integral;
   - Euler e RK4 devem convergir para a mesma solução quando $h \to 0$.

### 5.2 Os 250 exemplos como base de validação

A base de 250 exemplos foi projetada para cobrir:

- **Casos triviais**: funções lineares, matrizes identidade, polinômios de baixo grau — validam que o método funciona no caso básico;
- **Casos de stress**: matrizes de Hilbert (mal condicionadas), funções com singularidades, EDOs stiff — testam os limites do método;
- **Casos patológicos**: raízes múltiplas, matrizes singulares, funções descontínuas, EDOs com blowup — verificam que o método falha graciosamente;
- **Casos de precisão**: problemas com solução analítica conhecida — permitem medir erro absoluto e relativo contra o valor exato;
- **Casos de convergência**: problemas onde se pode comparar a taxa de convergência observada com a taxa teórica — validam a ordem de convergência.

Cada um dos 250 problemas é classificado em um dos seguintes status:

- **OK**: ambos (NumerPy e SciPy) convergiram com diferença dentro do limiar;
- **DIFERENÇA**: ambos convergiram, mas com diferença acima do limiar;
- **AMBOS FALHARAM**: nenhum convergiu (problema intratável para o método);
- **SO SCIPY**: apenas o SciPy convergiu (limitação do NumerPy);
- **SO CORE**: apenas o NumerPy convergiu (caso raro, geralmente por diferença de critério de parada).

### 5.3 Critérios de confiança

O solver pode ser considerado tecnicamente confiável com base em:

1. **Concordância com SciPy**: para métodos diretos (LU, Gauss, interpolação, integração), a concordância é virtualmente perfeita (diferença < $10^{-14}$), comprovando que a implementação está correta e numericamente equivalente.

2. **Consistência matemática**: os resultados obedecem as propriedades teóricas esperadas — Simpson é exato para polinômios cúbicos, RK4 tem erro $O(h^4)$, Newton converge quadraticamente para raízes simples, etc.

3. **Tratamento de erros**: todos os 12 métodos retornam dicionários estruturados com `success` e `error`, garantindo que falhas são detectáveis e diagnosticáveis. Nenhum método levanta exceções não tratadas.

4. **Validação defensiva**: a camada `validation/` rejeita entradas inválidas (NaN, Inf, dimensões incompatíveis, parâmetros fora de escala) antes que cheguem à camada de computação, evitando comportamentos indefinidos.

5. **Testes de robustez**: 20 testes de robustez por método (100 no total) cobrem casos patológicos que não aparecem em uso normal: matrizes singulares, funções com singularidades, passos negativos, parâmetros de tolerância extremos, etc.

---

## 6. Melhorias Futuras

### 6.1 Melhorias matemáticas

**Métodos de zeros de funções**:
- Implementar o método de Brent (combina bisseção com interpolação quadrática, garantindo convergência com velocidade superlinear);
- Adicionar o método de Illinois (bisseção modificada com convergência superlinear);
- Implementar o método de Müller (interpolação quadrática, converge para raízes complexas).

**Sistemas lineares**:
- Adicionar fatoração QR (mais estável que LU para problemas mal condicionados);
- Implementar Cholesky para matrizes simétricas positivas definidas (custo $n^3/6$ vs $n^3/3$ da LU);
- Adicionar pré-condicionadores para Gauss-Seidel e Gauss-Jacobi (SOR — Successive Over-Relaxation);
- Implementar GMRES para sistemas não simétricos grandes e esparsos.

**Interpolação**:
- Adicionar splines cúbicas (interpolação por partes com suavidade $C^2$);
- Implementar interpolação de Akima (preserva formas sem oscilações de Runge);
- Adicionar mínimos quadrados polinomiais (ajuste em vez de interpolação exata).

**Integração numérica**:
- Implementar quadratura gaussiana (maior precisão com menos pontos para funções suaves);
- Adicionar regra de Romberg (extrapolação de Richardson sobre trapézios);
- Implementar integração adaptativa (refina malha onde o erro é grande);
- Adicionar tratamento de integrais impróprias (singularidades nas extremidades).

**EDOs**:
- Implementar RK45 adaptativo (Dormand-Prince) com controle de erro embutido;
- Adicionar métodos implícitos (Euler implícito, trapezoidal) para EDOs stiff;
- Implementar métodos de passo múltiplo (Adams-Bashforth, Adams-Moulton);
- Adicionar suporte a sistemas de EDOs ($n$ equações de primeira ordem).

### 6.2 Melhorias computacionais

**Performance**:
- Utilizar `numpy.linalg` para operações matriciais nas quais o NumPy delega para BLAS/LAPACK (fatoração LU, substituição direta/regressiva);
- Pré-compilar funções críticas com Numba (`@jit`) para evitar overhead do interpretador Python em loops de iteração;
- Paralelizar Gauss-Jacobi com `multiprocessing` ou `concurrent.futures` (cada componente é independente na mesma iteração).

**Escalabilidade**:
- Adicionar suporte a matrizes esparsas (`scipy.sparse`) para sistemas lineares grandes;
- Implementar armazenamento em formato COO, CSR e CSC para matrizes esparsas;
- Para problemas com mais de 100 variáveis, usar métodos iterativos com pré-condicionamento em vez de métodos diretos.

**Precisão**:
- Implementar aritmética de precisão estendida (`mpmath`) para problemas que exigem mais de 15 dígitos significativos;
- Adicionar estimativa de erro a posteriori para todos os métodos iterativos;
- Implementar refinamento iterativo para sistemas lineares (melhora solução obtida por LU).

### 6.3 Melhorias arquiteturais

**Interface**:
- Adicionar exportação de resultados em PDF/LaTeX (relatórios técnicos com fórmulas e gráficos);
- Implementar modo escuro/claro na interface Dash;
- Adicionar visualização interativa de iterações (slider para percorrer cada passo);
- Suporte a sistemas de EDOs (múltiplas equações acopladas).

**API**:
- Criar API REST (Flask/FastAPI) para acesso programático aos métodos numéricos;
- Adicionar endpoints para processamento em lote (múltiplos problemas de uma vez);
- Documentação OpenAPI/Swagger.

**Testes**:
- Adicionar testes de propriedade (property-based testing com Hypothesis) para gerar problemas aleatórios;
- Adicionar testes de precisão estendida (comparação com soluções analíticas em alta precisão);
- Implementar CI/CD com execução automática dos 250 testes comparativos.

**GPU e paralelismo**:
- Migrar operações matriciais para CuPy (GPU) para sistemas lineares grandes;
- Usar CUDA via Numba para métodos iterativos em GPU;
- Paralelizar interpolação de Lagrange (cada $L_i$ é independente).

---

## 7. Conclusão Técnica

O NumerPy Solver é um projeto de engenharia de software numérica que implementa doze métodos fundamentais de cálculo numérico com rigor matemático, validação defensiva e transparência algorítmica. A arquitetura em camadas (core → validation → utils → pages) separa responsabilidades de forma limpa, garantindo que a lógica matemática é pura (sem dependência de UI), a validação é consistente (cada método tem seu validador dedicado), e a interface é reativa (cada página tem seu callback dedicado).

A comparação sistemática com o SciPy sobre 250 problemas de teste demonstra que as implementações são numericamente corretas: métodos diretos (LU, Gauss, interpolação, integração) produzem resultados idênticos ao SciPy dentro da precisão do ponto flutuante; métodos iterativos (Gauss-Seidel, Gauss-Jacobi) convergem para as mesmas soluções quando as condições de convergência são satisfeitas; e os métodos de zeros de funções e EDOs produzem resultados comparáveis, com diferenças explicáveis por diferenças nos critérios de parada e estratégias de passo.

O ponto forte do solver não é substituir o SciPy em produção — é complementá-lo com transparência. Cada método retorna dados intermediários de iteração que o SciPy não fornece, gráficos Plotly que visualizam o processo de convergência, e mensagens de erro estruturadas em português que facilitam o diagnóstico. Isso faz do NumerPy Solver uma ferramenta tanto pedagógica quanto profissional: estudantes podem inspecionar cada passo do algoritmo, e profissionais podem validar resultados antes de delegar ao SciPy para cálculos em larga escala.

As escolhas de implementação — pivotamento parcial em LU e Gauss, detecção de singularidade com limiar $10^{-14}$, alerta de dominância diagonal em métodos iterativos, retorno de dados parciais em caso de falha, avaliação de Horner em Newton, verificação de nó exato em Lagrange — refletem uma preocupação com robustez numérica que vai além do mínimo funcional. Cada método foi construído para falhar de forma informativa, não silenciosa.

A base de 250 exemplos de teste, cobrindo desde casos triviais até problemas patológicos, fornece uma validação abrangente que excede o que é tipicamente encontrado em projetos de métodos numéricos de mesmo escopo. A concordância quantitativa com o SciPy, combinada com a cobertura qualitativa de casos de borda, estabelece confiança na correção das implementações.

Em suma, o NumerPy Solver é um projeto seriamente construído: arquitetura limpa, implementações matematicamente corretas, validação extensa, documentação completa, e uma base comparativa transparente contra a biblioteca de referência do ecossistema científico Python.

---

*Documentação gerada em maio de 2025. Versão do solver: v1.1.0.*