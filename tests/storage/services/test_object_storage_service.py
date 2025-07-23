from src.core.storage.services.object_storage_service import ObjectStorageService


def test_create_receipt_upload_url_generates_key_and_presigned(
    mock_object_storage_provider, mock_secret_key_provider, mock_logging_provider
):
    mock_secret_key_provider.get_secret.return_value = "bucket-name"
    mock_object_storage_provider.generate_presigned_post.return_value = {
        "url": "http://example.com",
        "fields": {},
    }

    service = ObjectStorageService(
        mock_object_storage_provider,
        mock_secret_key_provider,
        mock_logging_provider,
    )
    result = service.create_receipt_upload_url(user_id=1)

    assert "key" in result
    assert result["upload"] == {"url": "http://example.com", "fields": {}}
    mock_object_storage_provider.generate_presigned_post.assert_called_once()


def test_generic_create_upload_url(
    mock_object_storage_provider, mock_secret_key_provider, mock_logging_provider
):
    service = ObjectStorageService(
        mock_object_storage_provider,
        mock_secret_key_provider,
        mock_logging_provider,
    )
    mock_object_storage_provider.generate_presigned_post.return_value = {
        "url": "http://example.com",
        "fields": {},
    }

    result = service.create_upload_url(
        bucket="bucket-name",
        key_prefix="1",
        extension=".png",
        expires_in=100,
    )

    assert result["key"].startswith("1/")
    assert result["key"].endswith(".png")
    mock_object_storage_provider.generate_presigned_post.assert_called_once_with(
        bucket="bucket-name", key=result["key"], expires_in=100
    )
