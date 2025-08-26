# GCP config
	gcloud init

	gcloud auth configure-docker

	# replace GCP_PROJECT_ID	
	gcloud builds submit \
	--config=cloudbuild.yaml \
	--project crowdstream{GCP_PROJECT_ID} \
	--substitutions=_MY_TAG=latest


	# this command avoids caching old version
	gcloud builds submit \
  --config=cloudbuild.yaml \
  --project crowdstream \
  --substitutions=_MY_TAG=$(date -u +%Y%m%d%H%M%S)
  

  gcloud services enable run.googleapis.com cloudbuild.googleapis.com
 JOB=allinone-gpu-job                                  
REGION=us-east4       


GPU quota request
without zonal redunancy lower price
g.co/cloudrun/gpu-quota


To execute this job, use:
gcloud beta run jobs execute allinone-gpu-job  --region=us-east4

GPU and CPU images
gcloud builds submit \
  --config=cloudbuild_gpu.yaml \
  --project crowdstream-443823 \
  --substitutions=_MY_TAG=gpu

  gcloud builds submit \
  --config=cloudbuild_cpu.yaml \
  --project crowdstream-443823 \
  --substitutions=_MY_TAG=cpu



You can verify this by checking the list of images in GCR:
	gcloud container images list --repository=[gcr.io/[PROJECT_ID]](http://gcr.io/%5BPROJECT_ID%5D)


	gcloud run deploy my-allinone-service [params]

Then:
	gcloud builds submit --config cloudbuild.yaml . # enables layer cache, speeds up docker image building


# Job details

## Minimum requirements (review)

mem: 4GiB
cpu: 2

Evaluar: 8GiB
cpu: 4

y timeout: 15min
retries: 3

## Define env vars on GCP config:

then:
	bucket_name = os.getenv('BUCKET_NAME', 'default-bucket-name')
	stems_number = os.getenv('STEMS_NUMBER', '5')


## Download processed dataset
gsutil -m cp -r \
  "gs://[bucketname]-dataset/output" \
  .


$ mkdir sample_audio/loops           
$ gsutil -m cp -R gs://[bucketname]/output sample_audio/loops/    
