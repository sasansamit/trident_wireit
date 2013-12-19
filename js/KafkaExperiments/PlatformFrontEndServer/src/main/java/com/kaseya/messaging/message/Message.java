package com.kaseya.messaging.message;

public class Message<k, v> {
    
    public k key;
    public v value;
    public String topic;
    
    public Message(String topic, k key, v value) {
        //TODO: disallow null topic
        this.key = key;
        this.value = value;
        this.topic = topic;
    }
    
}
