from xml.dom.minidom import parse
import xml.dom.minidom
import re
import splunklib.results as results

# Dictionary to store all search information

searchDict = {}


# Function to recursively iterate through dictionary to prepend base search strings

# if there is no base search, return own query else return query of base+own query

def prepend_base_search(searchId):
    if (searchDict[searchId][1] == ""):
        return searchDict[searchId][2]

    return prepend_base_search(searchDict[searchId][1]) + searchDict[searchId][2]


# Extraxt all search details in dashboard and create dictionary with searchId, Base searchId,

# full search query, variable list. Currently dashboard name is file in local directory which needs to

# substituted with xml from Splunk API call.
# dict_keys(['bsearchPolicies', 'bsearchTagSets', 'bsearchTestResults', 'searchPrmDatasource', 'searchPrmPFamily', 'searchPrmPolicy', 'searchTagSet', 'searchTag', 'searchDataSourcesCnt', 'searchPoliciesCnt', 'searchAssetsCnt', 'searchPassedPct', 'searchPassedCnt', 'sear
# chFailedCnt', 'searchWaivedCnt', 'searchUnknownCnt', 'searchFailedChart', 'searchAssetTable'])

def get_search_definitions(dashboardName):
    # DOMTree = xml.dom.minidom.parse(dashboardName)
    DOMTree = xml.dom.minidom.parseString(dashboardName)

    collection = DOMTree.documentElement

    searchList = collection.getElementsByTagName("search")

    # Creating initial search dictionary

    for search in searchList:
        search_id = search.getAttribute("id")
        if not search_id == "":
            search_base_id = search.getAttribute("base")

            search_query = search.getElementsByTagName("query")[0].childNodes[0].data

            searchDict[search_id] = [search_id, search_base_id, search_query, []]


    # Prepend base search query and find variables list

    for searchItem in searchDict.values():
        searchItem[2] = prepend_base_search(searchItem[0])

        searchItem[1] = ""

        searchItem[3] = re.findall(r'\$\w+\$', searchItem[2])

        searchDict[searchItem[0]] = searchItem
    # print(searchDict['bsearchTagSets'])

    return searchDict


def search_id_query_prm_mapping_from_string(xml_str):
    search_defination = get_search_definitions(xml_str)
    search_id_query_prm_mapping = {}

    for a in search_defination.values():
        search_id_query_prm_mapping[a[0]] = {"search_query": a[2], "param_list": a[3]}
    return search_id_query_prm_mapping


def get_reconciled_asset_ids(splunk_connection,search_id_query_prm_mapping,tag_set,tag_value):
    search_query_reconciled_id = search_id_query_prm_mapping['bsearchTagSets']['search_query']

    search_query_reconciled_id = "|".join([search_query_reconciled_id,' search tag_set = "{tag_set}" tag_value = "{tag_value}"'.
                                        format(tag_set=tag_set,tag_value=tag_value),' fields reconciled_asset_id'])

    service = splunk_connection
    kwargs_export = {"latest_time": "now",
                     "search_mode": "normal"}

    exportsearch_results = service.jobs.export(search_query_reconciled_id, **kwargs_export)

    reader = results.ResultsReader(exportsearch_results)
    list_reconsiled_id = []
    for result in reader:
        if isinstance(result, dict):
            list_reconsiled_id.append(dict(result)['reconciled_asset_id'])

    return list_reconsiled_id


def get_search_query(search_id_query_prm_mapping, key_query, dict_dynamic_parms):
    """:return: search query based on parameter

    """
    search_query = search_id_query_prm_mapping[key_query]['search_query']

    for param in dict_dynamic_parms.keys():
        search_query = search_query.replace(param, dict_dynamic_parms[param])
    return search_query
