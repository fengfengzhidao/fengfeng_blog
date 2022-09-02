# @Time:2022/9/2 21:17
# @Author:fengfeng
# 登录失败的可复用代码
def clean_form(form):
    err_dict: dict = form.errors
    # 拿到所有错误的字段名字
    err_valid = list(err_dict.keys())[0]
    # 拿到第一个字段的第一个错误信息
    err_msg = err_dict[err_valid][0]
    return err_valid, err_msg
