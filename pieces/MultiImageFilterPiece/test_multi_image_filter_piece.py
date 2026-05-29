from domino.testing import piece_dry_run


def test_multi_image_filter_piece():
    input_data = dict(
        image_urls=["https://picsum.photos/seed/domino/200/200"],
        sepia=True,
    )
    output_data = piece_dry_run("MultiImageFilterPiece", input_data)

    assert output_data["filtered_image_count"] == 1
    assert output_data["html_file_path"].endswith("filtered_images.html")


def test_empty_image_list():
    input_data = dict(image_urls=[], brightness=True)
    output_data = piece_dry_run("MultiImageFilterPiece", input_data)

    assert output_data["filtered_image_count"] == 0
    assert output_data["html_file_path"].endswith("filtered_images.html")
