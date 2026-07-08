from function.print_log import log


def assert_response(response,content):
    try:
        if content in response:
            log.info('测试用例通过！\n')
    except Exception as e:
        log.error('用例未获得通过！\n')
