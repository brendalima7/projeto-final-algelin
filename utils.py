import numpy as np
import cv2

# load frames
def load_video(path, scale=0.25, max_frames=300):
    cap = cv2.VideoCapture(path)
    frames = []
    while len(frames) < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.resize(frame, None, fx=scale, fy=scale)
        frames.append(small.astype(float))
    cap.release()
    return np.array(frames)

# build frame matrix
def build_matrix(frames):
    n_frames = frames.shape[0]
    shape = frames.shape[1:]
    M = frames.reshape(n_frames, -1).T
    return M, shape

# truncated svd
def separate_background(M, k=1):
    U, s, Vt = np.linalg.svd(M, full_matrices=False)
    background = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
    residual = M - background
    return background, residual, s

# convert a column back to an image
def column_to_image(column, shape):
    return column.reshape(shape)


def to_uint8(img):
    return np.clip(img, 0, 255).astype(np.uint8)


def save_video(frames, path, fps=20):
    height, width = frames[0].shape[:2]
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps,
                          (width, height), isColor=True)
    for f in frames:
        out.write(to_uint8(f))
    out.release()