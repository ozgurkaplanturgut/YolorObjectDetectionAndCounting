import os
import json, requests, time
from utils.redis_queue_handler import RedisQueue

def download_file(url: str, filename: str):
        
        """
        Downloads file under given directory
        Note: filename takes absolute path and name of file
        """
        try:
            if not os.path.exists('dowloaded_files'):
                os.makedirs('dowloaded_files')
            print(f"Trying to download file from given URL: {url}")
            print(f"File path: {filename}")
            response = requests.get(url)
            with open(os.path.join('dowloaded_files', filename), 'wb') as file:
                file.write(response.content)
            print("File downloaded under: {}".format(os.path.join('dowloaded_files', filename)))
            downloaded_path = os.path.join('dowloaded_files', filename)
            return downloaded_path
        except:
            print(f"File is not downloaded from {url} properly.", exc_info=True)        
        

def downloader():
    
    """
    Downloads file from redis queue
    """
    
    downloadable_queue = RedisQueue("downloadable_queue")
    downloaded_queue = RedisQueue("downloaded_queue")
    
    while True:
        if downloadable_queue.qsize() > 0:
            payload = json.loads(downloadable_queue.get())
            downloaded_path = download_file(payload["source_url"],
                                                    payload["source_url"].split("/")[-1])
            
            
            if os.path.exists(downloaded_path):
                print(f"Image has been downloaded successfully.")

                payload['source_url']= downloaded_path
                
        else:
            print("Downloadable queue is empty. Waiting for new file to download.")
            time.sleep(5)