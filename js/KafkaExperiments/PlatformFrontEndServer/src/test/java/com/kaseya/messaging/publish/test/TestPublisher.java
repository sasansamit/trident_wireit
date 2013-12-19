package com.kaseya.messaging.publish.test;

import com.kaseya.messaging.publish.*;
import com.kaseya.messaging.message.*;

import java.util.*;

public class TestPublisher {

    public static void main(String[] args) {
        // TODO Auto-generated method stub
        Properties props = new Properties();
        
        props.put("metadata.broker.list", "localhost:9092");
        props.put("serializer.class", "kafka.serializer.StringEncoder");
        props.put("partitioner.class", "kafka.producer.DefaultPartitioner");
        props.put("request.required.acks", "1");
        Publisher<String, String> testPublisher = new Publisher<String, String>(props);
        int sent = 0;
        while(sent < 10)
        {
            testPublisher.publish(new Message<String, String>("UnitTestTopic", "FirstTopic", String.valueOf(sent++)));
        }
        System.out.print("Published "+ String.valueOf(sent) + "Messages");

    }

}
