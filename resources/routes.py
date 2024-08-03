from resources.auth import Register, Login, Test, UpdateUserRole, InsertAdminUser, Logout

routes = (
    (Register, "/register"),
    (Login, "/login"),
    (Logout, "/logout"),
    (Test, "/some"),
    (UpdateUserRole, "/users/<string:user_id>/role"),
    (InsertAdminUser, "/insert_admin"),
)
