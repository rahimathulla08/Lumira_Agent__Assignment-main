import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  messages: [],
  isTyping: false,
};

const messagesSlice = createSlice({
  name: 'messages',
  initialState,
  reducers: {
    setMessages: (state, action) => { state.messages = action.payload; },
    addMessage: (state, action) => { state.messages.push(action.payload); },
    clearMessages: (state) => { state.messages = []; },
    setTyping: (state, action) => { state.isTyping = action.payload; },
    startAssistantMessage: (state, action) => {
      state.messages.push({
        id: action.payload.id,
        sessionId: action.payload.sessionId,
        role: 'assistant',
        content: '',
      });
      state.isTyping = true;
    },
    appendToAssistantMessage: (state, action) => {
      const { id, chunk } = action.payload;
      const msg = state.messages.find(m => m.id === id);
      if (msg) {
        msg.content += chunk;
      }
    },
    endAssistantMessage: (state) => {
      state.isTyping = false;
    },
  },
});

export const { setMessages, addMessage, clearMessages, setTyping, startAssistantMessage, appendToAssistantMessage, endAssistantMessage } = messagesSlice.actions;
export default messagesSlice.reducer;
