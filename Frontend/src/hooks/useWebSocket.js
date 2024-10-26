import { useState, useEffect, useRef, useCallback } from 'react';

const useWebSocket = () => {
  const [messages, setMessages] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef(null);

  useEffect(() => {
    // Initialize WebSocket
    if(!isConnected && !ws.current) {
        ws.current = new WebSocket('ws://localhost:8000');
    };

    // On open
    ws.current.onopen = () => {
      console.log('Connected to WebSocket');
      setIsConnected(true);
    };

    // On message
    ws.current.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
      console.log('Received message:', event.data);
    };

    // On close
    ws.current.onclose = () => {
      console.log('Disconnected from WebSocket');
      setIsConnected(false);
    };


    // Cleanup WebSocket connection on unmount
    return () => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.close();
        }
    };
  }, []);

  // Function to send messages through the WebSocket
  const sendMessage = useCallback(
    (message) => {
      if (ws.current && isConnected) {
        ws.current.send(message);
      } else {
        console.warn('WebSocket is not connected.');
      }
    },
    [isConnected]
  );

  return { messages, isConnected, sendMessage };
};

export default useWebSocket;
