# Kafka Quickstart
# Terminal 1
./bin/zookeeper-server-start.sh config/zookeeper.properties
# Terminal 2
./bin/kafka-server-start.sh config/server.properties

# Terminal 3: create topic
./bin/kafka-topics.sh --create --topic uji-praktikum --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
./bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Terminal 3: producer
./bin/kafka-console-producer.sh --topic uji-praktikum --bootstrap-server localhost:9092
# Type messages

# Terminal 4: consumer
./bin/kafka-console-consumer.sh --topic uji-praktikum --from-beginning --bootstrap-server localhost:9092
