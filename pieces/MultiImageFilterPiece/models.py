from pydantic import BaseModel, Field
from typing import List


class InputModel(BaseModel):
    image_urls: List[str] = Field(
        description="List of image URLs to fetch, filter, and render to HTML.",
        json_schema_extra={"from_upstream": "always"},
    )
    sepia: bool = Field(default=False, description="Apply sepia effect.")
    black_and_white: bool = Field(default=False, description="Apply black and white effect.")
    brightness: bool = Field(default=False, description="Apply brightness effect.")
    darkness: bool = Field(default=False, description="Apply darkness effect.")
    contrast: bool = Field(default=False, description="Apply contrast effect.")
    red: bool = Field(default=False, description="Apply red effect.")
    green: bool = Field(default=False, description="Apply green effect.")
    blue: bool = Field(default=False, description="Apply blue effect.")
    cool: bool = Field(default=False, description="Apply cool effect.")
    warm: bool = Field(default=False, description="Apply warm effect.")


class OutputModel(BaseModel):
    filtered_image_count: int = Field(
        description="Number of images successfully filtered.",
    )
    html_file_path: str = Field(
        description="Path to the HTML file containing all filtered images.",
    )
