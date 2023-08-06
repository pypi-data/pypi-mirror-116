
def test_add_number(number):
    return number + 1


def __get_base_url(env):
    return {
        'live': 'https://toolbox.pypestream.com',
        'local': 'http://localhost:8000',
        'sandbox': 'https://toolbox.claybox.usa.pype.engineering'
    }.get(env)


def __set_payload(payload):
    if not payload:
        return ''
    else:
        return payload


def send_log(alert_id, context, payload=None):
    import traceback
    import requests
    base_url = __get_base_url(context['env'])
    req_url = '{}/alerting/log/{}'.format(base_url, alert_id)

    req_body = {
        "traceback_log": traceback.format_exc(),
        "context": context,
        "payload": __set_payload(payload)}

    resp = requests.post(req_url, json=req_body)
    print(resp.text)
    try:
        if resp.status_code == 200:
            return resp.json()['log_id']
    except Exception as err:
        print(err)
    return 'error'
