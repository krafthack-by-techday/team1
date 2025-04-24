import requests

def get_mba_data_elhub():
    """
    Fetches data from the Elhub API for the MBA (Prisområde) data.
    Documentation of the dataset: 
    https://dok.elhub.no/data/forbruk-per-bruksdgn-prisomrade-og-nringshovedomra
    """
    main_path = "https://data.elhub.no/download/"
    dataset_path = "consumption_per_group_mba_hour/"
    file_path = "consumption_per_group_mba_hour-all-no-0000-00-00.csv"
    url = main_path + dataset_path + file_path
    response = requests.get(url)

    if response.status_code == 200:
        with open("data/reference_data/" + file_path, 'wb') as file:
            file.write(response.content)
        print(f"Data downloaded successfully and saved to {file_path}")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")

# can be run as a standalone for now
if __name__ == "__main__":
    get_mba_data_elhub()