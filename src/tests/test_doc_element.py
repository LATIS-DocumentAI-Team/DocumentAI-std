from src.base.content_type import ContentType
from src.tests.mock_sample import (
    mock_doc_element,
    mock_doc_element_classification,
    mock_document,
    mock_paddle,
    mock_easy,
    mock_tesseract,
    mock_document_entity_classification,
)
from src.utility.OCR_adapter import OCRAdapter


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


class TestDocument:
    def test_doc_element(self, mock_document_entity_classification):
        mock_doc_element = mock_document_entity_classification.elements[1][0]

        assert mock_doc_element.x == 10
        assert mock_doc_element.y == 20
        assert mock_doc_element.w == 30
        assert mock_doc_element.h == 40
        assert mock_doc_element.content_type == ContentType.TEXT
        assert mock_doc_element.content == "Text 1"
        assert mock_doc_element.label == 1

    def test_doc_element_classfication(self, mock_document):
        mock_doc_element = mock_document.elements[1][0]

        assert mock_doc_element.x == 10
        assert mock_doc_element.y == 20
        assert mock_doc_element.w == 30
        assert mock_doc_element.h == 40
        assert mock_doc_element.content_type == ContentType.TEXT
        assert mock_doc_element.content == "Text 1"

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

    def test_paddle_adapter(self, mock_paddle):
        output_json = OCRAdapter.from_paddle_ocr(mock_paddle)

        assert len(output_json["bbox"]) == len(output_json["content"])

    def test_easy_adapter(self, mock_easy):
        output_json = OCRAdapter.from_easy_ocr(mock_easy)
        assert len(output_json["bbox"]) == len(output_json["content"])

    def test_tesseract_adapter(self, mock_tesseract):
        output_json = OCRAdapter.from_tesseract_ocr(mock_tesseract)
        assert len(output_json["bbox"]) == len(output_json["content"])
