import { useState } from "react";
import { SessionStream } from "./session-stream";

export function Session() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const createSession = async () => {
    const response = await fetch("http://127.0.0.1:8000/start-browser", {
      method: "POST",
    });
    const res = await response.json();
    const session_id = res.sessionId;
    setSessionId(session_id);
  };
  return (
    <>
       <button
          onClick={() => {
            createSession();
          }}
        >
          Create session
        </button>

      <>
        {sessionId && (
          <>
            <SessionStream
              sessionId={sessionId}
              handleSessionClose={() => {
                setSessionId(null);
              }}
            />
          </>
        )}
      </>
    </>
  );
}
