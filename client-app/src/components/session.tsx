
export function Session() {
  const createSession = async () => {
    const response = await fetch("http://127.0.0.1:8000/start-browser", {
      method: "POST",
    });
    const res = await response.json();
    const session_id = res.sessionId;
    // setSessionId(session_id);
    window.open(`${import.meta.env.VITE_APP_BASE_URL}/sessions/${session_id}`,"_blank");
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

     
    </>
  );
}
