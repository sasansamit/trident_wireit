package com.klabs.kafkaTestApp;


import java.util.*;

import kafka.admin.*;
import kafka.javaapi.producer.Producer;
import kafka.producer.KeyedMessage;
import kafka.producer.ProducerConfig;

public class KafkaProducer {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
	    
	    String [] arguments = new String[8];
        arguments[0] = "--zookeeper";
        arguments[1] = "localhost:2181";
        arguments[2] = "--replica";
        arguments[3] = "1";
        arguments[4] = "--partition";
        arguments[5] = "11";
        arguments[6] = "--topic";
        arguments[7] = "topic8-p5-r1";

        CreateTopicCommand.main(arguments);
        try {
            Thread.sleep(6000);
        } catch (InterruptedException ie) {

        }
		
        Properties props = new Properties();
        props.put("metadata.broker.list", "localhost:9092");
        props.put("serializer.class", "kafka.serializer.StringEncoder");
        props.put("partitioner.class", "kafka.producer.DefaultPartitioner");
        props.put("request.required.acks", "1");
 
        ProducerConfig config = new ProducerConfig(props);
 
        Producer<String, String> producer = new Producer<String, String>(config);
        int partitionId = 0;
        long sent = 0;
 
        while(partitionId < 5) {
                 
               
               String key = String.valueOf(partitionId++);
               System.out.println("Publishing on " + key);
               //On Every Partion publish 20 messages
               for(int i=0; i<20; i++) {
                   String msg = String.valueOf(i) ;
                   KeyedMessage<String, String> data = new KeyedMessage<String, String>("topic8-p5-r1", key, msg);
                   producer.send(data);
               }
               
        }
        producer.close();
        System.out.println("Producing complete");
	}

}
