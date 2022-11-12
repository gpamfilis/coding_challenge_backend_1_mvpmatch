def no_content():
    return {"error": False, "msg": "no content"}, 204


def not_found(msg="resource not found"):
    return {"error": False, "msg": msg}, 404
