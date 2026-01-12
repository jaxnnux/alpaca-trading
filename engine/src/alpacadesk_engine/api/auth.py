"""Authentication API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import keyring

from alpaca.trading.client import TradingClient
from alpaca.common.exceptions import APIError

router = APIRouter()

# In-memory session store (would use proper session management in production)
_current_session = {
    "api_key_id": None,
    "secret_key": None,
    "is_paper": False,
    "client": None,
}


class LoginRequest(BaseModel):
    api_key_id: str
    secret_key: str
    is_paper: bool


class LoginResponse(BaseModel):
    success: bool
    message: str = ""


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate with Alpaca API and store credentials securely
    """
    try:
        # Validate credentials by creating a test client
        client = TradingClient(
            api_key=request.api_key_id,
            secret_key=request.secret_key,
            paper=request.is_paper,
        )

        # Test the connection
        account = client.get_account()

        # Store credentials securely using Windows Credential Manager
        keyring.set_password("alpacadesk", "api_key_id", request.api_key_id)
        keyring.set_password("alpacadesk", "secret_key", request.secret_key)
        keyring.set_password("alpacadesk", "is_paper", str(request.is_paper))

        # Store in session
        _current_session["api_key_id"] = request.api_key_id
        _current_session["secret_key"] = request.secret_key
        _current_session["is_paper"] = request.is_paper
        _current_session["client"] = client

        return LoginResponse(
            success=True,
            message=f"Successfully authenticated. Account: {account.account_number}"
        )

    except APIError as e:
        raise HTTPException(status_code=401, detail=f"Alpaca API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


@router.post("/logout")
async def logout():
    """
    Clear stored credentials
    """
    try:
        # Clear credentials from keyring
        try:
            keyring.delete_password("alpacadesk", "api_key_id")
            keyring.delete_password("alpacadesk", "secret_key")
            keyring.delete_password("alpacadesk", "is_paper")
        except keyring.errors.PasswordDeleteError:
            pass  # Credentials already cleared

        # Clear session
        _current_session["api_key_id"] = None
        _current_session["secret_key"] = None
        _current_session["is_paper"] = False
        _current_session["client"] = None

        return {"success": True, "message": "Logged out successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")


@router.get("/validate")
async def validate():
    """
    Validate current credentials
    """
    try:
        if _current_session["client"] is None:
            # Try to restore from keyring
            api_key_id = keyring.get_password("alpacadesk", "api_key_id")
            secret_key = keyring.get_password("alpacadesk", "secret_key")
            is_paper_str = keyring.get_password("alpacadesk", "is_paper")

            if api_key_id and secret_key and is_paper_str:
                is_paper = is_paper_str.lower() == "true"
                client = TradingClient(
                    api_key=api_key_id,
                    secret_key=secret_key,
                    paper=is_paper,
                )
                client.get_account()  # Test connection
                _current_session["client"] = client
                _current_session["api_key_id"] = api_key_id
                _current_session["secret_key"] = secret_key
                _current_session["is_paper"] = is_paper
                return {"valid": True}
            else:
                return {"valid": False}
        else:
            # Test existing client
            _current_session["client"].get_account()
            return {"valid": True}

    except Exception:
        return {"valid": False}


def get_current_client() -> TradingClient:
    """
    Get the current authenticated Alpaca client
    """
    if _current_session["client"] is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return _current_session["client"]
