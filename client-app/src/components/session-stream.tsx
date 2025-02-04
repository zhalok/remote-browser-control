import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";

export function SessionStream({ }: {  }) {
  const { id:sessionId } = useParams<{id:string}>();
  const videoRef = useRef(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [gotoUrl, setGotoUrl] = useState("");
  const [wsInstance, setWsInstance] = useState<WebSocket | null>(null); // <--- Add this line>
  let ws: WebSocket;
  const sendAction = (action: any) => {
    if (wsInstance && wsInstance.readyState === WebSocket.OPEN) {
      wsInstance.send(JSON.stringify(action));
    }
  };
  const handleClick = (e: any) => {
    const x = e.nativeEvent.offsetX;
    const y = e.nativeEvent.offsetY;
    if (videoRef.current) {
      //@ts-ignore
      const { width, height } = videoRef.current.getBoundingClientRect();
      sendAction({
        action: "click",
        payload: {
          x,
          y,
          fw: width,
          fh: height,
        },
      });
    }
  };

  const handleKeyDown = (e: any) => {
    sendAction({ action: "type", payload: { text: e.key } });
  };

  const handleScroll = (e: any) => {
    sendAction({ action: "scroll", payload: { dx: e.deltaX, dy: e.deltaY } });
  };
  useEffect(() => {
    // Connect to the WebSocket server
    ws = new WebSocket(`${import.meta.env.VITE_APP_WS_BASE_URL}/stream/${sessionId}`);

    setWsInstance(ws);

    ws.onopen = () => {
      console.log("Connected to WebSocket!");
    };

    ws.onmessage = (event) => {
      console.log("got it");
      const blob = new Blob([event.data], { type: "image/png" });
      const url = URL.createObjectURL(blob);
      if (videoRef.current) {
        //@ts-ignore
        videoRef.current.src = url;
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      videoRef.current = null;
      setErrorMessage("WebSocket connection failed." + error);
    };

    ws.onclose = () => {
      videoRef.current = null;
      console.log("WebSocket closed.");
      setWsInstance(null)
      window.close()
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
      <button onClick={()=>{
        wsInstance && wsInstance.close()
        window.close()
       setWsInstance(null)
      }}>Close Connection</button>
      <h2 className="text-xl font-bold mb-4">Browser Stream</h2>
      {errorMessage && <p className="text-red-500">{errorMessage}</p>}

      <div
        tabIndex={0}
        onKeyDown={handleKeyDown}
        onWheel={handleScroll}
        style={{ outline: "none" }}
      >
        <h2>Live Browser Stream</h2>
        <div>
        <input
          value={gotoUrl}
          onChange={(e) => {
            const val = e.target.value;
            const valText = val.startsWith("http") ? val : `http://${val}`;
            setGotoUrl(valText);
          }}
        />
        <button
          onClick={() =>
            //@ts-ignore

            wsInstance &&
            wsInstance.send(
              JSON.stringify({ action: "goto", payload: { url: gotoUrl } })
            )
          }
        >
          Go to URL
        </button>
        </div>
       
        
        <img
          ref={videoRef}
          alt="Playwright Stream"
          width="800"
          onClick={handleClick}
          style={{ cursor: "pointer" }}
        />
      </div>
    </div>
  );
}
