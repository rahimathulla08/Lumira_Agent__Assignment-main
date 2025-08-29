
import Sidebar from './components/Sidebar/Sidebar';
import ChatArea from './components/ChatArea/ChatArea';
import Composer from './components/Composer/Composer';
import ProviderPanel from './components/ProviderPanel/ProviderPanel';
import './App.css';

function App() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-pane">
        <ProviderPanel />
        <ChatArea />
        <Composer />
      </div>
    </div>
  );
}

export default App;
