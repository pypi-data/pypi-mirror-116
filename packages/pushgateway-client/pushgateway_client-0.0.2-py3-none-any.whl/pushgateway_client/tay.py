import requests
import socket


################################
# pushgateway相关
################################
def push_data(_url, _metric_name, _metric_value, _job_name, _labels: dict, ):
    dim = ''
    if "instance" in _labels.keys():
        pass
    else:
        _labels['instance'] = socket.gethostname()
    headers = {
        'X-Requested-With': 'Python Requests',
        'Content-type': 'application/json'
    }
    for key, value in _labels.items():
        dim += '/{}/{}'.format(key, value)
    try:
        result = requests.post(
            headers=headers,
            url="http://{}/metrics/job/{}{}".format(_url, _job_name, dim),  # 外网地址
            data="{} {}\n".format(_metric_name, _metric_value),
        )
        print(result.text)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    try:
        push_data(
            # _url="172.20.5.13:9091",
            _url="150.158.237.21:39091",
            _metric_name="yunwei_test",
            _metric_value="123",
            _job_name="yunwei",
            _labels={
                "aaa": "bbb"
            }
        )
    except Exception:
        print("数据推送失败！")
