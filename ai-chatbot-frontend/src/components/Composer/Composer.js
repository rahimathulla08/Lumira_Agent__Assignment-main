import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { addMessage, startAssistantMessage, appendToAssistantMessage, endAssistantMessage } from '../../store/slices/messagesSlice';

const Composer = () => {
  const [message, setMessage] = useState('');
  const dispatch = useDispatch();
  const currentSession = useSelector((state) => state.sessions.currentSession);

  const handleSend = async () => {
    if (!message.trim() || !currentSession) return;

    const newMessage = {
      id: Date.now(),
      sessionId: currentSession.id,
      role: 'user',
      content: message,
    };

    dispatch(addMessage(newMessage));
    setMessage('');

    // Start assistant streaming message
    const assistantId = Date.now() + 1;
    dispatch(startAssistantMessage({ id: assistantId, sessionId: currentSession.id }));

    try {
      const url = `/api/chat?prompt=${encodeURIComponent(message)}`;
      const response = await fetch(url, { headers: { 'Accept': 'text/event-stream' } });
      if (!response.ok || !response.body) throw new Error('Network error');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        // SSE messages can be separated by "\n\n" or "\r\n\r\n"
        const findDelimiter = (s) => {
          const crlf = s.indexOf('\r\n\r\n');
          const lf = s.indexOf('\n\n');
          if (crlf === -1 && lf === -1) return { idx: -1, len: 0 };
          if (crlf !== -1 && (lf === -1 || crlf < lf)) return { idx: crlf, len: 4 };
          return { idx: lf, len: 2 };
        };

        // Process all complete events in buffer
        while (true) {
          const { idx, len } = findDelimiter(buffer);
          if (idx === -1) break;
          const event = buffer.slice(0, idx).trim();
          buffer = buffer.slice(idx + len);
          if (event.startsWith('data:')) {
            try {
              const jsonStr = event.replace(/^data:\s*/, '');
              const payload = JSON.parse(jsonStr);
              const chunk = payload.response || '';
              if (chunk) {
                dispatch(appendToAssistantMessage({ id: assistantId, chunk }));
              }
            } catch (_) {
              // ignore malformed chunk
            }
          }
        }
      }

      // flush any remaining buffered event
      const trimmed = buffer.trim();
      if (trimmed.startsWith('data:')) {
        try {
          const payload = JSON.parse(trimmed.replace(/^data:\s*/, ''));
          const chunk = payload.response || '';
          if (chunk) dispatch(appendToAssistantMessage({ id: assistantId, chunk }));
        } catch (_) {}
      }
    } catch (e) {
      dispatch(appendToAssistantMessage({ id: assistantId, chunk: ' (error receiving response)' }));
    } finally {
      dispatch(endAssistantMessage());
    }
  };

  return (
    <div className="composer">
      <textarea
        rows="2"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
      />
      <button className="send-btn" onClick={handleSend}>Send</button>
    </div>
  );
};

export default Composer;
