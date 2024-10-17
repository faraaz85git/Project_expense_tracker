role_to_routes={
    "/expenses":["user","admin"],
    "/expenses/{expense_id}":["user","admin"],
    "/expense/categories":["user","admin"],
    "/budget/active_budget":["user","admin"],
    "/budget/budget_status":["user","admin"],
    "/budget":["user","admin"],
    "/users":["admin"],
    "/users/expenses":["admin"]
}

private_routes=["/users","/users/expenses"]