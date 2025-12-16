import { createStore } from 'vuex';

export default createStore({
  state: {
    isUserLoggedIn: false,
    userEmail: null,
  },
  mutations: {
    userAuthenticated(state, email) {
      state.isUserLoggedIn = true;
      state.userEmail = email;
      // Store in localStorage for persistence
      localStorage.setItem('isUserLoggedIn', 'true');
      localStorage.setItem('userEmail', email);
    },
    userLoggedOut(state) {
      state.isUserLoggedIn = false;
      state.userEmail = null;
      localStorage.removeItem('isUserLoggedIn');
      localStorage.removeItem('userEmail');
    },
    initializeAuth(state) {
      // Check localStorage on app initialization
      const isLoggedIn = localStorage.getItem('isUserLoggedIn');
      const email = localStorage.getItem('userEmail');
      if (isLoggedIn === 'true' && email) {
        state.isUserLoggedIn = true;
        state.userEmail = email;
      }
    },
  },
  actions: {},
  modules: {},
});

