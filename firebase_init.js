// firebase_init.js
// Paste your actual config values from Firebase console

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.0.0/firebase-app.js";
import { getDatabase, ref, push, onValue } from "https://www.gstatic.com/firebasejs/10.0.0/firebase-database.js";

const firebaseConfig = {
  apiKey: "AIzaSyCczLl8sXUeQAMtFA2r_jhxf7dcPBYujjE",
  authDomain: "scamshield-1af29.firebaseapp.com",
  databaseURL: "https://scamshield-1af29-default-rtdb.asia-southeast1.firebasedatabase.app/",
  projectId: "scamshield-1af29",
  storageBucket: "scamshield-1af29.firebaseapp.com",
  messagingSenderId: "scamshield-1af29.firebaseapp.com",
  appId: "1:184790588709:web:5a978d21ce616e3ca30ecc"
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

export { database, ref, push, onValue };