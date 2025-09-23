from google.cloud import storage
import os
import subprocess
from pathlib import Path

# Procesa archivos .mp3 o .wav

# Initialize the GCS client
client = storage.Client()
bucket_name = os.getenv('BUCKET_NAME', 'default-bucket-name')
input_dir = os.getenv('INPUT_PATH', 'input/')
output_dir = os.getenv('OUTPUT_PATH', 'output-allinone/')

print("PENDING: write processing logs to /logs/")

from tqdm import tqdm
import os

# Controla si TQDM está activado o desactivado mediante una variable de entorno (progress bar)
# En producción, típicamente se desactiva para evitar problemas con logs 
TQDM_OFF = os.getenv("TQDM_DISABLE", "1") == "1"  # default: apagado en prod
tqdm = lambda *a, **k: __import__("tqdm").tqdm(*a, disable=TQDM_OFF, **k)


import torch
import natten
import sys
print("Torch:", torch.__version__)
print("CUDA:", torch.version.cuda)
print("NATTEN:", natten.__version__)
print("Python:", sys.version)

# import torch
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))

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

def blob_exists(bucket_name, blob_name):
    """Check if a blob exists in the bucket."""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.exists()

def check_output_exists(bucket_name, filename, output_dir):
    """Check if output files already exist for this audio file."""
    # Check for the main analysis JSON file which is always generated
    analysis_file = os.path.join(output_dir, filename, f"{filename}.json")
    return blob_exists(bucket_name, analysis_file)

def upload_stems(bucket_name, filename, local_stems_dir, output_dir):
    """Upload demixed stems to GCS bucket."""
    stems_path = local_stems_dir / 'htdemucs' / filename
    if not stems_path.exists():
        print(f"[WARNING] No stems found at {stems_path}")
        return

    stem_files = ['bass.wav', 'drums.wav', 'other.wav', 'vocals.wav']
    uploaded_count = 0

    for stem_file in stem_files:
        local_stem_path = stems_path / stem_file
        if local_stem_path.exists():
            gcs_stem_path = os.path.join(output_dir, filename, 'stems', stem_file)
            print(f"Uploading stem {local_stem_path} to {gcs_stem_path}")
            try:
                upload_blob(bucket_name, str(local_stem_path), gcs_stem_path)
                uploaded_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to upload stem {stem_file}: {e}")
        else:
            print(f"[WARNING] Stem file not found: {local_stem_path}")

    print(f"Uploaded {uploaded_count} stem files for {filename}")

def process_files():
    # List files in the bucket
    files = list_files(bucket_name, input_dir)
    for blob in files:
        filename = os.path.splitext(os.path.basename(blob.name))[0]

        # Check if output already exists for this file
        if check_output_exists(bucket_name, filename, output_dir):
            print(f"Output already exists for {blob.name}, skipping processing.")
            continue

        local_input_path = '/tmp/' + os.path.basename(blob.name)
        #local_output_path = '/app/output/'
        local_output_path = '/app/output/analysis/'
        os.makedirs(local_output_path, exist_ok=True)

        # Download the file
        print(f"Downloading {blob.name}")
        download_blob(bucket_name, blob.name, local_input_path)

        
        # Process the file using allinone
        print(f"Processing {local_input_path}")
        subprocess.run(['python', '-m', 'allin1.cli',
                        '--out-dir','/app/output/analysis',
                        '--keep-byproducts',
                        '--demix-dir','/app/output/stems',
                        # '--viz-dir','/app/output/visualizations',
                        # '--sonif-dir','/app/output/sonifications',
                        # '--spec-dir','/app/output/spectrograms',
                        local_input_path])
        #NOTE: keep_byproducts=True by default is False (without the flag) and deletes the demixed tracks and spectrograms after processing

        print(f"Checking outputs in {local_output_path}")
        try:
            output_files = [f for f in os.listdir(local_output_path) if os.path.isfile(os.path.join(local_output_path, f))]
        except FileNotFoundError:
            print(f"[ERROR] Output directory {local_output_path} not found.")
            continue

        if not output_files:
            print(f"[WARNING] No files found to upload for {blob.name}. Skipping.")
            continue

        # Upload processed files
        for output_file in output_files:
            full_output_path = os.path.join(local_output_path, output_file)
            gcs_output_path = os.path.join(output_dir, filename, output_file)
            print(f"Uploading {full_output_path} to {gcs_output_path}")

            try:
                upload_blob(bucket_name, full_output_path, gcs_output_path)
            except FileNotFoundError:
                print(f"[ERROR] File not found during upload: {full_output_path}")
                continue

        # Upload stems (demixed audio files)
        local_stems_dir = Path('/app/output/stems')
        upload_stems(bucket_name, filename, local_stems_dir, output_dir)

        # Clean-up opcional
        os.remove(local_input_path)
        for f in output_files:
            os.remove(os.path.join(local_output_path, f))

if __name__ == "__main__":
    process_files()

