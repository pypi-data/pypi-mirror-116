import time
from filecmp import cmp

from metadata_driver_aws.data_plugin import Plugin


def test_complete(aws_plugin, test_file_path):
    # Create folder, upload file, list files, download file, delete file

    # Create bucket
    bucket_name = f"metadata-driver-aws-data-plugin-{int(time.time())}"
    print(f"Test bucket: {bucket_name}")
    aws_plugin.create_directory(f"s3://{bucket_name}/test")

    # List buckets
    buckets = aws_plugin.list_buckets()
    print("Buckets")
    for i, b in enumerate(buckets):
        print("\t", i, b)

    # Upload a file
    aws_plugin.upload(test_file_path, f"s3://{bucket_name}/test/TEST.md")
    files = aws_plugin.list(f"s3://{bucket_name}/test/")
    assert len(files) == 1
    assert files[0] == "test/TEST.md"

    # Get presigned_url
    sign_url = aws_plugin.generate_url(f"s3://{bucket_name}/test/TEST.md")
    assert sign_url.startswith(f"http://localhost:9000/{bucket_name}/test/TEST.md")

    # Download a file
    aws_plugin.download(
        f"s3://{bucket_name}/test/TEST.md", "/tmp/test_driver_aws_data_plugin"
    )
    assert cmp(test_file_path, "/tmp/test_driver_aws_data_plugin")

    # Delete the file
    aws_plugin.delete(f"s3://{bucket_name}/test/TEST.md")
    files = aws_plugin.list(f"s3://{bucket_name}/test/")
    assert len(files) == 0

    # Delete the bucket
    aws_plugin.delete_bucket(bucket_name)
