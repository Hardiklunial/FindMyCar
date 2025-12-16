<template>
  <div class="login_registration">
    <Button
      v-if="!isUserLoggedIn"
      color="green"
      text="Login"
      eventName="login_clicked"
      @login_clicked="handleLogin"
    />

    <Button
      v-if="!isUserLoggedIn"
      color="grey"
      text="Register"
      eventName="register_clicked"
      @register_clicked="handleRegister"
    />

    <p v-if="isRegistrationSuccessfull">Registration Successfull Please Login To Continue</p>
  </div>
  <form class="add-form" @submit="onSubmit" v-if="isLoginActive || isRegisterActive">
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
import Button from './Button.vue';
import { localHost } from '../utils/urls';
import bcrypt from 'bcryptjs';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      isLoginActive: false,
      isRegisterActive: false,
      isRegistrationSuccessfull: false,
    };
  },
  components: {
    Button,
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
    },
    handleRegister() {
      this.isRegisterActive = !this.isRegisterActive;
      this.isLoginActive = false;
      this.isRegistrationSuccessfull = false;
    },
    async onSubmit(e) {
      e.preventDefault();
      if (this.email.length > 6 && this.email.includes('@') && this.password.length > 6) {
        const user = {
          email: this.email,
          password: bcrypt.hashSync(this.password, 10),
        };

        if (this.isRegisterActive) {
          const userName = await fetch(`${localHost}/users?email=${this.email}`);
          const userNameData = await userName.json();

          if (userNameData.length === 0) {
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
        } else if (this.isLoginActive) {
          const existingUserName = await fetch(`${localHost}/users?email=${this.email}`);
          const existingUserNameData = await existingUserName.json();

          if (existingUserNameData.length > 0) {
            let doesPasswordMatch = bcrypt.compareSync(
              this.password,
              existingUserNameData[0].password,
            );

            if (doesPasswordMatch) {
              console.log('Password Matches');
              this.isLoginActive = false;
              this.$store.commit('userAuthenticated', existingUserNameData[0].email);
              this.$emit('user-authenticated');
            } else {
              alert('Password Incorrect');
            }
          } else {
            alert('User Not Found');
          }

          console.log('login in the user');
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
  color: #fff;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-control input {
  width: 100%;
  height: 40px;
  margin: 5px 0;
  padding: 3px 7px;
  font-size: 17px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.form-control input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-control input:focus {
  outline: none;
  border-color: #D90429;
  background: rgba(255, 255, 255, 0.15);
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

