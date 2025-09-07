import { useEffect, useRef, useCallback } from "react";

export default function useWebSocket(props) {
    const { isWsConnected, setIsWsConnected, setLogs } = props;
    const setLogsRef = useRef(setLogs);
    const ws = useRef(null);

    useEffect(() => {
        setLogsRef.current = setLogs;
    }, [setLogs]);

    useEffect(() => {
        // Initialize WebSocket
        if (!isWsConnected && !ws.current) {
            const url = (import.meta.env.VITE_BE_BASE_URL || "")
                .replace(/^http/, 'ws')

            ws.current = new WebSocket(url);
        }

        // On open
        ws.current.onopen = () => {
            console.log("Connected to WebSocket");
            setIsWsConnected(true);
        };

        // On message
        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setLogsRef.current(data);
        };

        // On close
        ws.current.onclose = () => {
            console.log("WebSocket connection closed");
            setIsWsConnected(false);
        };

        // Cleanup WebSocket connection on unmount
        return () => {
            if (ws.current) {
                ws.current.close();
                ws.current = null;
            }
        };
    }, []);

    // Function to send messages through the WebSocket
    const sendMessage = useCallback(
        (message) => {
            if (ws.current && isWsConnected) {
                ws.current.send(message);
            } else {
                console.warn("WebSocket is not connected.");
            }
        },
        [isWsConnected]
    );
}
