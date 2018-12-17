set -e

chmod +x ./build/install.sh
chmod +x ./build/validate.sh

./build/install.sh
./build/validate.sh

chmod +x ./build/build_docker.sh
chmod +x ./build/push_docker.sh

./build/build_docker.sh
./build/push_docker.sh