package com.kaseya.SocketServer;

import java.io.IOException;
import java.util.Properties;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.LinkedBlockingQueue;

import org.json.simple.JSONObject;

import com.kaseya.messaging.publish.Publisher;
import com.netiq.websocket.WebSocket;
import com.netiq.websocket.WebSocketServer;

//import com.kaseya.messaging.publish.*;
    /**
     * A queue broker which accepts messages from Websocket clients and shovels them onto an in-memory data store (for speed).

     */
public class WebSocketQueueBroker extends WebSocketServer {

      /** Queue to mediate between WS server and the class user. May need to be replaced with something more robust. */
      private final BlockingQueue<String> _queue = new LinkedBlockingQueue<String>();
      
      private static final  int _numThreads = 1;
      
      private ExecutorService _executor;
      
      private Publisher<String, String> _publisher;

      /**
       * Start the queue server listening on the default WS port.
       */
      public WebSocketQueueBroker() {
        super();
        init();
      }

      /**
       * Start queue server.
       * 
       * @param port
       *          a particular port to use for WS
       */
      public WebSocketQueueBroker(int port) {
        super(port);
        init();
      }

      /**
       * @param conn
       * 
       * @see com.netiq.websocket.WebSocketServer#onClientClose(com.netiq.websocket.WebSocket)
       */
      @Override
      public void onClientClose(WebSocket conn) {
        // TODO Auto-generated method stub

      }

      /**
       * Takes a new message from a WS client and pushes it into the data store.
       * 
       * @param conn
       *          the connection
       * @param message
       *          the message to store
       * 
       * @see com.netiq.websocket.WebSocketServer#onClientMessage(com.netiq.websocket.WebSocket, java.lang.String)
       */
      @Override
      public void onClientMessage(WebSocket conn, String message) {
        System.out.println("WS queue broker got something");
        this._queue.offer(message);
      }

      /**
       * A new client opens a connection to this server. We need to greet them.
       * 
       * @param conn
       *          the client's connection
       * 
       * @see com.netiq.websocket.WebSocketServer#onClientOpen(com.netiq.websocket.WebSocket)
       */
      @Override
      public void onClientOpen(WebSocket conn) {
        JSONObject msg = new JSONObject();

        // meet n greet
        msg.put("welcome", "client");

        // a handle for the client to get at the output data from Storm
        // i.e. socket.id
        msg.put("outputDataHandle", "1");

        try {
          conn.send(msg.toJSONString());
        }
        catch (IOException e) {
          // Forward to error method
          this.onError(e);
        }
      }

      /**
       * Handles exceptions that may be triggered by WS activities
       * 
       * @param ex
       *          the exception
       * 
       * @see com.netiq.websocket.WebSocketServer#onError(java.lang.Throwable)
       */
      @Override
      public void onError(Throwable ex) {
        System.err.println("Error in WS queue broker");
        ex.printStackTrace();
      }

      /**
       * 
       * @return the next element that needs processing
       */
      public String poll() {
        return this._queue.poll();
      }
      
      public static void main(String[] args) {
          System.out.println("Starting websocket server");
          WebSocketQueueBroker server = new WebSocketQueueBroker(12345);
          server.start();
          System.out.println("Server Started");
          
      }
      
      private void init() {
          System.out.println("Starting Worker pool");
          _executor = Executors.newFixedThreadPool(_numThreads);
          Properties props = new Properties();
          props.put("metadata.broker.list", "localhost:9092");
          props.put("serializer.class", "kafka.serializer.StringEncoder");
          props.put("partitioner.class", "kafka.producer.DefaultPartitioner");
          props.put("request.required.acks", "1");
          _publisher = new Publisher<String, String>(props);
          for(int i=0; i<_numThreads; i++)
          {
              _executor.submit(new WebSocketWorker(_queue, _publisher));
          }
          System.out.println("Worker pool Started");
      }

}

