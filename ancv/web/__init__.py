def is_terminal_client(user_agent: str) -> bool:
    user_agent = user_agent.lower()
    return any(
        client in user_agent
        for client in [
            "curl",
            "wget",
            "powershell",
        ]
    )
