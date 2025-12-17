import { createStore } from 'vuex';

export default createStore({
  state: {
    isUserLoggedIn: false,
    userEmail: null,
    userId: null,
    userName: null,
  },
  mutations: {
    userAuthenticated(state, userData) {
      state.isUserLoggedIn = true;
      state.userEmail = userData.email;
      state.userId = userData.id;
      state.userName = userData.name || 'User';
      // Store in localStorage for persistence
      localStorage.setItem('isUserLoggedIn', 'true');
      localStorage.setItem('userEmail', userData.email);
      localStorage.setItem('userId', userData.id);
      localStorage.setItem('userName', userData.name || 'User');
    },
    userLoggedOut(state) {
      state.isUserLoggedIn = false;
      state.userEmail = null;
      state.userId = null;
      state.userName = null;
      localStorage.removeItem('isUserLoggedIn');
      localStorage.removeItem('userEmail');
      localStorage.removeItem('userId');
      localStorage.removeItem('userName');
    },
    initializeAuth(state) {
      // Check localStorage on app initialization
      const isLoggedIn = localStorage.getItem('isUserLoggedIn');
      const email = localStorage.getItem('userEmail');
      const userId = localStorage.getItem('userId');
      const userName = localStorage.getItem('userName');
      if (isLoggedIn === 'true' && email) {
        state.isUserLoggedIn = true;
        state.userEmail = email;
        state.userId = userId;
        state.userName = userName;
      }
    },
  },
  actions: {},
  modules: {},
});

