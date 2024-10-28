import asyncio
import os
from io import BytesIO
import yaml
from vital_ai_vitalsigns.vitalsigns import VitalSigns
from kgraphservice.binary.s3_impl import S3Impl


def load_config(vitalhome):

    config_path = os.path.join(vitalhome, "vital-config", "kgraphservice", "kgraphservice_config.yaml")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        return config


async def test_s3impl(s3_impl, bucket_name, pdf_path, key_name):

    # Load PDF into memory as a byte array
    with open(pdf_path, 'rb') as file:
        original_pdf_data = file.read()

    # Test S3Impl functionality
    print("Testing upload_file_sync...")
    s3_impl.upload_file_sync(original_pdf_data, bucket_name, key_name)

    print("Testing get_file_sync...")
    downloaded_data_sync = s3_impl.get_file_sync(bucket_name, key_name)

    # Compare downloaded data (sync) with original data
    if downloaded_data_sync == original_pdf_data:
        print("Sync download test PASSED: Downloaded data matches the original file.")
    else:
        print("Sync download test FAILED: Downloaded data does not match the original file.")

    print("Testing get_file_async...")
    output_stream = BytesIO()
    await s3_impl.get_file_async(bucket_name, key_name, output_stream)
    output_stream.seek(0)
    downloaded_data_async = output_stream.read()

    # Compare downloaded data (async) with original data
    if downloaded_data_async == original_pdf_data:
        print("Async download test PASSED: Downloaded data matches the original file.")
    else:
        print("Async download test FAILED: Downloaded data does not match the original file.")

    print("Testing list_files...")
    file_list = s3_impl.list_files(bucket_name, prefix='test_pdf/')
    print("Files in bucket (test_pdf/):", file_list)

    print("Testing get_file_metadata...")
    metadata = s3_impl.get_file_metadata(bucket_name, key_name)
    print("Metadata for file:", metadata)

    print("Testing delete_file...")
    s3_impl.delete_file(bucket_name, key_name)
    print("File deleted.")


def main():

    print('Test KGraphService Binary')

    vs = VitalSigns()

    print("VitalSigns Initialized")

    config = vs.get_config()

    print(config)

    vitalhome = vs.get_vitalhome()

    print(vitalhome)

    kgraphservice_config = load_config(vitalhome)

    aws_access_key_id = kgraphservice_config["kgraphservice_binary"].get("aws_access_key_id", "")
    aws_secret_access_key = kgraphservice_config["kgraphservice_binary"].get("aws_secret_access_key", "")
    region_name = kgraphservice_config["kgraphservice_binary"].get("region_name", "")
    bucket_name = kgraphservice_config["kgraphservice_binary"].get("bucket_name", "")

    # Print variables to confirm values
    print("AWS Access Key ID:", aws_access_key_id)
    print("AWS Secret Access Key:", aws_secret_access_key)
    print("Region Name:", region_name)
    print("Bucket Name:", bucket_name)

    s3_impl = S3Impl(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    pdf_path = '/Users/hadfield/Desktop/2410.12288v1.pdf'

    key_name = '2410.12288v1.pdf'

    asyncio.run(test_s3impl(s3_impl, bucket_name, pdf_path, key_name))


if __name__ == "__main__":
    main()
