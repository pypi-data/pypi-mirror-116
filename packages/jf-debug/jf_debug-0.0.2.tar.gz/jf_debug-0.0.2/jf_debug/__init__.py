# coding=utf-8

import time
import traceback


def get_ms_time():
    """ 获取毫秒时间
    :return: 毫秒时间
    """
    return time.time() * 1000


def log(info, script_name="script_name", info_key="DEBUG"):
    """ 日志输出
    :param info: 日志信息
    :param script_name: 运行脚本名
    :param info_key: 日志信息类型，可选“INFO”、“DEBUG”、“ERROR”
    """
    print("[{}] [{}] log info: {}".format(info_key, script_name, info))


def timer(wrapper_func):
    """ 计时器，修饰方法。实际函数被修饰即会被运行，传入方法初始化inner_wrapper，后将运行方法的参数传入args，到此后即可完整运行被修饰函数。
    :param wrapper_func: 被修饰的方法
    """
    def inner_wrapper(*args):
        """ 内部运行方法，用于接收参数
        :param args: 被修饰方法入参，实质
        :return: 被修饰方法返回值
        """
        start_time = get_ms_time()
        wrapper_func_res = wrapper_func(*args)
        end_time = get_ms_time()
        log("run function: {}, cost time: {} ms".format(wrapper_func.__name__, end_time - start_time))
        return wrapper_func_res

    return inner_wrapper


def error_trace(wrapper_func):
    """ 错误打印，修饰方法。
    :param wrapper_func: 被修饰的方法
    """
    def inner_wrapper(*args):
        """ 内部运行方法，用于接收参数
        :param args: 被修饰方法入参，实质
        :return: 被修饰方法返回值
        """
        try:
            wrapper_func_res = wrapper_func(*args)
            return wrapper_func_res
        except Exception as e:
            wrapper_func_res = None
            error_info = traceback.format_exc(e)
            error_info = error_info[:-1].replace("\n", " || ")
            log(error_info)
        return wrapper_func_res

    return inner_wrapper

