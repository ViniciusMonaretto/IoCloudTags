#!/bin/sh

cd ./web-page

echo "Build angular app"

ng build

cd ../server/src

rm -rf ./webApp
mkdir ./webApp

cp ../../web-page/dist/web-page/* ./webApp
