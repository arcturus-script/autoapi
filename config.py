configs = [
    {
        "client_id": "",
        "secret": "",
        "redirect_uri": "https://alist.nn.ci/tool/onedrive/callback",
        "redis_host": "localhost",
        "redis_port": 6379,
        "redis_key": "drive",  # stay unique
        "refresh_token": "",  # can keep empty, or initial value
        "redis_password": "",
    }
]

api_list = [
    r"https://graph.microsoft.com/v1.0/me/drive/root",
    r"https://graph.microsoft.com/v1.0/me/drive",
    r"https://graph.microsoft.com/v1.0/drive/root",
    r"https://graph.microsoft.com/v1.0/users",
    r"https://graph.microsoft.com/v1.0/me/messages",
    r"https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules",
    r"https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta",
    r"https://graph.microsoft.com/v1.0/me/drive/root/children",
    r"https://graph.microsoft.com/v1.0/me/drive/recent",
    r"https://graph.microsoft.com/v1.0/me/mailFolders",
    r"https://graph.microsoft.com/v1.0/me/outlook/masterCategories",
]
