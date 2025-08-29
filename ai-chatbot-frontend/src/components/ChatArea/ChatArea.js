import { useSelector } from 'react-redux';

const ChatArea = () => {
  const messages = useSelector((state) => state.messages.messages);
  const currentSession = useSelector((state) => state.sessions.currentSession);

  // Filter messages by current session
  const sessionMessages = messages.filter(
    (m) => m.sessionId === currentSession?.id
  );

  const isTyping = useSelector((state) => state.messages.isTyping);

  return (
    <div className="chat-container">
      {currentSession ? (
        <>
          {sessionMessages.map((m) => (
            <div key={m.id} className={`bubble-row ${m.role === 'user' ? 'end' : 'start'}`}>
              <div className={`bubble ${m.role}`}>{m.content}</div>
            </div>
          ))}
          {isTyping && (
            <div className="bubble-row start">
              <div className="bubble assistant">
                <span className="typing">•••</span>
              </div>
            </div>
          )}
        </>
      ) : (
        <p>Select a session to start chatting</p>
      )}
    </div>
  );
};

export default ChatArea;
