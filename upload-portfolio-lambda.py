import boto3
from botocore.client import Config
import io
import zipfile
import mimetypes

s3 = boto3.resources('s3', config=Config(signature_version='s3v4'))

portfolio_bucket = s3.Bucket('portfolio.davidmclark.info')
build_bucket = s3.Bucket('portfoliobuild.davidmclark.info')

portfolio_zip = io.BytesIO()
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')