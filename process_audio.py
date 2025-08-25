from google.cloud import storage
import os
import subprocess

# Procesa archivos .mp3 o .wav

# Initialize the GCS client
client = storage.Client()
bucket_name = os.getenv('BUCKET_NAME', 'default-bucket-name')
stems_number = os.getenv('STEMS_NUMBER', '5')
print(f"Stems amount: {stems_number}")
input_dir = 'input/'
output_dir = 'output-allinone/'

print("PENDING: write processing logs to /logs/")

def list_files(bucket_name, prefix):
    """Lists all the blobs in the bucket that begin with the prefix."""
    blobs = client.list_blobs(bucket_name, prefix=prefix)
    return [blob for blob in blobs if blob.name.endswith('.mp3') or blob.name.endswith('.wav')]

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

def process_files():
    # List files in the bucket
    files = list_files(bucket_name, input_dir)
    for blob in files:
        local_input_path = '/tmp/' + os.path.basename(blob.name)
        local_output_path = '/tmp/output'
        os.makedirs(local_output_path, exist_ok=True)

        # Download the file
        print(f"Downloading {blob.name}")
        download_blob(bucket_name, blob.name, local_input_path)

        # Process the file using allinone
        print(f"Processing {local_input_path}")
        subprocess.run(['python', '-m', 'allin1.cli',
                        '--out-dir','/app/output/analysis',
                        '--viz-dir','/app/output/visualizations',
                        '--sonif-dir','/app/output/sonifications',
                        '--demix-dir','/app/output/tracks',
                        '--spec-dir','/app/output/spectrograms',
                        '--keep-by-products',
                        local_input_path])

        #NOTE: keep_byproducts=True by default is False (without the flag) and deletes the demixed tracks and spectrograms after processing


        local_output_path_final = "/app/output/""
        print(f"Final output is in {local_output_path_final}")

        # Upload the processed file back to GCS
        output_files = os.listdir(local_output_path_final)
        for output_file in output_files:
            full_output_path = os.path.join(local_output_path_final, output_file)
            gcs_output_path = os.path.join(output_dir,filename,os.path.basename(output_file))
            print(f"Uploading {full_output_path} to {gcs_output_path}")
            upload_blob(bucket_name, full_output_path, gcs_output_path)

        # Clean up
        #os.remove(local_input_path)
        #for f in output_files:
        #    os.remove(os.path.join(local_output_path, f))

if __name__ == "__main__":
    process_files()

