import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  sessions: [],
  currentSession: null,
};

const sessionsSlice = createSlice({
  name: 'sessions',
  initialState,
  reducers: {
    setSessions: (state, action) => { state.sessions = action.payload; },
    setCurrentSession: (state, action) => { state.currentSession = action.payload; },
    addSession: (state, action) => { state.sessions.push(action.payload); },
  },
});

export const { setSessions, setCurrentSession, addSession } = sessionsSlice.actions;
export default sessionsSlice.reducer;
