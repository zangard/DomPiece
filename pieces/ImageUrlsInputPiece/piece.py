from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import base64
import requests


class ImageUrlsInputPiece(BasePiece):

    def piece_function(self, input_data: InputModel):
        self.logger.info(f"Fetching {len(input_data.image_urls)} image URL(s).")

        image_base64_strings = []
        for url in input_data.image_urls:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            encoded = base64.b64encode(response.content).decode("utf-8")
            image_base64_strings.append(encoded)

        return OutputModel(
            image_base64_strings=image_base64_strings,
        )
