from django.http import JsonResponse


# 封装响应状态码
def ok_msg(msg: str):
    return ok({}, msg)


# 成功的
def ok(data: any, msg: str):
    return res_full(0, data, msg)


# 失败的
def fail(msg: str):
    return res_full(8, {}, msg)


# 完整的写法
def res_full(code: int, data: any, msg: str):
    return JsonResponse({"code": code, "data": data, "msg": msg})
