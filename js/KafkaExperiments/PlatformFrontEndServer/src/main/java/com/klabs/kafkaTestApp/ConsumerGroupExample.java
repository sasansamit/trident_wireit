package com.klabs.kafkaTestApp;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import kafka.consumer.ConsumerConfig;
import kafka.consumer.KafkaStream;
import kafka.javaapi.consumer.ConsumerConnector;

public class ConsumerGroupExample {
    private final ConsumerConnector consumer;
    private final String            topic;
    private ExecutorService         executor;

    public ConsumerGroupExample(String a_zookeeper, String a_groupId, String a_topic) {
        consumer = kafka.consumer.Consumer.createJavaConsumerConnector(createConsumerConfig(a_zookeeper,
                                                                                            a_groupId));
        this.topic = a_topic;
    }

    public void shutdown() {
        System.out.println("Shutting down");
        if (consumer != null)
            consumer.shutdown();
        if (executor != null)
            executor.shutdown();
    }

    public void run(int a_numThreads) {
        Map<String, Integer> topicCountMap = new HashMap<String, Integer>();
        topicCountMap.put(topic, new Integer(a_numThreads));
        Map<String, List<KafkaStream<byte[], byte[]>>> consumerMap = consumer.createMessageStreams(topicCountMap);
        List<KafkaStream<byte[], byte[]>> streams = consumerMap.get(topic);
        System.out.println("Total stream obtained: " +streams.size());

        // now launch all the threads
        //
        executor = Executors.newFixedThreadPool(a_numThreads);

        // now create an object to consume the messages
        //
        int threadNumber = 0;
        for (final KafkaStream stream : streams) {
            executor.submit(new ConsumerTest(stream, threadNumber));
            threadNumber++;
        }
    }

    private static ConsumerConfig createConsumerConfig(String a_zookeeper, String a_groupId) {
        Properties props = new Properties();
        props.put("zookeeper.connect", a_zookeeper);
        props.put("group.id", a_groupId);
        props.put("zookeeper.session.timeout.ms", "400");
        props.put("zookeeper.sync.time.ms", "200");
        props.put("auto.commit.interval.ms", "1000");

        return new ConsumerConfig(props);
    }

    public static void main(String[] args) {
        System.out.println("Starting 1");
        try {
            String zooKeeper = "localhost:2181";
            String groupId = "1000";
            String topic = "topic7-p5-r1";
            int threads = 5;

            ConsumerGroupExample example = new ConsumerGroupExample(zooKeeper, groupId, topic);
            example.run(threads);

            try {
                Thread.sleep(60000);
            } catch (InterruptedException ie) {

            }
            example.shutdown();
        } catch (Exception e) {
            // TODO Auto-generated catch block
            System.out.println("Samit " + e.getMessage());
            e.printStackTrace();
        }
    }
}
