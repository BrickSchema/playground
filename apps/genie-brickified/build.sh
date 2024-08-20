#!/bin/bash

rm backend.zip frontend.zip

# build backend
zip -r backend.zip configs geniebackend Dockerfile requirements.txt

# build frontend
# yarn build
cd build
zip -r ../frontend.zip .
cd ..
