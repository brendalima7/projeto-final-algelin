# projeto-final-algelin

## Remoção de background de vídeo com SVD

### Ideia

Cada frame do vídeo (redimensionado e achatado) vira uma **coluna** de uma matriz `M`:

```
M = [ f1 | f2 | ... | fn ]      (pixels × frames)
```

Como a câmera é fixa, o background é praticamente igual em todos os frames, então as colunas de `M` são quase linearmente dependentes. Isso faz `M` ser aproximadamente de **posto baixo**:

```
M = U Σ Vᵀ ≈ σ1 · u1 · v1ᵀ
```

- `u1` (primeiro vetor singular à esquerda) é a "imagem" que melhor explica todos os frames, ou seja, o **background**.
- `σ1 · v1ᵀ` dá o peso desse background em cada frame (variações de iluminação).
- O produto `U[:, :k] Σk Vt[:k, :]` é a **projeção** de cada frame no subespaço gerado pelos `k` primeiros vetores singulares, o que corresponde ao background reconstruído.
- O resíduo `M − background` guarda o que se move (**foreground**).

Pelo teorema de Eckart–Young, essa truncagem é a melhor aproximação de posto `k` de `M`. Objetos em movimento ocupam pixels diferentes em cada frame, por isso não cabem num subespaço de dimensão baixa e ficam no resíduo.

A implementação está em [utils.py](utils.py) (`separate_background`) e o fluxo completo em [notebooks/BACKGROUND.ipynb](notebooks/BACKGROUND.ipynb).

### Como executar

1. Instale as dependências com [uv](https://docs.astral.sh/uv/):

   ```bash
   uv sync
   ```

2. Coloque o vídeo de entrada em `videos/original/` (de preferência com a câmera parada).

3. Abra `notebooks/BACKGROUND.ipynb` e troque o caminho do vídeo:

   ```python
   video_path = "../videos/original/meu_video.mp4"
   ```

4. Crie as pastas de saída, se ainda não existirem (o `cv2.VideoWriter` falha sem avisar quando a pasta não existe):

   ```bash
   mkdir -p videos/svd/background images/svd/background
   ```

5. Rode todas as células. As saídas são:
   - `videos/svd/background/background.mp4`: o background reconstruído, frame a frame
   - `images/svd/background/background.png`: uma imagem estática do background (mediana dos frames)

### Parâmetros úteis

- `load_video(path, scale=0.25, max_frames=300)`: diminua `scale` ou `max_frames` se faltar memória, já que a matriz tem `(altura·largura·3) × n_frames` entradas.
- `separate_background(M, k=1)`: `k=1` costuma bastar. Aumente `k` (2–3) se a iluminação variar bastante, mas saiba que um `k` grande demais começa a absorver o foreground.
- `save_video(..., fps=20)`: ajuste ao FPS do vídeo original.
