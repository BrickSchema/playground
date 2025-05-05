#!/bin/bash

rm backend.zip frontend.zip

# build backend
zip -r backend.zip backend Dockerfile package.json yarn.lock

# build frontend
cd frontend && zip -r ../frontend.zip .
