import { useState, useEffect, useRef, useCallback } from "react";
import { useStepDataContext } from "../context/StepDataContext";

export default function useWebSocket() {
    const { setLogs } = useStepDataContext();
    const setLogsRef = useRef(setLogs);
    const ws = useRef(null);
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        setLogsRef.current = setLogs;
    }, [setLogs]);
    

    useEffect(() => {
        // Initialize WebSocket
        if (!isConnected && !ws.current) {
            ws.current = new WebSocket("ws://localhost:8000");
        }

        // On open
        ws.current.onopen = () => {
            console.log("Connected to WebSocket");
            setIsConnected(true);
        };

        // On message
        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setLogsRef.current(data); 
        };

        // On close
        ws.current.onclose = () => {
            console.log("Disconnected from WebSocket");
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
                console.warn("WebSocket is not connected.");
            }
        },
        [isConnected]
    );
}
