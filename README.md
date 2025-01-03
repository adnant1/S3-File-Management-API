# S3 File Management API

This is a RESTful API built using Flask, Python, and AWS S3 that allows users to manage their files stored in an AWS S3 bucket. It allows users to upload, retrieve, delete files, and list all files with metadata, such as size and file type.

## Features

- **Upload a file** to an S3 bucket.
- **Retrieve all files** stored in the S3 bucket with pre-signed URLs.
- **Delete a file** from the S3 bucket using its key.
- **Metadata display** for files including size and type.

## Technologies Used

- **Python**: Backend programming language
- **Flask**: Web framework for Python
- **AWS S3**: Cloud storage service for file service
- **Boto3**: AWS SDK for Python, used to interact with S3

## Endpoints

| Method  | Endpoint             | Description                                     |
|---------|----------------------|-------------------------------------------------|
| `POST`  | `/upload`            | Upload a file to the S3 bucket.                 |
| `GET`   | `/files`             | Get a list of all the files in the S3 bucket.   |
| `DELETE`| `/files/<filekey>`   | Delete a specific file by `filekey`.            |
