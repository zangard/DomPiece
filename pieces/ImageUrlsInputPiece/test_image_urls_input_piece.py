from domino.testing import piece_dry_run


def test_image_urls_input_piece():
    input_data = dict(
        image_urls=[
            "https://upload.wikimedia.org/wikipedia/commons/3/3f/JPEG_example_flower.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png",
        ]
    )
    output_data = piece_dry_run(
        "ImageUrlsInputPiece",
        input_data,
    )

    assert len(output_data["image_base64_strings"]) == 2
    assert all(isinstance(s, str) and len(s) > 0 for s in output_data["image_base64_strings"])
