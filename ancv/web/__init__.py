def is_terminal_client(user_agent: str) -> bool:
    terminal_clients = [
        "curl",
        "wget",
        "powershell",
    ]

    for client in terminal_clients:
        if client.lower() in user_agent.lower():
            return True
    return False
