import google.ads.google_ads.client
import googleads.errors as errors
import pandas as pd
from datetime import datetime

try:
    current_data = pd.read_csv("data/test.csv")
    csv_exists = True
except Exception:
    csv_exists = False

path_to_creds = "path_to_your_creds"
client = google.ads.google_ads.client.GoogleAdsClient.load_from_storage(path=path_to_creds)
status_enum = client.get_type('UserListAccessStatusEnum').UserListAccessStatus.Name
google_ads_service = client.get_service('GoogleAdsService', version='v1')
date = datetime.now().date()

query = "SELECT user_list.size_for_search, user_list.size_for_display, user_list.name, user_list.id, user_list.account_user_list_status FROM user_list"
account_id = "select_account"
results = google_ads_service.search(str(account_id).replace("-", ""), query=query, page_size=500)
rows = []
for row in results:
    audience_id = row.user_list.id.value
    audience_name = row.user_list.name.value
    status = status_enum(row.user_list.account_user_list_status)
    search_size = row.user_list.size_for_search.value
    display_size = row.user_list.size_for_display.value
    rows.append([date, audience_id, audience_name, status, search_size, display_size])
columns = ["Date","ID", "Name", "Status", "Size - Search", "Size - Display"]
df = pd.DataFrame(data = rows, columns = columns)
print(df)

if csv_exists:
    pd.concat([current_data, df]).to_csv("data/test.csv", index=False)
else:
    df.to_csv("data/test.csv",index=False)




