# DeleteOneDriveFiles
Mass delete one drive files

# How to get CLIENT_ID, CLIENT_SECRET and TENANT ID
az login

az ad app create --display-name "OneDriveDelete"
-> get the appid

az ad app credential reset --id <appid>
