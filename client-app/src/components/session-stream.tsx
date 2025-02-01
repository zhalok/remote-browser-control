import { useEffect, useRef, useState } from "react";

export function SessionStream({ sessionId }: { sessionId: string }) {
  const videoRef = useRef(null);
  const [connected, setConnected] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [messages,setMessages] = useState<string[]>([])
  let ws: WebSocket;
  useEffect(() => {
    // Connect to the WebSocket server
    ws = new WebSocket(`ws://127.0.0.1:8000/stream/${sessionId}`);

    ws.onopen = () => {
      setConnected(true);
      console.log("Connected to WebSocket!");
    };

    ws.onmessage = (event) => {
      const blob = new Blob([event.data], { type: "image/png" });
      const url = URL.createObjectURL(blob);
      if (videoRef.current) {
        //@ts-ignore
        videoRef.current.src = url;
      }

    // setMessages((m)=>{
    //     return [...m,event.data]
    // })

    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setErrorMessage("WebSocket connection failed."+error,);
    };

    ws.onclose = () => {
      setConnected(false);
      console.log("WebSocket closed.");
    };

    // Clean up on unmount
    return () => {
    //   if (ws) {
    //     ws.close();
    //   }
    };
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Browser Stream</h2>
      {errorMessage && <p className="text-red-500">{errorMessage}</p>}
      <div className="border rounded bg-gray-100 h-64 flex justify-center items-center">
        {connected ? (
          <img ref={videoRef} alt="Browser Stream" className="max-w-full max-h-full" />
        ) : (
          <p>Connecting to browser...</p>
        )}
      </div>
      {/* <ul>{messages.map((m)=>{
        return <li>{m}</li>
      })}</ul> */}
    </div>
  );
}
