import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import messagesReducer from './slices/messagesSlice';
import sessionsReducer from './slices/sessionsSlice';

const PERSIST_KEY = 'chat_state_v1';

function loadState() {
  try {
    const serialized = localStorage.getItem(PERSIST_KEY);
    if (!serialized) return undefined;
    return JSON.parse(serialized);
  } catch (e) {
    return undefined;
  }
}

function saveState(state) {
  try {
    const toPersist = {
      messages: { messages: state.messages.messages },
      sessions: { sessions: state.sessions.sessions, currentSession: state.sessions.currentSession },
      auth: state.auth,
    };
    localStorage.setItem(PERSIST_KEY, JSON.stringify(toPersist));
  } catch (e) {
    // ignore write errors
  }
}

const preloadedState = loadState();

export const store = configureStore({
  reducer: {
    auth: authReducer,
    messages: messagesReducer,
    sessions: sessionsReducer,
  },
  preloadedState,
});

store.subscribe(() => saveState(store.getState()));

export default store;
