import { createStore } from 'vuex';

export default createStore({
  state: {
    isUserLoggedIn: false,
    userEmail: null,
    userId: null,
    userName: null,
  },
  mutations: {
    // Called when user successfully logs in
    // Updates Vuex state and saves to localStorage for persistence
    userAuthenticated(state, userData) {
      state.isUserLoggedIn = true;
      state.userEmail = userData.email;
      state.userId = userData.id;
      state.userName = userData.name || 'User';
      // Save to localStorage so user stays logged in after page refresh
      localStorage.setItem('isUserLoggedIn', 'true');
      localStorage.setItem('userEmail', userData.email);
      localStorage.setItem('userId', userData.id);
      localStorage.setItem('userName', userData.name || 'User');
    },
    // Called when user logs out
    // Clears Vuex state and removes from localStorage
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
    // Called when app starts to restore login state from localStorage
    initializeAuth(state) {
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

