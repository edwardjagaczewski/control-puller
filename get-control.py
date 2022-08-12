import requests
import pandas as pd
from auth import *

client_id = ""
client_secret = ""
#Found in User Settings e.g "us20.app"
app_url = "us20.app"

query = ("""
    query ManageControlsTable(
    $filterBy: ControlFilters
    $issueAnalyticsSelection: ControlIssueAnalyticsSelection
  ) {
    controls(filterBy: $filterBy, first: 500) {
      nodes {
        id
        name
        description
        type
        severity
        createdBy {
          id
          name
          email
        }
        issueAnalytics(selection: $issueAnalyticsSelection) {
          issueCount
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      totalCount
    }
  }
""")

# The variables sent along with the above query
variables = {
  "first": 500,
  "filterBy": {
    "withIssues": None
  }
}


def query_wiz_api(query, variables):
    """Query WIZ API for the given query data schema"""
    data = {"variables": variables, "query": query}

    try:
        # Uncomment the nexvt first line and comment the line after that
        # to run behind proxies
        # result = requests.post(url="https://api.us20.app.wiz.io/graphql",
        #                        json=data, headers=HEADERS, proxies=proxyDict)
        result = requests.post(url="https://api." + app_url + ".wiz.io/graphql",
                               json=data, headers=HEADERS)
    except Exception as e:
        if ('502: Bad Gateway' not in str(e) and
                '503: Service Unavailable' not in str(e) and
                '504: Gateway Timeout' not in str(e)):
            print("<p>Wiz-API-Error: %s</p>" % str(e))
            return(e)
        else:
            print("Retry")
    
    return result.json()

print("Getting Token...")
request_wiz_api_token(client_id, client_secret)
print("Fetching Controls...")
result = query_wiz_api(query, variables)
print(result)

pageInfo = result['data']['controls']['pageInfo']
controls = []
#Pagination of results and building dataframe
#while (pageInfo['hasNextPage']):
    # fetch next page
#    variables['after'] = pageInfo['endCursor']
#    result = query_wiz_api(query, variables)
#    i = 0
    #Appending ccrs
i=0
for x in result['data']['controls']['nodes']:
        rule = result['data']['controls']['nodes'][i]['name']
        controls.append(rule)
        i = i + 1
pageInfo = result['data']['controls']['pageInfo']

df = pd.DataFrame(controls, columns=['Control Name'])
df.index = df.index + 1

print("Writing CSV...")
df.to_csv('controls.csv')
print("Complete!")