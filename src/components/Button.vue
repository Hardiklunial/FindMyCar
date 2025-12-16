<template>
  <button
    :class="['btn', `btn-${color}`]"
    @click="$emit(eventName)"
  >
    {{ text }}
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    text: {
      type: String,
      required: true,
    },
    color: {
      type: String,
      default: 'primary',
    },
    eventName: {
      type: String,
      required: true,
    },
  },
  emits: ['login_clicked', 'register_clicked'],
};
</script>

<style scoped>
.btn {
  padding: 10px 20px;
  margin: 5px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-green {
  background-color: #4CAF50;
  color: white;
}

.btn-green:hover {
  background-color: #45a049;
}

.btn-grey {
  background-color: #9e9e9e;
  color: white;
}

.btn-grey:hover {
  background-color: #757575;
}

.btn-primary {
  background-color: #2196F3;
  color: white;
}

.btn-primary:hover {
  background-color: #1976D2;
}
</style>

