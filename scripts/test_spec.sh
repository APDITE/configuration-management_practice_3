#!/bin/sh
# Демонстрация: ассемблер выдаёт поля и байты из тестов спецификации.

cd "$(dirname "$0")/.." || exit 1
mkdir -p out
./run.sh asm -i programs/spec.yaml -o out/spec.bin --test
