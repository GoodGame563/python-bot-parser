from miniopy_async import Minio
from dotenv import load_dotenv
import os
import aiohttp
load_dotenv()


port = os.environ.get('MINIO_PORT_PROGRAMM_ADDRESS_DESKTOP')
minio_user=os.environ.get('MINIO_ROOT_USER')
minio_password=os.environ.get('MINIO_ROOT_PASSWORD')
bucket_name =os.environ.get('MINIO_BUCKET_NAME')


#client.fput_object(bucket_name, destination_file, source_file)
client = Minio(
    f'localhost:{port}',
    access_key=minio_user,
    secret_key=minio_password,
    secure=False
)

'''
async def if not await client.bucket_exists(bucket_name):
    print("create bucket")
    client.make_bucket(bucket_name)
    '''

async def get_file(filename):
    try:
        async with aiohttp.ClientSession() as session:
            responce = await client.get_object(bucket_name, f"{filename}", session)
            byte = await responce.read()
    finally:
        responce.close()
    return byte

async def add_file(filename, id_channel, blob):
    try:
        await client.put_object(bucket_name, f"{id_channel}/{filename}", blob, blob.getbuffer().nbytes)
    except Exception as passing:
        print(f"не возможно загрузить контент в минио {passing}")
    #return byte
#print(add_file("test.jpg", "2054430930", "record/2054430930/4/photo_2024-05-10_19-27-22.jpg"))