import os
import uuid
import boto3

ACCESS_KEY = 'AKIAIXT57SZBA5USI57Q'
SECRET_KEY = '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'
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format('ebutler')
s3_client = boto3.client('s3',
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY)


def build_filename(uploaded, obj=None):
    print(obj)
    if obj != None:
        filename = obj.slug + '-' + \
            uploaded.name.split('.')[0].lower() + '-' + \
            '.' + uploaded.name.split('.')[-1]
    else:
        filename = uuid.uuid4().hex + '-' + uploaded.name
    return filename


def upload(filename, destination_folder, obj=None):
    upload_folder = 'uploads/'
    destination_name = build_filename(filename, obj)
    tmp_location = upload_folder + str(destination_name)

    with open(tmp_location, 'wb+') as destination:
        for chunk in filename.chunks():
            destination.write(chunk)
    try:
        response = s3_client.upload_file(
            tmp_location, 'wddng', destination_folder + str(destination_name))
    except Exception as error:
        print(error)
        return False
    return "https://wddng.s3-eu-west-1.amazonaws.com/{}{}".format(destination_folder, destination_name)
