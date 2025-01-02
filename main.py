from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import ClientError
import uuid

app = Flask(__name__)

#Setup

#Creating the s3 resource
s3 = boto3.resource('s3')

#Global variable for bucket name
BUCKET_NAME = 'python-file-management-bucket'

#S3 bucket
bucket = s3.Bucket(BUCKET_NAME)

#Allowed extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'mp3', 'mp4', 'csv', 'zip'}

#Max file size, 25MB in bytes
MAX_FILE_SIZE = 25 * 1024 * 1024

#Check whether a file extensions is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Routes

#Validate and upload a file to S3
@app.route('/upload', methods=['POST'])
def upload_file():
    
    #get the file from the user
    #returns a FileStorage object
    file = request.files.get('file')
    
    #Check if file exists
    if file is none or file.filename == '':
        #400 is 'bad request'
        return jsonify({'error': 'No file uploaded.'}), 400
    
    if allowed_file(file.filename):

        #check if the file is within limits
        if file.content_length > MAX_FILE_SIZE:
            return jsonify({'error': 'Max file size exceeded.'}), 400
        
        #secure the file name
        filename = secure_filename(file.filename)

        #create a unique identifier key for the file
        unique_key = str(uuid.uuid4()) + '_' + filename

        #Upload the file
        try:
            bucket.upload_file(filename, unique_key)
            return jsonify({'message': 'File uploaded successfully.'}), 201
        except ClientError as e:
            #collect the type of code and message
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            return jsonify({'error code': error_code, 'message': error_message})



#Retrieve file names and URLs from S3
@app.route('/files', methods=['GET'])
def list_files():
    #Fill in
    pass 

#Delete a file from S3
@app.route('/files/<filename>', methods=['DELETE'])  
def delete_file(filename):
    #Fill in
    pass 



if __name__ == '__main__':
    app.run(debug=True)