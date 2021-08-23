#!/usr/bin/env bash

for dir in $(find /sys/devices/virtual/powercap/intel-rapl -type d -name "intel-rapl:*"); do
  chmod 444 "${dir}/name"
  chmod 444 "${dir}/energy_uj"
done
