
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import {getAuth, createUserWithEmailAndPassword, onAuthStateChanged} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

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
      // const reference = ref(db, 'users/' + user.uid)
      // const testRef = ref(db,'testCompletion/' + user.uid)
      // user.displayName = signupName  
      console.log(user)
      // set(reference, { //Update realtime database with user info
      //   username: signupName,
      //   email:signupEmail,
      //   image:'avatar1.jpg' //default avatar
      //   })
      // update(testRef, {totalScore:0}) //default score = 0

      // document.getElementById('signinMessage').innerText="You have successfully signed up!" 
      // document.getElementById('signinMessage').setAttribute("style","color:green")
      // clearFields()
      // main.classList.toggle("sign-up-mode") //Move screen back to login



    }
    catch(error) {
      console.log(error);
      showSignUpError(error.code); //Show error code
    }
  }}

// onAuthStateChanged(auth, (user) => {
//   if (user) {
//     const uid = user.uid;
//     console.log(uid)
//     window.location.replace('../Homepage/homepage.html')
//   }
// })
  
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

const switchers = [...document.querySelectorAll(".switcher")];
document.getElementsByClassName('btn-signup')[0].addEventListener("click", function(event){
  event.preventDefault()
});
document.getElementsByClassName('btn-signup')[0].addEventListener('click',signupEmailPassword);



switchers.forEach((item) => {
  item.addEventListener("click", function () {
    switchers.forEach((item) =>
      item.parentElement.classList.remove("is-active")
    );
    this.parentElement.classList.add("is-active");
  });
});

