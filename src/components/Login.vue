<template>
  <div class="login_registration">
    <div class="flex gap-3 mb-4">
      <button
        v-if="!isUserLoggedIn"
        @click="handleLogin"
        :class="['px-6 py-2 rounded-lg font-semibold transition-all', isLoginActive ? 'bg-red-600 text-white shadow-lg' : 'bg-gray-200 text-gray-700 hover:bg-gray-300']"
      >
        Login
      </button>

      <button
        v-if="!isUserLoggedIn"
        @click="handleRegister"
        :class="['px-6 py-2 rounded-lg font-semibold transition-all', isRegisterActive ? 'bg-red-600 text-white shadow-lg' : 'bg-gray-200 text-gray-700 hover:bg-gray-300']"
      >
        Register
      </button>
    </div>

    <p v-if="isRegistrationSuccessfull" class="text-green-600 font-medium mb-4">Registration Successful! Please Login To Continue</p>
  </div>
  <form class="add-form" @submit="onSubmit" v-if="isLoginActive || isRegisterActive">
    <div v-if="isRegisterActive" class="form-control">
      <label>Name</label>
      <input type="text" v-model="name" name="name" placeholder="Your Name" />
    </div>
    <div class="form-control">
      <label>Email</label>
      <input type="email" v-model="email" name="email" placeholder="Email" />
    </div>
    <div class="form-control">
      <label>Password</label>
      <input type="password" name="password" v-model="password" placeholder="Password" />
    </div>
    <input type="submit" :value="isLoginActive ? 'Login' : 'Register'" class="btn btn-block" />
  </form>
</template>

<script>
import { localHost } from '../utils/urls';
import bcrypt from 'bcryptjs';

export default {
  name: 'Login',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      isLoginActive: false,
      isRegisterActive: false,
      isRegistrationSuccessfull: false,
    };
  },
  props: {
    isUserLoggedIn: Boolean,
  },
  emits: ['user-authenticated'],
  methods: {
    handleLogin() {
      this.isLoginActive = !this.isLoginActive;
      this.isRegisterActive = false;
      this.isRegistrationSuccessfull = false;
      this.name = '';
      this.email = '';
      this.password = '';
    },
    handleRegister() {
      this.isRegisterActive = !this.isRegisterActive;
      this.isLoginActive = false;
      this.isRegistrationSuccessfull = false;
      this.name = '';
      this.email = '';
      this.password = '';
    },
    // Handle form submission for both login and registration
    async onSubmit(e) {
      e.preventDefault();
      
      // Validate name for registration
      if (this.isRegisterActive) {
        if (!this.name || this.name.trim().length < 2) {
          alert('Please enter a valid name (at least 2 characters)');
          return;
        }
      }
      
      // Basic email and password validation
      if (this.email.length > 6 && this.email.includes('@') && this.password.length > 6) {
        // Hash password before storing (never store plain text passwords!)
        const user = {
          email: this.email,
          password: bcrypt.hashSync(this.password, 10),
        };

        // Add name only for registration
        if (this.isRegisterActive) {
          user.name = this.name.trim();
        }

        // Registration flow
        if (this.isRegisterActive) {
          // Check if email already exists
          const userName = await fetch(`${localHost}/users?email=${this.email}`);
          const userNameData = await userName.json();

          if (userNameData.length === 0) {
            // Email is available, create new user
            const res = await fetch(`${localHost}/users`, {
              method: 'POST',
              headers: {
                'Content-type': 'application/json',
              },
              body: JSON.stringify(user),
            });

            if (res.status === 201) {
              this.isRegistrationSuccessfull = true;
            } else {
              alert('Registration not Successfull');
            }
          } else {
            alert(`Username ${this.email} is not available`);
          }
        } 
        // Login flow
        else if (this.isLoginActive) {
          // Find user by email
          const existingUserName = await fetch(`${localHost}/users?email=${this.email}`);
          const existingUserNameData = await existingUserName.json();

          if (existingUserNameData.length > 0) {
            // Compare entered password with stored hashed password
            let doesPasswordMatch = bcrypt.compareSync(
              this.password,
              existingUserNameData[0].password,
            );

            if (doesPasswordMatch) {
              this.isLoginActive = false;
              // Store user data in Vuex store
              const userData = {
                email: existingUserNameData[0].email,
                id: existingUserNameData[0].id,
                name: existingUserNameData[0].name || 'User',
              };
              this.$store.commit('userAuthenticated', userData);
              this.$emit('user-authenticated');
            } else {
              alert('Password Incorrect');
            }
          } else {
            alert('User Not Found');
          }
        }
      } else {
        alert('Email not valid or password should be greater than 6 digits');
      }
    },
  },
};
</script>

<style scoped>
.add-form {
  margin-bottom: 40px;
}

.form-control {
  margin: 20px 0;
}

.form-control label {
  display: block;
  color: #1f2937;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-control input {
  width: 100%;
  height: 40px;
  margin: 5px 0;
  padding: 3px 7px;
  font-size: 17px;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.9);
  color: #1f2937;
}

.form-control input::placeholder {
  color: rgba(0, 0, 0, 0.5);
}

.form-control input:focus {
  outline: none;
  border-color: #D90429;
  background: rgba(255, 255, 255, 1);
}

.form-control-check {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.form-control-check label {
  flex: 1;
}

.form-control-check input {
  flex: 2;
  height: 20px;
}

.login_registration {
  text-align: center;
  margin-bottom: 20px;
}

.login_registration p {
  color: #4CAF50;
  margin-top: 10px;
  font-weight: 500;
}

.btn-block {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  background: #D90429;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-block:hover {
  background: #c70325;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(217, 4, 41, 0.4);
}
</style>

