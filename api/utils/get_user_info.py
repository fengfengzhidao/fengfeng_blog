import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
}


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        return ip
    ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def get_addr_info(ip):
    if ip.startswith('10.') or ip.startswith('192') or ip.startswith('127'):
        return {'prov': '中国', 'city': '内网'}
    url = f'https://www.ip138.com/iplookup.asp?ip={ip}&action=2'
    res = requests.get(url=url, headers=headers).content.decode('gbk')
    result = re.findall(r'ip_result = (.*?);', res, re.S)[0]
    consequence = eval(result)
    addr: dict = consequence['ip_c_list'][0]
    addr.pop('begin')
    addr.pop('end')
    addr.pop('idc')
    addr.pop('net')
    area = addr.get('area')
    if not area:
        addr.pop('area')
    return addr


if __name__ == '__main__':
    get_addr_info('106.13.185.190')
    get_addr_info('36.99.136.139')
    get_addr_info('120.228.2.238')
    get_addr_info('127.0.0.1')
