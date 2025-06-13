import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router";

createApp(App)
    .use(router)
    .mount('#app')

fetch('http://localhost:1111/pages', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
