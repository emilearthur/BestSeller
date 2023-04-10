docker run --rm -it \
    -v $PWD/layers:/tmp/layers \
    -v $PWD/src/requirements_layers.txt:/tmp/requirements.txt \
    --platform=linux/x86_64 \
    --env PIP_INDEX_URL=$PIP_INDEX_URL \
    public.ecr.aws/sam/build-python3.9:latest-x86_64 \
    pip install -r /tmp/requirements.txt --target /tmp/layers/python