set -e

echo "Updating package list..."
apt-get update -y

echo "Installing OpenJDK 11..."
apt-get install -y openjdk-11-jdk

echo "Setting up JAVA_HOME environment variable..."
JAVA_HOME_PATH="/usr/lib/jvm/java-11-openjdk-amd64"
export JAVA_HOME=$JAVA_HOME_PATH
export PATH=$JAVA_HOME/bin:$PATH

echo "Verifying Java installation..."
java -version

echo "Verifying libjvm.so file..."
LIBJVM_PATH="$JAVA_HOME_PATH/lib/server/libjvm.so"
if [ -f "$LIBJVM_PATH" ]; then
    echo "libjvm.so found at $LIBJVM_PATH"
else
    echo "Error: libjvm.so not found. Please check the Java installation."
    exit 1
fi

echo "Setup completed successfully!"