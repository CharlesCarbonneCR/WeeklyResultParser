from office365.sharepoint.client_context import ClientContext
import os
from dotenv import load_dotenv

load_dotenv()

test_client_id = os.getenv('test_client_id')
test_client_secret = os.getenv('test_client_secret')

ctx = ClientContext("https://hidroplatanar-my.sharepoint.com/personal/charles_hidroplatanar_com/").with_client_credentials(
    test_client_id, test_client_secret
)
target_web = ctx.web.get().execute_query()
print(target_web.url)

folders = (
    ctx.web.default_document_library().root_folder.get_folders(False).execute_query()
)
for folder in folders:
    print(
        "Url: {0}, Created: {1}".format(folder.serverRelativeUrl, folder.time_created)
    )
    if "FilaDeMogoteDailyReports" in folder.serverRelativeUrl :
        filaDeMogoteDailyReportsRelativeUrl = folder.serverRelativeUrl
print("daily reports relative path :", filaDeMogoteDailyReportsRelativeUrl)

libraryRoot = ctx.web.get_folder_by_server_relative_path(filaDeMogoteDailyReportsRelativeUrl)
ctx.load(libraryRoot)
ctx.execute_query()
files = libraryRoot.files
ctx.load(files)
ctx.execute_query()
for file in files:
    file_url = file.serverRelativeUrl
    fileName = file.name
    print("URL: {0}".format(file_url))
    excelPath = '../excel/'+fileName
    excelPath = os.path.join(os.path.dirname(__file__), excelPath)
    with open(excelPath, "wb") as local_file:
        file = (
            ctx.web.get_file_by_server_relative_url(file_url)
            .download(local_file)
            .execute_query()
        )
    print("[Ok] file has been downloaded into: {0}".format(excelPath))

