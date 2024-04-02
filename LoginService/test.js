// FILE IS FOR REFERENCE IN PERFORMING USER RETRIEVAL FROM "firebase.py"
// NOT INTENDED FOR FUNCTIONAL USE


import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import {getAuth, createUserWithEmailAndPassword, onAuthStateChanged, signInWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

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
        update_body(uid,"test")
    }
  })
//   async function get_email(uid) {
//     try {
//         const response = await fetch('http://localhost:5001/email', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ id:uid })
//         });
//         if (response.ok) {
//             var response_data = await response.json()
//             response_data = response_data['data']
//             return(response_data)
//         }
//     } catch (error) {
//         console.log(error)
//         alert('error')
//     }
// }

async function get_body(uid) {
    try {
        const response = await fetch('http://localhost:5001/body', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id:uid })
        });
        if (response.ok) {
            var response_data = await response.json()
            console.log(response_data)
            response_data = response_data['data']
            return(response_data)
        }
    } catch (error) {
        console.log(error)
        alert('error')
    }
}

// async function update_body(uid,body) {
//     try {
//         const response = await fetch('http://localhost:5001/updatebody', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ id:uid, body: body})
//         });
//         if (response.ok) {
//             var response_data = await response.json()
//             console.log(response_data)
//             response_data = response_data['data']
//             return(response_data)
//         }
//     } catch (error) {
//         console.log(error)
//         alert('error')
//     }
// }


async function create_user(uid,email) {
    try {
        const response = await fetch('http://localhost:5001/user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id:uid, email:email })
        });
        if (response.ok) {
            var response_data = await response.json()
            console.log(response_data)
            response_data = response_data['data']
            return(response_data)
        }
    } catch (error) {
        console.log(error)
        alert('error')
    }
}