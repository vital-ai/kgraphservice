import requests
import json
from io import BytesIO

# Set the base URL for the FastAPI app
BASE_URL = "http://localhost:6008"

# File to upload and download
# PDF_PATH = "/Users/hadfield/Desktop/2410.12288v1.pdf"
# FILE_KEY_NAME = "2410.12288v1.pdf"

PDF_PATH = "/Users/hadfield/Desktop/largefile.webm"
FILE_KEY_NAME = "largefile.webm"


def test_upload_file_async():
    url = f"{BASE_URL}/kgraphservice-upload-async"
    with open(PDF_PATH, 'rb') as file:
        metadata = json.dumps({
            "key_name": FILE_KEY_NAME
        })
        files = {
            "metadata": (None, metadata),
            # "file": (FILE_KEY_NAME, file, "application/pdf")
            "file": (FILE_KEY_NAME, file, "video/webm")

        }
        response = requests.post(url, files=files)
    print("Async Upload Response:", response.json())


def test_download_file_async():
    url = f"{BASE_URL}/kgraphservice-download-async/"
    metadata = json.dumps({
        "key_name": FILE_KEY_NAME
    })

    # Use a streaming POST request to handle large files
    with requests.post(url, data={"metadata": metadata}, stream=True) as response:
        if response.status_code == 200:
            with open("../test_output/downloaded_async.pdf", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):  # 8 KB chunks
                    if chunk:  # Only write non-empty chunks
                        f.write(chunk)
            print("Async Download Response: File downloaded as 'downloaded_async.pdf'")
        else:
            print("Async Download Error:", response.json())


def test_upload_file_sync():
    url = f"{BASE_URL}/kgraphservice-upload-sync/"
    with open(PDF_PATH, 'rb') as file:
        metadata = json.dumps({
            "key_name": FILE_KEY_NAME
        })
        files = {
            "metadata": (None, metadata),
            # "file": (FILE_KEY_NAME, file, "application/pdf")
            "file": (FILE_KEY_NAME, file, "video/webm")
        }
        response = requests.post(url, files=files)

    print("Sync Upload Response:", response.json())


def test_download_file_sync():
    url = f"{BASE_URL}/kgraphservice-download-sync/"
    json_body = {"key_name": FILE_KEY_NAME}
    response = requests.post(url, json=json_body)
    if response.status_code == 200:
        with open("../test_output/downloaded_sync.pdf", "wb") as f:
            f.write(response.content)
        print("Sync Download Response: File downloaded as 'downloaded_sync.pdf'")
    else:
        print("Sync Download Error:", response.json())


def test_list_files():
    url = f"{BASE_URL}/kgraphservice-list-files/"
    json_body = {"prefix": ""}
    response = requests.post(url, json=json_body)
    print("List Files Response:", response.json())


def test_get_file_metadata():
    url = f"{BASE_URL}/kgraphservice-file-metadata/"
    json_body = {"key_name": FILE_KEY_NAME}
    response = requests.post(url, json=json_body)
    print("File Metadata Response:", response.json())


def test_delete_file():
    url = f"{BASE_URL}/kgraphservice-delete-file/{FILE_KEY_NAME}"
    response = requests.delete(url)
    print("Delete File Response:", response.json())


def main():
    print("\nTesting Async File Upload")
    test_upload_file_async()

    print("\nTesting Async File Download")
    test_download_file_async()

    # print("\nTesting Sync File Upload")
    # test_upload_file_sync()

    # print("\nTesting Sync File Download")
    # test_download_file_sync()

    print("\nTesting List Files")
    test_list_files()

    print("\nTesting Get File Metadata")
    test_get_file_metadata()

    print("\nTesting Delete File")
    test_delete_file()


if __name__ == "__main__":
    main()
