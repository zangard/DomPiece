from pydantic import BaseModel, Field
from typing import List


class InputModel(BaseModel):
    """
    Image URLs Input Piece Input Model
    """

    image_urls: List[str] = Field(
        description="List of image URLs to fetch and encode as base64 strings",
    )


class OutputModel(BaseModel):
    """
    Image URLs Input Piece Output Model
    """

    image_base64_strings: List[str] = Field(
        description="List of base64 encoded strings of the fetched images",
    )
