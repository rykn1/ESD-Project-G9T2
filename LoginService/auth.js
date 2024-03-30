import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import {getAuth, onAuthStateChanged} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyCM4fJjQqUmMt8BmQ3Qi7hKVkhRSmzdDkQ",
    authDomain: "esdproj-c3b1c.firebaseapp.com",
    projectId: "esdproj-c3b1c",
    storageBucket: "esdproj-c3b1c.appspot.com",
    messagingSenderId: "477463865668",
    appId: "1:477463865668:web:ffcd62197c671fc679cf11"
  };
  
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app)

  onAuthStateChanged(auth, (user) => {
    if (user) {
        const uid = user.uid;
        const email = user.email;
        console.log(email)
        console.log(uid)
        update_body(uid,"test")
    } else {
        window.location.replace("http://localhost/ESD-Project-G9T2/LoginService/login.html")
    }
  })