from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from io import BytesIO
from PIL import Image
import numpy as np
import requests
import base64


FILTER_MASKS = {
    "sepia": ((0.393, 0.769, 0.189), (0.349, 0.686, 0.168), (0.272, 0.534, 0.131)),
    "black_and_white": ((0.333, 0.333, 0.333), (0.333, 0.333, 0.333), (0.333, 0.333, 0.333)),
    "brightness": ((1.4, 0, 0), (0, 1.4, 0), (0, 0, 1.4)),
    "darkness": ((0.6, 0, 0), (0, 0.6, 0), (0, 0, 0.6)),
    "contrast": ((1.2, 0.6, 0.6), (0.6, 1.2, 0.6), (0.6, 0.6, 1.2)),
    "red": ((1.6, 0, 0), (0, 1, 0), (0, 0, 1)),
    "green": ((1, 0, 0), (0, 1.6, 0), (0, 0, 1)),
    "blue": ((1, 0, 0), (0, 1, 0), (0, 0, 1.6)),
    "cool": ((0.9, 0, 0), (0, 1.1, 0), (0, 0, 1.3)),
    "warm": ((1.2, 0, 0), (0, 0.9, 0), (0, 0, 0.8)),
}


def _apply_filters(image: Image.Image, filters: list) -> Image.Image:
    np_image = np.array(image, dtype=float)
    for filter_name in filters:
        mask = np.array(FILTER_MASKS[filter_name], dtype=float)
        for y in range(np_image.shape[0]):
            for x in range(np_image.shape[1]):
                np_image[y, x, :3] = np.dot(mask, np_image[y, x, :3])
        np_image = np.clip(np_image, 0, 255)
    return Image.fromarray(np_image.astype(np.uint8))


def _to_base64_png(image: Image.Image) -> str:
    buf = BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


class MultiImageFilterPiece(BasePiece):

    def piece_function(self, input_data: InputModel):
        active_filters = [name for name in FILTER_MASKS if getattr(input_data, name, False)]
        self.logger.info(
            f"Applying filters {active_filters} to {len(input_data.image_urls)} image(s)."
        )

        filtered_b64_images = []
        for i, url in enumerate(input_data.image_urls):
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content)).convert("RGB")
            filtered = _apply_filters(image, active_filters)
            filtered_b64_images.append(_to_base64_png(filtered))
            self.logger.info(f"Processed image {i + 1}/{len(input_data.image_urls)}")

        img_tags = "\n".join(
            f'    <div class="image-card">'
            f'<p>Image {i + 1}</p>'
            f'<img src="data:image/png;base64,{b64}" alt="Image {i + 1}"/>'
            f'</div>'
            for i, b64 in enumerate(filtered_b64_images)
        )
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Filtered Images</title>
  <style>
    body {{ font-family: sans-serif; background: #f5f5f5; padding: 20px; }}
    h1 {{ color: #333; }}
    .filters {{ margin-bottom: 16px; color: #666; }}
    .gallery {{ display: flex; flex-wrap: wrap; gap: 16px; }}
    .image-card {{ background: #fff; border-radius: 8px; padding: 12px; box-shadow: 0 2px 6px rgba(0,0,0,.1); }}
    .image-card p {{ margin: 0 0 8px; font-weight: bold; color: #444; }}
    .image-card img {{ max-width: 400px; display: block; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Filtered Images</h1>
  <p class="filters">Filters applied: {", ".join(active_filters) if active_filters else "none"}</p>
  <div class="gallery">
{img_tags}
  </div>
</body>
</html>"""

        html_file_path = f"{self.results_path}/filtered_images.html"
        with open(html_file_path, "w") as f:
            f.write(html)

        self.display_result = {
            "file_type": "html",
            "file_path": html_file_path,
        }

        return OutputModel(
            filtered_image_count=len(filtered_b64_images),
            html_file_path=html_file_path,
        )
