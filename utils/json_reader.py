from utils. __init__ import *

def read_json(filepath):
    file_path = os.path.join(os.path.dirname(__file__), '../Test_data/{filepath}'.format(filepath=filepath))
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def get_test_case_details_from_json(filename,testcase_name ,testcase_section):
    policy_details = read_json(filename)
    return policy_details[testcase_name][testcase_section]

