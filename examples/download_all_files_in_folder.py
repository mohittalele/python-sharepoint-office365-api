from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import os

def downloadFile(ctx, download_path, file_url):
    with open(download_path, "wb") as local_file:
        file = ctx.web.get_file_by_server_relative_url(file_url).download(local_file).execute_query()
        # file = ctx.web.get_file_by_server_relative_url(file_url).download(local_file).execute_query()
    print("[Ok] file has been downloaded into: {0}".format(download_path))


def printAllContents(ctx, relativeUrl):
    try:
        libraryRoot = ctx.web.get_folder_by_server_relative_url(relativeUrl)
        ctx.load(libraryRoot)
        ctx.execute_query()

        folders = libraryRoot.folders
        ctx.load(folders)
        ctx.execute_query()

        for myfolder in folders:
            # print("Folder name: {0}".format(myfolder.properties["Name"]))
            print("Folder name: {0}".format(myfolder.properties["ServerRelativeUrl"]))
            printAllContents(ctx, relativeUrl + '/' + myfolder.properties["Name"])

        files = libraryRoot.files
        ctx.load(files)
        ctx.execute_query()

        for myfile in files:
            print("File name: {0}".format(myfile.properties["ServerRelativeUrl"]))
            path_list = myfile.properties["ServerRelativeUrl"].split('/')
            file_dest = outputDir + "/" + path_list[-3] + "/" + path_list[-2] + "/" + path_list[-1]
            os.makedirs(os.path.dirname(file_dest), exist_ok=True)
            downloadFile(ctx, file_dest, myfile.properties["ServerRelativeUrl"])

    except Exception as e:
        print(e)
        pass


site_url = "https://[your_domain].sharepoint.com/sites/[site_name]"
username = ""
password = ""
outputDir = "/tmp"
ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))
web = ctx.web
ctx.load(web)
ctx.execute_query()
print("Web title: {0}".format(web.properties['Title']))

# try to find the right relativeurl
# Failed here
urls_try = [
    '/sites/[site_name]/Shared Documents/',
    # '/sites/[site_name]/Documents/',
    # '/Documents',
    # '/sites/team/Shared Documents/'
]
for relative_url in urls_try:
    printAllContents(ctx, relative_url)
