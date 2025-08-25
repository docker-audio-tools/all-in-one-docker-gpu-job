AUDIO_PATH=$PWD/audio
RESULTS_PATH=$PWD/results
TRACKS_PATH=$PWD/tracks
FILENAME=$1

# predownload model (-m MODEL) to avoid downloading it each time
# WARNING each execution downloads the demucs model again
# Downloading: "https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/955717e8-8726e21a.th" to /root/.cache/torch/hub/checkpoints/955717e8-8726e21a.th

docker run -it \
     -v $AUDIO_PATH:/app/input \
     -v $RESULTS_PATH:/app/output \
     -v $TRACKS_PATH:/app/tracks \
     allinone \
     --out-dir /app/output/analysis \
     --viz-dir /app/output/visualizations \
     --sonif-dir /app/output/sonifications \
     --demix-dir /app/tracks \
     --spec-dir /app/output/spectrograms \
     --keep-byproducts \
     /app/input/$FILENAME


# ✦ Por defecto, los tracks de demux sí se borran al finalizar el script.
#   El script src/allin1/cli.py tiene un argumento --keep-byproducts que por defecto es False.
#   Dentro de la función analyze en src/allin1/analyze.py, hay una sección que verifica el valor de keep_byproducts. Si es False, se borran los
#   archivos de audio demixeados y los espectrogramas.
#   Para evitar que se borren, es necesario ejecutar el script con el flag --keep-byproducts.

# usage: cli.py [-h] [-o OUT_DIR] [-v] [--viz-dir VIZ_DIR] [-s] [--sonif-dir SONIF_DIR] [-a] [-e] [-m MODEL] [-d DEVICE] [-k] [--demix-dir DEMIX_DIR]
#               [--spec-dir SPEC_DIR] [--overwrite] [--no-multiprocess]
#               paths [paths ...]