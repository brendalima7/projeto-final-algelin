# Decomposição em Valores Singulares (SVD)

Projeto de Álgebra Linear que explora a Decomposição em Valores Singulares em duas aplicações:

- compressão de imagens coloridas;
- separação do background de vídeos com câmera fixa.

## Estrutura do projeto

```text
.
├── images/
│   ├── image_compression/       # Imagem usada na compressão
│   └── svd/background/         # Backgrounds estáticos extraídos
├── notebooks/
│   ├── IMAGE_COMPRESSION.ipynb # Compressão de imagem RGB
│   └── BACKGROUND.ipynb        # Extração de background de vídeo
├── videos/
│   ├── original/               # Vídeos de entrada
│   └── background/             # Vídeos de background reconstruídos
├── utils.py                         # Funções compartilhadas
└── pyproject.toml                   # Dependências e configuração do projeto
```

## Compressão de imagem colorida

O notebook [IMAGE_COMPRESSION.ipynb](notebooks/IMAGE_COMPRESSION.ipynb) comprime a imagem `images/image_compression/dog.jpg` sem convertê-la para escala de cinza.

A SVD é calculada separadamente nos canais vermelho, verde e azul:

```text
Aᴄ = Uᴄ Σᴄ Vᴄᵀ,  c ∈ {R, G, B}
```

Cada canal é reconstruído com apenas os `r` maiores valores singulares e, ao final, os três canais são empilhados novamente. O notebook compara aproximações de postos `5`, `20` e `100`, além de exibir:

- a média dos valores singulares dos três canais;
- a soma acumulada normalizada desses valores.

Quanto menor o posto, maior a compressão e menor a quantidade de detalhes preservados.

## Remoção de background de vídeo

O fluxo completo está no notebook [BACKGROUND.ipynb](notebooks/BACKGROUND.ipynb), com as funções auxiliares implementadas em [utils.py](utils.py).

Cada frame do vídeo é redimensionado, achatado e armazenado como uma coluna da matriz `M`:

```text
M = [f₁ | f₂ | ... | fₙ]      (pixels × frames)
```

Quando a câmera permanece fixa, o cenário muda pouco entre os frames. Assim, `M` pode ser aproximada por uma matriz de posto baixo:

```text
M = U Σ Vᵀ ≈ Uₖ Σₖ Vₖᵀ
```

- `Uₖ Σₖ Vₖᵀ` representa o background reconstruído;
- `M − Uₖ Σₖ Vₖᵀ` representa o resíduo, onde se concentra o movimento;
- pelo teorema de Eckart–Young, a SVD truncada fornece a melhor aproximação de posto `k` para `M`.

Atualmente, o repositório contém dois vídeos de entrada (`video_01.mp4` e `video_02.mp4`) e seus respectivos resultados. O notebook seleciona o vídeo por meio da variável:

```python
n_video = 2
```

As saídas são gravadas automaticamente em:

```text
videos/background/background_0{n_video}.mp4
images/svd/background/background_0{n_video}.png
```

## Como executar

### Pré-requisitos

- Python 3.11 ou superior;
- [uv](https://docs.astral.sh/uv/).

### Instalação

Na raiz do projeto, instale as dependências:

```bash
uv sync
```

Inicie o Jupyter Lab sem alterar as dependências do projeto:

```bash
uv run --with jupyter jupyter lab
```

Depois, abra e execute um dos notebooks da pasta `notebooks/`.

### Usando outra imagem

Coloque a imagem em `images/image_compression/` e altere o caminho em `IMAGE_COMPRESSION.ipynb`:

```python
A = imread('../images/image_compression/minha_imagem.jpg')
```

### Usando outro vídeo

1. Coloque o arquivo em `videos/original/`, preferencialmente gravado com a câmera parada.
2. Ajuste `n_video` ou substitua `video_path` em `BACKGROUND.ipynb`.
3. Execute todas as células do notebook.

## Parâmetros principais

- `r`, em `IMAGE_COMPRESSION.ipynb`: quantidade de valores singulares preservados em cada canal RGB.
- `load_video(path, scale=0.25, max_frames=300)`: controla a resolução e o número máximo de frames carregados.
- `separate_background(M, k=1)`: define o posto usado na reconstrução do background. Valores maiores podem capturar variações de iluminação, mas também podem incorporar partes do foreground.
- `save_video(frames, path, fps=20)`: define a taxa de quadros do vídeo gerado.

O custo de memória da remoção de background cresce com `(altura · largura · 3) × número de frames`. Em caso de falta de memória, reduza `scale` ou `max_frames`.
