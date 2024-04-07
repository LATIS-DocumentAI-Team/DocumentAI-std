from DocumentAI_std.base.doc_enum import ContentRelativePosition, VerticalAlignment
from DocumentAI_std.tests.mock_sample import *
from DocumentAI_std.utils.OCR_adapter import OCRAdapter
from DocumentAI_std.utils.layout_utils import LayoutUtils
from DocumentAI_std.utils.text_utils import TextUtils
from utils.image_utils import ImageUtils


class TestDocElements:
    def test_doc_element(self, mock_doc_element):
        assert mock_doc_element.x == 1
        assert mock_doc_element.y == 2
        assert mock_doc_element.w == 3
        assert mock_doc_element.h == 4
        assert mock_doc_element.content_type == ContentType.TEXT
        assert mock_doc_element.content == "Mock Content"

    def test_doc_element_classification_properties(
        self, mock_doc_element_classification
    ):
        assert mock_doc_element_classification.x == 1
        assert mock_doc_element_classification.y == 2
        assert mock_doc_element_classification.w == 3
        assert mock_doc_element_classification.h == 4
        assert mock_doc_element_classification.content_type == ContentType.TEXT
        assert mock_doc_element_classification.content == "Mock Content"
        assert mock_doc_element_classification.label == 5

    def test_to_json(self, mock_doc_element_classification):
        json_data = mock_doc_element_classification.to_json()
        assert json_data["bbox"] == [1, 2, 3, 4]
        assert json_data["content_type"] == ContentType.TEXT
        assert json_data["content"] == "Mock Content"
        assert json_data["label"] == 5

    def test_serialize(self, mock_doc_element):
        serialize_object = mock_doc_element.serialize()
        assert serialize_object["x"] == 1
        assert serialize_object["y"] == 2
        assert serialize_object["w"] == 3
        assert serialize_object["h"] == 4
        assert serialize_object["content_type"] == ContentType.TEXT
        assert serialize_object["content"] == "Mock Content"


class TestDocument:
    def test_doc_element_classfication(self, mock_document_entity_classification):
        doc_element_class = mock_document_entity_classification.elements[0]

        assert mock_document_entity_classification.filename == "test.jpg"
        assert doc_element_class.x == 10
        assert doc_element_class.y == 20
        assert doc_element_class.w == 30
        assert doc_element_class.h == 40
        assert doc_element_class.content_type == ContentType.TEXT
        assert doc_element_class.content == "Text 1"
        assert doc_element_class.label == 1

    def test_doc_element(self, mock_document):
        doc_element = mock_document.elements[0]

        assert mock_document.filename == "test.jpg"
        assert doc_element.x == 10
        assert doc_element.y == 20
        assert doc_element.w == 30
        assert doc_element.h == 40
        assert doc_element.content_type == ContentType.TEXT
        assert doc_element.content == "Text 1"

    def test_to_json(self, mock_document):
        json_data = mock_document.to_json()

        assert len(json_data["bbox_list"]) == 3
        assert len(json_data["bbox_list"]) == len(json_data["content_type_list"])
        assert len(json_data["bbox_list"]) == len(json_data["content_list"])
        assert json_data["bbox_list"][0] == [10, 20, 30, 40]
        assert json_data["bbox_list"][1] == [50, 60, 70, 80]
        assert json_data["bbox_list"][2] == [90, 100, 110, 120]

        assert json_data["content_type_list"][0] == ContentType.TEXT
        assert json_data["content_type_list"][1] == ContentType.TEXT
        assert json_data["content_type_list"][2] == ContentType.TEXT

        assert json_data["content_list"][0] == "Text 1"
        assert json_data["content_list"][1] == "Text 2"
        assert json_data["content_list"][2] == "Text 3"

    def test_seralize(self, mock_document):
        serialize_object = mock_document.serialize()

        assert serialize_object["filename"] == "test.jpg"
        assert serialize_object["elements"] == [
            e.serialize() for e in mock_document.elements
        ]

    def test_paddle_adapter(self, mock_paddle):
        output_json = OCRAdapter.from_paddle_ocr(mock_paddle)

        assert len(output_json["bbox"]) == len(output_json["content"])

    def test_easy_adapter(self, mock_easy):
        output_json = OCRAdapter.from_easy_ocr(mock_easy)
        assert len(output_json["bbox"]) == len(output_json["content"])

    def test_tesseract_adapter(self, mock_tesseract):
        output_json = OCRAdapter.from_tesseract_ocr(mock_tesseract)
        assert len(output_json["bbox"]) == len(output_json["content"])


class TestUtils:
    def test_nbr_chars(self, mock_doc_element):
        assert TextUtils.nbr_chars(mock_doc_element) == 12

    def test_is_date(self, mock_dates):
        for date in mock_dates:
            assert (
                TextUtils.is_date(
                    DocElement(None, None, None, None, ContentType.TEXT, date)
                )
                == True
            )

    def test_relative_position(self, mock_document):
        """Test the relative_position method."""
        # Test the top height position
        position = LayoutUtils.relative_position(
            mock_document.elements[0], mock_document
        )
        assert position == ContentRelativePosition.TOP_HEIGHT

        # Test the central height position
        position = LayoutUtils.relative_position(
            mock_document.elements[1], mock_document
        )
        assert position == ContentRelativePosition.CENTRAL_HEIGHT

        # Test the bottom height position
        position = LayoutUtils.relative_position(
            mock_document.elements[2], mock_document
        )
        assert position == ContentRelativePosition.BOTTOM_HEIGHT

    @pytest.mark.parametrize("s1, s2, expected_distance", mock_levenshtien())
    def test_levenshtein_distance(self, s1, s2, expected_distance):
        # Create DocElement instances
        doc_element1 = DocElement(0, 0, 0, 0, ContentType.TEXT, s1)
        doc_element2 = DocElement(0, 0, 0, 0, ContentType.TEXT, s2)

        # Compute Levenshtein distance
        distance = TextUtils.levenshtein_distance(doc_element1, doc_element2)

        # Check if the computed distance matches the expected distance
        assert distance == expected_distance, f"Distance for {s1} and {s2} is incorrect"

    @pytest.mark.parametrize(
        "a_x, a_y, b_x, b_y, expected_euclidean, expected_manhattan, expected_chebyshev",
        mock_distances(),
    )
    def test_distances(
        self,
        a_x,
        a_y,
        b_x,
        b_y,
        expected_euclidean,
        expected_manhattan,
        expected_chebyshev,
    ):
        # Create DocElement instances
        doc_element1 = DocElement(a_x, a_y, 0, 0, ContentType.TEXT, "")
        doc_element2 = DocElement(b_x, b_y, 0, 0, ContentType.TEXT, "")

        # Compute distances
        euclidean_dist = LayoutUtils.euclidean_distance(doc_element1, doc_element2)
        manhattan_dist = LayoutUtils.manhattan_distance(doc_element1, doc_element2)
        chebyshev_dist = LayoutUtils.chebyshev_distance(doc_element1, doc_element2)

        # Check if the computed distances match the expected distances
        assert euclidean_dist == expected_euclidean, f"Euclidean distance is incorrect"
        assert manhattan_dist == expected_manhattan, f"Manhattan distance is incorrect"
        assert chebyshev_dist == expected_chebyshev, f"Chebyshev distance is incorrect"

    @pytest.mark.parametrize("a, b, expected_overlap", mock_overlap())
    def test_overlap_calculation(self, a, b, expected_overlap):
        # Compute overlap
        overlap = LayoutUtils.calculate_overlap(a, b)

        # Check if the computed overlap matches the expected overlap
        assert overlap == expected_overlap

    @pytest.mark.parametrize("a, b, expected_alignment", mock_horizontal_alignment())
    def test_horizontal_alignment(self, a, b, expected_alignment):
        # Compute horizontal alignment
        alignment = LayoutUtils.calculate_horizontal_alignment(a, b)

        # Check if the computed alignment matches the expected alignment
        assert alignment == expected_alignment

    @pytest.mark.parametrize("a, b, expected_alignment", mock_vertical_alignment())
    def test_vertical_alignment(self, a, b, expected_alignment):
        # Compute vertical alignment
        alignment = LayoutUtils.calculate_vertical_alignment(a, b)

        # Check if the computed alignment matches the expected alignment
        assert alignment == expected_alignment

    @pytest.mark.parametrize("a, expected_entropy", mock_entropy())
    def test_entropy(self, a, expected_entropy):
        # Calculate entropy using the ImageUtils class
        entropy = ImageUtils.entropy(a)

        # Check if the calculated entropy matches the expected value
        assert pytest.approx(entropy, abs=1e-6) == expected_entropy

    @pytest.mark.parametrize("ocr_method, lang_list, source", mock_ocr())
    def test_ocr(self, ocr_method, lang_list, source):
        ocr = OCRAdapter(ocr_method, lang_list)
        # ocr.apply_ocr()
        print(ocr.apply_ocr(source).to_json())
        # Compute overlap
        # overlap = LayoutUtils.calculate_overlap(a, b)

        # Check if the computed overlap matches the expected overlap
        # assert overlap == expected_overlap
