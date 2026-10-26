import cv2
import numpy as np

def patch_clone(input_path, output_path, patch_w_pct=0.12, patch_h_pct=0.12):
    img = cv2.imdecode(np.fromfile(input_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    h, w = img.shape[:2]
    print(f"Loaded {input_path}: {w}x{h}")

    pw = int(w * patch_w_pct)
    ph = int(h * patch_h_pct)

    # Source patch: top-right corner (same x position, different y)
    source = img[0:ph, w - pw:w].copy()

    # Destination: bottom-right corner (where the watermark is)
    dest_region = img[h - ph:h, w - pw:w].copy()

    # Blend source over destination with a gradient mask so edges are soft
    blend_mask = np.zeros((ph, pw), dtype=np.float32)
    for i in range(ph):
        for j in range(pw):
            # Fade in from edges — stronger blend toward the corner
            alpha_y = i / ph          # 0 at top of patch, 1 at bottom
            alpha_x = j / pw          # 0 at left of patch, 1 at right
            blend_mask[i, j] = alpha_y * alpha_x
    blend_mask = blend_mask[:, :, np.newaxis]

    blended = (source * blend_mask + dest_region * (1 - blend_mask)).astype(np.uint8)
    img[h - ph:h, w - pw:w] = blended

    success = cv2.imwrite(output_path, img, [cv2.IMWRITE_WEBP_QUALITY, 82])
    print(f"Saved {output_path}: {'OK' if success else 'FAILED'}")

base = r"C:\Users\seanm\Desktop\_M\seanmcgrathmusic_website\assets\images"

patch_clone(f"{base}\\songwriter-desk.jpg", f"{base}\\songwriter-desk.webp")
patch_clone(f"{base}\\paper-texture.jpg",   f"{base}\\paper-texture.webp")
