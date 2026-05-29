from pydantic import BaseModel, Field
from typing import List


class InputModel(BaseModel):
    """
    Image URLs Input Piece Input Model
    """

    image_urls: List[str] = Field(
        description="List of image URLs to pass to the next node",
    )


class OutputModel(BaseModel):
    """
    Image URLs Input Piece Output Model
    """

    image_urls: List[str] = Field(
        description="List of image URLs passed to the next node",
    )
