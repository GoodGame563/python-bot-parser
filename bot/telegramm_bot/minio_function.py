import time
from minio import Minio


minio_user="minioadmin"
minio_password="minioadmin"
bucket_name ='files'
from minio.sse import SseCustomerKey


#client.fput_object(bucket_name, destination_file, source_file)
client = Minio(
    'localhost:9000',
    access_key=minio_user,
    secret_key=minio_password,
    secure=False
)


if not client.bucket_exists(bucket_name):
    print("create bucket")
    client.make_bucket(bucket_name)

def get_file(filename):
    try:
        responce = client.get_object(bucket_name, f"{filename}")
        byte = responce.read()
    finally:
        responce.close()
        responce.release_conn() 
    print("Success")
    return byte

    #return byte
#print(add_file("test.jpg", "2054430930", "record/2054430930/4/photo_2024-05-10_19-27-22.jpg"))