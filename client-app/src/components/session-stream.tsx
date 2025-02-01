import { useEffect, useRef, useState } from "react";

export function SessionStream({ sessionId }: { sessionId: string }) {
  const videoRef = useRef(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [wsInstance, setWsInstance] = useState<WebSocket | null>(null); // <--- Add this line>
  let ws: WebSocket;
  const sendAction = (action:any) => {
    
      if (wsInstance && wsInstance.readyState === WebSocket.OPEN) {
        wsInstance.send(JSON.stringify(action));
      }
    
  };
  const handleClick = (e:any) => {
    const x = e.nativeEvent.offsetX;
    const y = e.nativeEvent.offsetY;
    if(videoRef.current){
        //@ts-ignore
        const { width, height } = videoRef.current.getBoundingClientRect();
        sendAction({ action: "click", payload:{
            x,y,fw:width,fh:height
        } });
    }
   
  };

  const handleKeyDown = (e:any) => {
    sendAction({ action: "type", text: e.key });
  };

  const handleScroll = (e:any) => {
    sendAction({ action: "scroll", dx: e.deltaX, dy: e.deltaY });
  };
  useEffect(() => {
    // Connect to the WebSocket server
    ws = new WebSocket(`ws://127.0.0.1:8000/stream/${sessionId}`);

    setWsInstance(ws);

    ws.onopen = () => {
      console.log("Connected to WebSocket!");
    };

    ws.onmessage = (event) => {
        console.log("got it")
      const blob = new Blob([event.data], { type: "image/png" });
      const url = URL.createObjectURL(blob);
      if (videoRef.current) {
        //@ts-ignore
        videoRef.current.src = url;
      }

   
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setErrorMessage("WebSocket connection failed." + error);
    };

    ws.onclose = () => {
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
      {/* <div className="border rounded bg-gray-100 h-64 flex justify-center items-center">
        {connected ? (
          <img
            ref={videoRef}
            alt="Browser Stream"
            className="max-w-full max-h-full"
          />
        ) : (
          <p>Connecting to browser...</p>
        )}
      </div> */}
      <div 
      tabIndex={0} 
      onKeyDown={handleKeyDown} 
      onWheel={handleScroll} 
      style={{ outline: "none" }}
    >
      <h2>Live Browser Stream</h2>
      <img 
        ref={videoRef}
        alt="Playwright Stream" 
        width="800" 
        onClick={handleClick} 
        style={{ cursor: "pointer" }}
      />
    </div>
      {/* <ul>{messages.map((m)=>{
        return <li>{m}</li>
      })}</ul> */}
    </div>
  );
}
