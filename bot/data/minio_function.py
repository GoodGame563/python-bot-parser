from miniopy_async import Minio
from miniopy_async.commonconfig import ENABLED, Filter
from miniopy_async.lifecycleconfig import Expiration, LifecycleConfig, Rule, Transition
# from minio import LifecycleConfig, Rule, Expiration
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

config = LifecycleConfig(
    [
        Rule(
            ENABLED,
            rule_filter=Filter(prefix=""),
            rule_id="rule1",
            expiration=Expiration(days=1)
        )
    ],
)
async def check_backet_exists():
    if not await client.bucket_exists(bucket_name):
        print("create bucket")
        await client.make_bucket(bucket_name)
    else:
        print("bucket exists")
    await client.set_bucket_lifecycle(bucket_name, config)


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
