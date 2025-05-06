from fastapi import Depends, APIRouter, HTTPException, Request, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from schema.user import User, UserResponse, UserTokenResponse, UserLogOut
from DAL.user_table_queries import create_user_query, get_user_query, user_exists
from service.password_service import PasswordChecker
from controller.grpc_client import request_authorization


authentication_router = APIRouter()


@authentication_router.post('/api/v1/signup', summary='Sign up user to the service', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(form_data: User, pass_service: PasswordChecker = Depends()):
    user_already_created = get_user_query(username=form_data.username)
    if user_already_created:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Use already exists')

    if not pass_service.validate_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password')

    form_data.password = pass_service.generate_password_hash(form_data.password)

    created_user = create_user_query(form_data.model_dump())

    if not created_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Error')

    return created_user.__data__


@authentication_router.post('/api/v1/login', summary='Login user to service', status_code=status.HTTP_200_OK)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends() , pass_service: PasswordChecker = Depends()):
    get_user_data = get_user_query(username=form_data.username)

    if not pass_service.check_pass_against_db_pass(form_data.password, get_user_data.password) or not user_exists(form_data.username):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    token_response = await request_authorization('tokens', user_id=str(get_user_data.id))

    response.headers['Authorization'] = f'Bearer {token_response.access}'
    response.set_cookie(
        key='refresh_token',
        value=token_response.refresh,
        httponly=True,
        samesite='lax'
    )

    return {'message': 'Logged in successfully!'}


@authentication_router.post('/api/v1/access', summary='Give refresh token to get new access token', response_model=UserTokenResponse, status_code=status.HTTP_200_OK)
async def get_access(request: Request, response: Response):
    token = request.headers['refresh_token']

    user_id_response = await request_authorization('user_id', token=token)
    if not user_id_response.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    get_user_data = get_user_query(user_id=user_id_response.user_id)
    if not get_user_data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User does not exist')

    access_response = await request_authorization('access', token=token)
    response.headers['Authorization'] = f'Bearer {access_response.access}'

    return {'message': 'Done'}


@authentication_router.post('/api/v1/logout', summary='User logout')
async def logout(user_data: UserLogOut):
    logout_response = await request_authorization('logout', user_id=user_data.user_id)
    if logout_response.message == 'logged_out':
        return JSONResponse(content={'message': 'logged out'}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={'message': 'user is not logged in'}, status_code=status.HTTP_400_BAD_REQUEST)


async def get_current_user(request: Request):
    token = request.headers['Authorization'].split(' ')[1]
    user_id_response = await request_authorization('user_id', token=token)
    get_user_data = get_user_query(user_id=user_id_response.user_id)
    return User(username=get_user_data.username, email=get_user_data.email, full_name=get_user_data.full_name, role=get_user_data.role, password="")


@authentication_router.get('/api/v1/current', summary='get current active user', response_model=User)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user


def role_required(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f'Insufficient privileges. Required {required_role} role'
            )
        return current_user
    return role_checker


@authentication_router.get('/api/v1/admin', summary='Admin user')
async def read_admin_data(current_user: User = Depends(role_required('admin'))):
    content = {'message': 'Welcome Admin'}
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)