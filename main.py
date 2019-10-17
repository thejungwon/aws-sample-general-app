from flask import Flask
from flask import render_template, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import json
import mysql.connector
import boto3
from botocore.exceptions import ClientError

UPLOAD_FOLDER = 'media'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

with open('config.json') as json_file:
    data = json.load(json_file)
    app.config['RDS_ENDPOINT'] = data['rds-endpoint'] if "rds-endpoint" in data else ""
    app.config['RDS_USER'] = data['rds-user'] if "rds-user" in data else ""
    app.config['RDS_PASSWORD'] = data['rds-password'] if "rds-password" in data else ""
    app.config['S3_BUCKETNAME'] = data['s3-bucketname'] if "s3-bucketname" in data else ""
    app.config['S3_REGION'] = data['s3-region'] if "s3-region" in data else ""
    print(app.config)



@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        print(request.form)
        data = request.form.to_dict()
        print(data)
        app.config['RDS_ENDPOINT'] = data['rds-endpoint'] if "rds-endpoint" in data else ""
        app.config['RDS_USER'] = data['rds-user'] if "rds-user" in data else ""
        app.config['RDS_PASSWORD'] = data['rds-password'] if "rds-password" in data else ""
        app.config['S3_BUCKETNAME'] = data['s3-bucketname'] if "s3-bucketname" in data else ""
        app.config['S3_REGION'] = data['s3-region'] if "s3-region" in data else ""
        print(app.config)
        try :
            mydb = mysql.connector.connect(
              host=app.config['RDS_ENDPOINT'],
              user=app.config['RDS_USER'],
              passwd=app.config['RDS_PASSWORD']
            )

        except Exception as e:
            print(e)
            #return redirect("/")

        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)

        try:
            if app.config['S3_REGION'] is None:
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=app.config['S3_BUCKETNAME'])
            else:
                s3_client = boto3.client('s3', region_name=app.config['S3_REGION'])
                location = {'LocationConstraint': app.config['S3_REGION']}
                s3_client.create_bucket(Bucket=app.config['S3_BUCKETNAME'],
                                        CreateBucketConfiguration=location)
        except Exception as e:
            print(e)

    return redirect("/")


@app.route('/post', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        print(request.form)
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect("/")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect("/")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/")


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80 ,debug=True)
