import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import {getAuth, onAuthStateChanged} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "",
    authDomain: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: ""
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
    } else {
        window.location.replace("http://localhost/ESD-Project-G9T2/LoginService/login.html")
    }
  })