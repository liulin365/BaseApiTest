import sys
from function.print_log import log


def assert_response(response, content):

    try:
        for key, expected_value in content.items():
            actual_value = response.get(key)
            if actual_value != expected_value:
                log.error(f'断言失败！预期 {key}={expected_value}，实际 {key}={actual_value}\n')
                sys.exit(1)

        log.info('测试用例通过~~~\n')

    except Exception as e:
        log.error(f'断言异常：{e}\n')
        sys.exit(1)