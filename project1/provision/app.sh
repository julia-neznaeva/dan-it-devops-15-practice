#!/bin/bash
GIT_USERNAME="julia.neznaeva"
GIT_TOKEN="glpat-6o8urmBHwLlWDwYTFny_lmM6MQpvOjEKdTpteWltbA8.01.1702yem4o"
REPO_URL="https://gitlab.com/dan-it/groups/devops_soft.git"

APP_USER="petclinic"
PROJECT_SOURCE_DIR="/home/petclinic/devops_soft/forStep1/PetClinic"
PROJECT_DIR="/home/petclinic/devops_soft"
APP_DIR="/opt/petclinic"
REPO_HOST_PATH="gitlab.com/dan-it/groups/devops_soft.git"
JAR_NAME="spring-petclinic-2.3.1.BUILD-SNAPSHOT.jar"

set -ex
apt update
apt install -y openjdk-8-jdk git

if ! id "$APP_USER" > /dev/null 2>&1; then
  echo "Create app user"
  useradd -m -s /bin/bash "$APP_USER"
fi

if [ ! -d "$PROJECT_DIR" ]; then
  echo "Git clone"
  sudo -u "$APP_USER" git clone "https://${GIT_USERNAME}:${GIT_TOKEN}@${REPO_HOST_PATH}" "$PROJECT_DIR"
fi

if [ ! -d "$APP_DIR" ]; then
  echo "Create petclinic app folder"
  mkdir -p "$APP_DIR"
  
  echo "Access to APP_DIR"
  chown -R "$APP_USER":"$APP_USER" "$APP_DIR"
  chmod +x ${PROJECT_SOURCE_DIR}/mvnw
fi

 sudo -u "$APP_USER" bash -c "cd ${PROJECT_SOURCE_DIR} && ./mvnw clean package"

  echo "Copy jar file"
  cp ${PROJECT_SOURCE_DIR}/target/${JAR_NAME} ${APP_DIR}/petclinic.jar

  echo "Mysql profile, export env vars, "
 sudo -u petclinic bash <<EOF
  export SPRING_PROFILES_ACTIVE=mysql
  export MYSQL_URL=jdbc:mysql://192.168.56.11:3306/petclinic
  export MYSQL_USER=petclinic
  export MYSQL_PASS=password
  java -jar /opt/petclinic/petclinic.jar
EOF
