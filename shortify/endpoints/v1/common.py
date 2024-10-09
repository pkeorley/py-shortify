from fastapi import Depends
from typing_extensions import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

CredentialsHeader = Annotated[HTTPAuthorizationCredentials, Depends(security)]
