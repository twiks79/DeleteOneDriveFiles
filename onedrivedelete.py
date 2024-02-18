from msal import ConfidentialClientApplication
import requests
import json
import os

# Define the client ID, client secret, and tenant ID
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
TENANT_ID = os.environ.get('TENANT_ID')

# Define the maximum number of items to delete
MAX_ITEMS_TO_DELETE = 4000

def authenticate_and_get_token():
    # Create a Confidential Client Application
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )

    # Acquire a token for the Microsoft Graph API
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    access_token = result.get("access_token")
    return access_token

def delete_items_in_folder(access_token, folder_id, count=0):
    # Define the Microsoft Graph API endpoint for deleting items
    endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
    
    # Define the headers for the request
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Send a request to retrieve items in the folder
    response = requests.get(endpoint, headers=headers)
    response_data = response.json()
    
    # Iterate over items and delete them
    for item in response_data['value']:
        if count >= MAX_ITEMS_TO_DELETE:
            print("Reached maximum items to delete.")
            return count
        # Delete the item
        requests.delete(f"{endpoint}/{item['id']}", headers=headers)
        print(f"Deleted: {item['name']}")
        count += 1
    return count

def main():
    # Authenticate and get the access token
    access_token = authenticate_and_get_token()
    
    # Get root folder or allow user to select a folder
    root_folder_id = 'root'
    target_folder_name = input("Enter the name of the target folder: ")
    if target_folder_name:
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me/drive/root/children",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response_data = response.json()
        for item in response_data['value']:
            if item['name'] == target_folder_name:
                root_folder_id = item['id']
                break
    
    # Delete items in the target folder
    print("Deleting items...")
    deleted_count = delete_items_in_folder(access_token, root_folder_id)
    print(f"Total items deleted: {deleted_count}")

if __name__ == "__main__":
    main()
