from miniopy_async import Minio
from dotenv import load_dotenv
import os
import aiohttp
import asyncio 
load_dotenv()

minio_container=os.environ.get('MINIO_CONTAINER_NAME')

minio_user=os.environ.get('MINIO_ROOT_USER')
minio_password=os.environ.get('MINIO_ROOT_PASSWORD')

bucket_name =os.environ.get('MINIO_BUCKET_NAME')

port_in = os.environ.get('MINIO_PORT_PROGRAMM_ADDRESS')
port_out = os.environ.get('MINIO_PORT_PROGRAMM_ADDRESS_DESKTOP')

is_docker = os.environ.get('POST_IN_DOCKER')

#client.fput_object(bucket_name, destination_file, source_file)
if is_docker == 'True':
    client = Minio(
        f'{minio_container}:{port_in}',
        access_key=minio_user,
        secret_key=minio_password,
        secure=False
    )
else:    
    client = Minio(
        f'localhost:{port_out}',
        access_key=minio_user,
        secret_key=minio_password,
        secure=False
    )

async def check_backet_exists():
    if not await client.bucket_exists(bucket_name):
        print("create bucket")
        await client.make_bucket(bucket_name)
    else:
        print("bucket exists")


async def get_file(filename):
    try:
        async with aiohttp.ClientSession() as session:
            responce = await client.get_object(bucket_name, f"{filename}", session)
            byte = await responce.read()
    finally:
        responce.close()
    return byte

async def check_file_size(filename) -> bool:
    try:
        size = await client.stat_object(bucket_name, f"{filename}")
        return size.size < 1024 * 1024 * 50
    except Exception as e:
        print(f"Ошибка при получении размера файла {e}")
        return False

async def add_file(filename, id_channel, blob):
    if not await client.bucket_exists(bucket_name):
        print("create bucket")
        client.make_bucket(bucket_name)
    try:
        await client.put_object(bucket_name, f"{id_channel}/{filename}", blob, blob.getbuffer().nbytes)
    except Exception as passing:
        print(f"не возможно загрузить контент в минио {passing}")
    #return byte
#print(add_file("test.jpg", "2054430930", "record/2054430930/4/photo_2024-05-10_19-27-22.jpg"))
