set -e

pushDockerImage() {
   DIRECTORY=$1
   LOWER_DIRECTORY=$(echo $DIRECTORY | tr '[:upper:]' '[:lower:]')
   WEB_IMAGE_NAME="${ACR_LOGINSERVER}/$LOWER_DIRECTORY:kube${BUILD_NUMBER}"
   docker push $WEB_IMAGE_NAME
}  

dirs=`find -name "Dockerfile" | xargs dirname | cut -c 3-`

for directory in $dirs; do
	pushDockerImage $directory
done