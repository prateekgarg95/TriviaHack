from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyDhuVifox4FOCFmUjjuPJaVUz_TVBO9uNM"
my_cse_id = "012114595421034588555:uu11iyb7zda"


def google_search(search_term,**kwargs):
    service = build("customsearch", "v1", developerKey=my_api_key)
    res = service.cse().list(q=search_term, cx=my_cse_id, **kwargs).execute()
    # pprint.pprint(res)
    return res['items']



