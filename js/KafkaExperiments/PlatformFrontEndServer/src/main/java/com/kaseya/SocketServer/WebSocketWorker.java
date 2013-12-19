package com.kaseya.SocketServer;

import java.util.concurrent.BlockingQueue;

import org.json.simple.JSONValue;
import org.json.simple.JSONObject;
import com.kaseya.messaging.publish.*;
import com.kaseya.messaging.message.*;


public class WebSocketWorker implements Runnable {
    
    private final BlockingQueue<String> _queue;
    private final Publisher<String, String> _pub;
    
    public WebSocketWorker(BlockingQueue<String> q, Publisher<String, String> pub) {
        _queue = q;
        _pub = pub;
    }
    
    public void run() {
        try {
            while (true) {process( _queue.take().toString()); }
          } catch (InterruptedException ex) {
              System.out.println("Exception in Worker"+ ex.toString());
          }
    }
    
    private void process(String msg) {
        System.out.println("Thread received message" + msg);
        //JSONObject obj = (JSONObject)JSONValue.parse(msg);
        //TODO: we can extract topic information from messages itself
        _pub.publish(new Message<String, String>("memory", null, msg));
        
    }
    

}
