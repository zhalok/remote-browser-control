import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import { Session } from "./components/session";
import { SessionStream } from "./components/session-stream";

function App() {
  return (
    <>
      <BrowserRouter>
        {" "}
        <Routes>
          <Route path="/" element={<Session />} />
          <Route path="/sessions/:id" element={<SessionStream />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
