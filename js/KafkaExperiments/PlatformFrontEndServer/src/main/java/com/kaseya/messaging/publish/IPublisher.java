package com.kaseya.messaging.publish;

import com.kaseya.messaging.message.*;

public interface IPublisher<K, V>{
    
    public void publish(Message<K, V> msg);
    
    public void shutDown();
}
