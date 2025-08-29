import { useSelector, useDispatch } from 'react-redux';
import { setCurrentSession } from '../../store/slices/sessionsSlice';

const ProviderPanel = () => {
  const dispatch = useDispatch();
  const currentSession = useSelector((state) => state.sessions.currentSession);
  const providers = ['OpenAI', 'Claude', 'Gemini'];

  const handleChange = (e) => {
    if (!currentSession) return;

    const updatedSession = { ...currentSession, provider: e.target.value };
    dispatch(setCurrentSession(updatedSession));
  };

  return (
    <div className="provider-panel">
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{ fontWeight: 700, fontSize: 16, color: 'var(--text)' }}>Lumira</div>
        <div style={{ opacity: .7 }}>|</div>
        <div>
          <span style={{ marginRight: 8 }}>Provider</span>
          <select value={currentSession?.provider || ''} onChange={handleChange}>
            <option value="">Select</option>
            {providers.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default ProviderPanel;
