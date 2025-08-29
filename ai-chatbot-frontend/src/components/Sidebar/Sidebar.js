import { useSelector, useDispatch } from 'react-redux';
import { setCurrentSession, addSession } from '../../store/slices/sessionsSlice';

const Sidebar = () => {
  const dispatch = useDispatch();
  const sessions = useSelector((state) => state.sessions.sessions);
  const currentSession = useSelector((state) => state.sessions.currentSession);

  const handleNewSession = () => {
    const newSession = {
      id: Date.now(),
      title: `Session ${sessions.length + 1}`,
    };
    dispatch(addSession(newSession));
    dispatch(setCurrentSession(newSession));
  };

  return (
    <div className="sidebar">
      <h3>Sessions</h3>
      <div>
        {sessions.map((s) => (
          <div
            key={s.id}
            className={`session-item ${currentSession?.id === s.id ? 'active' : ''}`}
            onClick={() => dispatch(setCurrentSession(s))}
          >
            {s.title}
          </div>
        ))}
      </div>
      <button className="new-session-btn" onClick={handleNewSession}>
        New Session
      </button>
    </div>
  );
};

export default Sidebar;
