from botocore.response import StreamingBody

from cicloguia.src.adapters import repository


def test_upload_image(test_image_name, images_folder, images_repo: repository.S3Repository):
    file_path = images_folder + test_image_name
    with open(file_path, 'rb') as data:
        response = images_repo.add(data=data, file_name=test_image_name)
        assert response is None


def test_load_image(test_image_name, images_repo: repository.S3Repository):
    response = images_repo.get(file_name=test_image_name)
    assert isinstance(response, StreamingBody)
