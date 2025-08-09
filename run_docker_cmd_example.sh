AUDIO_PATH=$PWD/audio
RESULTS_PATH=$PWD/results
FILENAME=$1

docker run -it \
     -v $AUDIO_PATH:/app/input \
     -v $RESULTS_PATH:/app/output \
     allinone \
     --out-dir /app/output/analysis \
     --viz-dir /app/output/visualizations \
     --sonif-dir /app/output/sonifications \
     /app/input/$FILENAME
