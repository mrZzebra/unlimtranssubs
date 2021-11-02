import json
from source.fullСalculation import full_calculation 
from traceback import format_exc

def predictMethod(input_json):
    try:
        input_json = json.loads(input_json)
        mid = input_json['id']
        starting_vintage = int(input_json['starting_vintage'])
        periods = int(input_json['periods'])
        result = full_calculation(starting_vintage,periods, mid)
        return json.dumps(result)

    except:
        return json.dumps({'error': format_exc()})
