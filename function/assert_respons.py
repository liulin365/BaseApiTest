from function.print_log import log


def assert_response(response,content):
    try:
        assert response['ok'] == True
        log.info(f'{content}用例通过！')
    except Exception as e:
        log.error(f'{content}用例未获得通过！\n{e}')