# @Time:2022/7/13 18:52
# @Author:fengfeng
import time
import math
import functools
from django.core.cache import cache
from django.http import JsonResponse

TIME_OUT = 10  # 限制时间，最大10秒一次


# 缓存类
class CacheModel:

    def __init__(self, model="cache", *args):
        self.request = args[1]
        self.model = model

    def get(self, key, value=None) -> dict:
        # 根据model的不同使用不同的方法
        if self.model == 'session':
            return self.request.session.get(key, value)
        return cache.get(key, value)

    def set(self, key, value):
        if self.model == 'session':
            self.request.session[key] = value
            return
        cache.set(key, value)


# 钩子函数独有异常类
class HookException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


# 默认的钩子函数 返回原函数的参数
def default_hook_function(*args, **kwargs):
    # 如果是方法，request就是args第二个参数
    # request = args[1]
    # raise HookException('全局钩子')
    pass


# 主要是针对api的频率限制，以及钩子函数
def frequency_limit_decorator(
        key=None,
        cache_id='nid',
        msg='点赞过于频繁，请{}秒后重试！',
        mode='cache',  # 默认使用缓存配置
        timeout=TIME_OUT,
        hook=default_hook_function):
    """
    key：
    cache_id：
    msg：显示的消息，{}中显示的是 timeout的差值
    mode：cache or session
    timeout：时间差
    hook：钩子函数
    """
    def frequency_decorator(fun):

        @functools.wraps(fun)
        def cache_control(*args, **kwargs):
            # 根据key从缓存中获取数据
            class_obj = args[0]
            # 缓存的key
            cache_key = key or class_obj.__class__.__name__
            # 缓存的数据
            cache_ctl = CacheModel(mode, *args)
            _data = cache_ctl.get(cache_key, {})
            # 具体的每一项id，通过关键字传给视图
            get_id_the = kwargs.get(cache_id)
            # 之前的时间，现在的时间
            old_time = _data.get(get_id_the, 0)
            now_time = time.time()
            # 时间差，单位秒
            time_difference = math.ceil(now_time - old_time)
            if time_difference < timeout:
                data = {
                    'msg': msg.format(timeout - time_difference),
                    'code': 567,
                }
                return JsonResponse(data)
            res = fun(*args, **kwargs)
            # 获取当前时间戳
            _data[get_id_the] = time.time()

            cache_ctl.set(cache_key, _data)

            # 函数执行完毕就执行钩子函数
            try:
                # 在钩子函数里面可以执行封号策略
                hook(*args, **kwargs)
            except HookException as e:
                return JsonResponse({'code': 767, "msg": e.msg})
            return res

        return cache_control

    return frequency_decorator
