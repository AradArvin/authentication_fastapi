import grpc
from controller.generated.authorization_pb2 import SendSUB, SendToken
from controller.generated.authorization_pb2_grpc import AuthorizationStub


CHANNEL_OPTIONS = [
    ('grpc.keepalive_time_ms', 10000),
    ('grpc.keepalive_timeout_ms', 5000),
    ('grpc.keepalive_permit_without_calls', 1),
    ('grpc.enable_retries', 0)
]


async def run(response_type, user_id, token):
    async with grpc.aio.insecure_channel(target='localhost:50051', options=CHANNEL_OPTIONS) as channel:
        stub = AuthorizationStub(channel)
        if response_type == 'refresh':
            response = await stub.GetRefresh(SendSUB(user_id=user_id))
        elif response_type == 'access':
            response = await  stub.GetAccess(SendToken(token=token))
        elif response_type == 'user_id':
            response = await stub.GetUserId(SendToken(token=token))
        elif response_type == 'tokens':
            response = await stub.GetTokens(SendSUB(user_id=user_id))
        elif response_type == 'logout':
            response = await stub.LogOut(SendSUB(user_id=user_id))

        return response


async def request_authorization(response_type, user_id=None, token=None):
    response = await run(response_type, user_id, token)
    return response