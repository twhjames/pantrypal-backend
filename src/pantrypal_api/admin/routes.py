from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse

from src.core.account.services.user_account_service import UserAccountService
from src.pantrypal_api.account.controllers.user_account_controller import (
    UserAccountController,
)
from src.pantrypal_api.account.routers.user_account_routers import (
    get_account_controller,
)
from src.pantrypal_api.account.schemas.user_account_schemas import LoginUserIn
from src.pantrypal_api.modules import injector

router = APIRouter(tags=["Admin"], include_in_schema=False)

LOGIN_FORM = """
<!DOCTYPE html>
<html>
  <head>
    <title>PantryPal Admin Login</title>
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <link href=\"https://unpkg.com/@tabler/core@latest/dist/css/tabler.min.css\" rel=\"stylesheet\" />
  </head>
  <body class=\"d-flex flex-column\">
    <div class=\"page page-center\">
      <div class=\"container-tight py-4\">
        <div class=\"text-center mb-4\">
          <h1>PantryPal Admin</h1>
        </div>
        <form class=\"card card-md\" method=\"post\" action=\"/admin/login\">
          <div class=\"card-body\">
            <div class=\"mb-3\">
              <label class=\"form-label\">Email</label>
              <input type=\"email\" name=\"email\" class=\"form-control\" required />
            </div>
            <div class=\"mb-2\">
              <label class=\"form-label\">Password</label>
              <input type=\"password\" name=\"password\" class=\"form-control\" required />
            </div>
          </div>
          <div class=\"card-footer text-end\">
            <button type=\"submit\" class=\"btn btn-primary\">Login</button>
          </div>
        </form>
      </div>
    </div>
  </body>
</html>
"""


@router.get("/admin/login", response_class=HTMLResponse)
async def login_page() -> HTMLResponse:
    return HTMLResponse(content=LOGIN_FORM)


@router.post("/admin/login")
async def admin_login(
    email: str = Form(...),
    password: str = Form(...),
    controller: UserAccountController = Depends(get_account_controller),
):
    """Handle admin sign-in and issue an auth cookie."""
    from pydantic import ValidationError

    try:
        login_data = LoginUserIn(email=email, password=password)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
        )

    try:
        token = await controller.login(login_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    user_service = injector.get(UserAccountService)
    user = await user_service.get_user(token.user_id)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Administrator access required",
        )

    # Redirect back to the admin dashboard after successful login
    response = RedirectResponse(url="/admin/", status_code=302)
    response.set_cookie("Authorization", f"Bearer {token.token}", httponly=True)
    return response


@router.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("Authorization")
    return response
