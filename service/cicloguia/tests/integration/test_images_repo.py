# noinspection PyPackageRequirements
from botocore.response import StreamingBody

from cicloguia.src.adapters import repository


def test_upload_image(image_names, images_folder, images_repo: repository.S3Repository):
    file_path = images_folder + image_names[0]
    with open(file_path, 'rb') as data:
        response = images_repo.add(data=data, file_name=image_names[0])
        assert response is None


def test_load_image(image_names, images_repo: repository.S3Repository):
    response = images_repo.get(file_name=image_names[0])
    assert isinstance(response, StreamingBody)
