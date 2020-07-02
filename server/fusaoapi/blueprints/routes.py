from fusaoapi.resources import (
    UserRegister,
    UserLogin,
    UserLogout,
    AllUsers,
    Result,
)


def init_routes(api):
    api.add_resource(UserRegister, "/signup")
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(AllUsers, "/users")
    api.add_resource(Result, "/name")
