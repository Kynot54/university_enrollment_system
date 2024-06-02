# cpsc449-fall2023-project4
CPSC 449 - Fall 2023 - Project 4 - Asynchronous Messaging and Conditional GET

Project members:
- Jimmy Quach
- Kyle Whynott
- Stephanie Becerra
- Kendrick Ngo
- Rich Bui
- ..


# Development

1. Set working directory as this project's directory

2. Configure Python

   ```bash
   sudo apt install --yes python3-pip python3-venv
   python3.10 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure SQLite

   ```bash
   sudo apt update
   sudo apt install --yes sqlite3
   ```

4. Configure Foreman

   ```bash
   sudo apt update
   sudo apt install --yes ruby-foreman
   ```

5. Configure KrakenD

   ```bash
   sudo apt install ca-certificates gnupg
   sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 5DE6FD698AD6FDD2
   echo "deb https://repo.krakend.io/apt stable main" | sudo tee /etc/apt/sources.list.d/krakend.list
   sudo apt update
   sudo apt install --yes krakend
   sudo apt install --yes entr
   ```

6. Configure Redis CLI

   You will need to have Redis CLI installed and running on the system at port 6379. You can verify this by running the following command:

   ```bash
   redis-cli ping
   ```

   Otherwise install redis:
   ```bash
   sudo apt update
   sudo apt install --yes redis
   ```

7. Configure AWS CLI

   You will need to follow the instructions on the Long-term credentials tab of [Configuring using AWS CLI commands](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html#getting-started-quickstart-new-command) to configure dummy credentials for DynamoDB local.

   ```bash
   sudo apt update
   sudo apt install --yes openjdk-19-jre-headless
   ```

8. Configure RabbitMQ

   You will need to have RabbitMQ installed and running on the system. You can verify this by running the following command:

   ```bash
   sudo rabbitmqctl ping
   ```

   ```bash
   sudo apt update
   sudo apt install --yes rabbitmq-server
   ```

9. Start API

   ```bash
   chmod +x ./bin/deploy.sh
   ./bin/deploy.sh
   ```

10. Initialize databases
   
   If databases haven't been initialized yet (ie. this is the first run), run the following **after running one of the commands above, which activates the LiteFS replication service**:

   ```bash
   chmod +x ./bin/init.sh
   ./bin/init.sh
   ```

   You may also wish to run this in development to reset the database, especially if a schema has been changed.
