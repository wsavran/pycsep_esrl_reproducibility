@echo off

echo.
echo Building Docker image
echo =====================
docker build \
--build-arg USERNAME=$USER \
--build-arg USER_UID=$(id -u) \
--build-arg USER_GID=$(id -g) \
--no-cache \
-t pycsep_esrl .