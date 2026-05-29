from domino.testing import piece_dry_run


def test_image_urls_input_piece():
    input_data = dict(
        image_urls=[
            "https://example.com/image1.png",
            "https://example.com/image2.jpg",
        ]
    )
    output_data = piece_dry_run(
        "ImageUrlsInputPiece",
        input_data,
    )

    assert output_data["image_urls"] == input_data["image_urls"]
