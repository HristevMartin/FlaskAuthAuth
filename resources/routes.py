from resources.auth import Register, Login, Test, UpdateUserRole, InsertAdminUser

routes = (
    (Register, "/register"),
    (Login, "/login"),
    (Test, "/some"),
    (UpdateUserRole, "/users/<string:user_id>/role"),
    (InsertAdminUser, "/insert_admin"),
)
