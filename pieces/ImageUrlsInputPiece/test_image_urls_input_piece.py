from domino.testing import piece_dry_run


def test_image_urls_input_piece():
    input_data = dict(
        image_urls=[
            "https://picsum.photos/seed/domino/200/200",
            "https://picsum.photos/seed/test/200/200",
        ]
    )
    output_data = piece_dry_run("ImageUrlsInputPiece", input_data)

    assert output_data["image_urls"] == input_data["image_urls"]
