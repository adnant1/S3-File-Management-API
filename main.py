from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import ClientError
import uuid
import os

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
    if not file or file.filename == '':
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

        #temporarily save the file in the working directory
        temp_path = os.path.join(os.getcwd(), file.filename)

        #Upload the file
        try:
            file.save(temp_path) #temporarily save the file into the working directory
            bucket.upload_file(file.filename, unique_key)
            os.remove(temp_path) #delete the temporary file
            return jsonify({'message': 'File uploaded successfully.'}), 201
        except ClientError as e:
            #collect the type of code and message
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            return jsonify({'error code': error_code, 'message': error_message})


#Retrieve file names from S3
@app.route('/files', methods=['GET'])
def list_files():

    #get files  
    files = bucket.objects.all()

    #create a dict to store file keys and urls
    file_dict = {}

    #check if there's any items in the iterable
    files_list = list(files)
    if not files_list:
        return jsonify({'message': 'No files found.'}), 404

    #Store each file key and pre signed url inside the dict
    for file in files:
        key = file.key
        #creates a url to access the file for a limited amount of time
        url = s3.meta.client.generate_presigned_url('get_object', Params = {'Bucket': BUCKET_NAME, 'Key': key}, ExpiresIn=60)

        #add key and url to the dict
        file_dict[key] = url
 
    
    return jsonify(file_dict)


#Delete a file from S3
@app.route('/files/<filekey>', methods=['DELETE'])  
def delete_file(filekey):

    #check to see if file exists
    try:
        data = s3.meta.client.head_object(Bucket=BUCKET_NAME, Key=filekey)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return jsonify({'error': 'File not found.'}), 404
        else:
            return jsonify({'error': str(e)}), 500

    #delete the file
    try:
        bucket.Object(filekey).delete()
        return jsonify({'message': 'File deleted successfully.'}), 200
    except ClientError as e:
        #collect the type of code and message
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        return jsonify({'error code': error_code, 'message': error_message}), 500 #Internal server error


if __name__ == '__main__':
    app.run(debug=True)