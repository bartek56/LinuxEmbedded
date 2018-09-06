#!/bin/bash

path=$PWD

mkdir yocto
cd yocto


git clone -b sumo git://git.yoctoproject.org/poky
git clone -b sumo git://git.openembedded.org/meta-openembedded
git clone -b sumo git://git.yoctoproject.org/meta-raspberrypi
git clone -b sumo https://github.com/meta-qt5/meta-qt5.git


source poky/oe-init-build-env build
cd ..
yocto-layer create mylayer

cd meta-mylayer

mkdir recipes-example recipes-example/example
cp $path/basicquick_0.1.bb recipes-example/example/basicquick_0.1.bb

mkdir recipes-core recipes-core/image
cp $path/qt5-raspberrypi3-image.bb  /recipes-core/image/qt5-raspberrypi3-image.bb

mkdir recipes-ext recipes-ext/qt
cp $path/qtbase_git.bbappend recipes-ext/qt/qtbase_git.bbappend

cp $path/bblayers.conf conf/bblayers.conf
cp $path/local.conf conf/local.conf

bitbake qt5-raspberrypi3-image



