#!/bin/bash

git clone https://github.com/openwrt/openwrt

cp openwrt_raspi3_x64_defconfig openwrt/

cd openwrt
git pull

./scripts/feeds update -a

./scripts/feeds install -a

make openwrt_raspi3_x64_defconfig

make

gunzip bin/targets/brcm2708/bcm2710/openwrt-brcm2708-bcm2710-rpi-e-ext4-factory.img.gz


dd if=bin/targets/brcm2708/bcm2710/openwrt-brcm2708-bcm2710-rpi-3-ext4-factory.img of=/dev/mmcblk0



