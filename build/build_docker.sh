buildDockerImage() {
   DIRECTORY=$1
   LOWER_DIRECTORY=$(echo $DIRECTORY | tr '[:upper:]' '[:lower:]')
   WEB_IMAGE_NAME="${ACR_LOGINSERVER}/$LOWER_DIRECTORY:kube${BUILD_NUMBER}"
   docker build -t $WEB_IMAGE_NAME $DIRECTORY
}  

dirs=`find -name "Dockerfile" | xargs dirname | cut -c 3-`

for directory in $dirs; do
	buildDockerImage $directory
done