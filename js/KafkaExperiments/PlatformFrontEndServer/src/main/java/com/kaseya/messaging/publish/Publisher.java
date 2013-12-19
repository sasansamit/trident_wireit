package com.kaseya.messaging.publish;

import java.util.*;

import kafka.javaapi.producer.Producer;
import kafka.producer.*;

import com.kaseya.messaging.message.Message;

public class Publisher<K, V> implements IPublisher<K, V> {
    
    private Producer<K, V> m_kafkaPublisher;
    
    public Publisher(Properties prop) {
        m_kafkaPublisher = new Producer<K, V>(new ProducerConfig(prop));
    }
    
    public void publish(Message<K, V> msg) {
        KeyedMessage<K, V> data = new KeyedMessage<K, V>(msg.topic, msg.key, msg.value);
        m_kafkaPublisher.send(data);
    }
    
    
    
    public void shutDown() {
        m_kafkaPublisher.close();
    }
    
}
