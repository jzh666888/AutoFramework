def json_output_check(expect, actual):
    """
    json返回体的通用断言方法
    :param expect: 接收断言的预期值，需要满足dict or list
    :param actual: 接口的json返回体转换成json()进行接收
    :return:
    """
    for k, v in expect.items():
        assert k in actual.keys(), f'key【{k}】 not in actual.keys, actual keys = {list(actual.keys())}'
        if isinstance(v, type):
            assert type(
                actual[k]) == v, f'key【{k}】 type != expect type【{v}】, actual value【{actual[k]}】 is 【{type(actual[k])}】'
        elif isinstance(v, list):
            assert len(actual[k]) == len(v), f'【{k}】array element len != expect len, actual element【{actual[k]}】, excpect element【{v}】'
            for element_index in range(len(v)):
                if isinstance(v[element_index], type):
                    assert type(actual[k][element_index]) == v[element_index], f'【{k}】array element type != expect type 【{v[element_index]}】' \
                                                        f', actual value 【{actual[k][element_index]}】 is ' \
                                                        f'【{type(actual[k][element_index])}】'
                elif isinstance(v[element_index], dict):
                    json_output_check(v[element_index], actual[k][element_index])
                else:
                    assert actual[k][element_index] == v[element_index], f'【{k}】array element != expect value 【{v[element_index]}】, actual value 【{actual[k][element_index]}】'

        else:
            assert actual[k] == v, f'key【{k}】 value != expect value【{v}】, actual value【{actual[k]}】'
    assert len(expect.keys()) == len(
        actual.keys()), f'actual.keys length out of expect.keys, actual keys = {list(actual.keys())}'

if __name__ == '__main__':
    expect_res = {
        'name':'jzh',
        'age':27,
        'getTime':1768654509,
        'createTime': 123
    }
    actual_res = {
        'name':'jzh',
        'age':27,
        'getTime': 1768654509,
        'createTime': '123'
    }
    json_output_check(expect_res,actual_res)