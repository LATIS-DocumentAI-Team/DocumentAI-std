from src.base.content_type import ContentType
from src.tests.mock_sample import mock_doc_element, mock_doc_element_classification


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


class TestDocumentt:
    def test_doc_element(self, mock_document):
        assert mock_doc_element.x == 1
        assert mock_doc_element.y == 2
        assert mock_doc_element.w == 3
        assert mock_doc_element.h == 4
        assert mock_doc_element.content_type == ContentType.TEXT
        assert mock_doc_element.content == "Mock Content"

    def test_to_json(self, mock_document):
        img_path = "/path/to/your/image.jpg"
        document = Document(img_path, ocr_output)
        json_data = document.to_json()

        assert len(json_data['bbox_list']) == 1
        assert json_data['bbox_list'][0] == [1, 2, 3, 4]
        assert len(json_data['content_type_list']) == 1
        assert json_data['content_type_list'][0] == ContentType.TEXT
        assert len(json_data['content_list']) == 1
        assert json_data['content_list'][0] == "Mock Content"
