# Базовий образ Jenkins inbound agent
FROM jenkins/inbound-agent:latest

USER root
# Встановлюємо Docker CLI всередині контейнера
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

# Створюємо групу docker (якщо її немає) і додаємо користувача jenkins
RUN groupadd -f docker && \
    usermod -aG docker jenkins && \
    echo 'export PATH=$PATH:/usr/bin' >> /home/jenkins/.profile

