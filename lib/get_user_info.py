from qqwry import QQwry

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
}


# 获取ip
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        return ip
    ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


# 获取地址
def get_addr_info(ip):
    if ip.startswith('10.') or ip.startswith('192') or ip.startswith('127'):
        return str(('国家内网', ''))
    q = QQwry()
    q.load_file('lib/qqwry.dat')
    return str(q.lookup(ip))


if __name__ == '__main__':
    # lis = eval(get_addr_info('106.13.185.190'))
    print(get_addr_info('116.9.72.179'))

    # get_addr_info('36.99.136.139')
    # get_addr_info('120.228.2.238')
    # get_addr_info('127.0.0.1')
