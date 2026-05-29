from domino.base_piece import BasePiece
from .models import InputModel, OutputModel


class ImageUrlsInputPiece(BasePiece):

    def piece_function(self, input_data: InputModel):
        self.logger.info(f"Received {len(input_data.image_urls)} image URL(s).")

        return OutputModel(
            image_urls=input_data.image_urls,
        )
