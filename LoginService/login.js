
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import {getAuth, createUserWithEmailAndPassword, onAuthStateChanged, signInWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

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

const signupEmailPassword = async () => {  
  
  const signupEmail = document.getElementById('signup-email').value.toLowerCase().trim(); // Convert email input into lowercase
  const signupPassword = document.getElementById('signup-password').value.trim();
  const confirmPassword = document.getElementById('signup-password-confirm').value.trim();


  if (confirmPassword.length == 0 || signupEmail.length == 0 || signupPassword.length == 0) { //Check if any blanks
    showSignUpError('blank')
  } else if (signupPassword != confirmPassword) {
    showSignUpError('diff')
  } else if (signupPassword.length <6) { // Check if password less than 6 characters
    showSignUpError('short')
  } else {
    showSignUpError('none') // No error
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, signupEmail, signupPassword) //Create account in firebase authentication 
      // const db = getDatabase();
      const user = userCredential.user
      console.log(user)
      

    }
    catch(error) {
      console.log(error);
      showSignUpError(error.code); //Show error code
    }
  }}

  

  const loginEmailPassword = async () => { //Login user
    const loginEmail = document.getElementById('login-email').value.trim();
    const loginPassword = document.getElementById('login-password').value.trim();
    if (loginEmail == '' || loginPassword == '') { //Check for blank input
      showLogInError('blank'); 
    } else {
      // console.log(loginEmail,loginPassword)
      try {
      const loginCredential = await signInWithEmailAndPassword(auth, loginEmail, loginPassword)
      // window.location.href = "../Home/home.html" //Redirect to homepage
      }
      catch(error) { // Username/password wrong
        // console.log(error);
        showLogInError('invalid')
      }
    }
  }


onAuthStateChanged(auth, (user) => {
  if (user) {
    fetch('http://localhost:5005/user', {
        method: 'POST',
        headers: { 'Content-Type':'application/json'},
        body: JSON.stringify({id: user.uid, email: user.email})
      });
    const uid = user.uid;
    console.log(uid)
    window.location.replace('../Frontend/Homepage/homepage.html')
  }
})
  
function showSignUpError(error) { //Error code function for signup
  console.log(error)
  var msgSpace = document.getElementById('signupError')
  if (error == 'auth/email-already-in-use'){
    msgSpace.innerText= 'Email already exists!'
  } else if (error== 'diff') {
    msgSpace.innerText = 'passwords are not the same'
  } else if (error == 'short') {
    msgSpace.innerText= 'Password has to be more than 6 characters!'
  } else if (error == 'blank') {
    msgSpace.innerText = 'Please fill in the blanks!'
  } else if (error == 'checkbox') {
    msgSpace.innerText = 'Please agree to our terms and services!'
  } else if (error == 'none') {
    msgSpace.innerText = ''
  }
    
}

function showLogInError(error) { //Error code function for signin
  var loginMsg = document.getElementById('signinMessage')
  loginMsg.setAttribute('style','color:red')
  if (error == 'blank') {
    loginMsg.innerText = 'Please fill in the blanks!'
  } else if (error == 'invalid') {
    loginMsg.innerText = 'Wrong email or password!'
  }
}

const switchers = [...document.querySelectorAll(".switcher")];


document.getElementsByClassName('btn-signup')[0].addEventListener("click", function(event){
  event.preventDefault()
});
document.getElementsByClassName('btn-signup')[0].addEventListener('click',signupEmailPassword);

document.getElementsByClassName('btn-login')[0].addEventListener("click", function(event){
  event.preventDefault()
});
document.getElementsByClassName('btn-login')[0].addEventListener('click',loginEmailPassword);

switchers.forEach((item) => {
  item.addEventListener("click", function () {
    switchers.forEach((item) =>
      item.parentElement.classList.remove("is-active")
    );
    this.parentElement.classList.add("is-active");
  });
});

