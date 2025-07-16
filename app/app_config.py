# This code snippet is importing the `fastapi_users` object from the `config` module within the `auth`
# package of the `users` module in the `app` package. It then calls the `current_user()` function from
# the `fastapi_users` object to retrieve the current user information.
# we are using this code part in handlers
from app.users.auth import fastapi_users

current_user = fastapi_users.current_user()
