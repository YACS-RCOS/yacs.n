def success_msg(content: dict):
    result = {"success": True, "errMsg": None, "content": content}
    return result

def error_msg(error_msg: str, content=None):
    result = {"success": False, "errMsg": error_msg, "content": content}
    return result
