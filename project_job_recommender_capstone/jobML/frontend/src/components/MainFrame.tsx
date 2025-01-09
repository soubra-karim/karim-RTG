import { FunctionComponent } from "react";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./MainFrame.module.css";

const MainFrame: React.FunctionComponent = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  const handleSignIn = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
  
    try {
      const response = await fetch('http://localhost:8000/UserAuth/Login/', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
  
      if (response.ok) {
        try {
          const data = await response.json();
          console.log("Sign in successful", data);
          
          // Save the token in local storage or state management
          localStorage.setItem('token', data.token);
          console.log('User type:', data.user_type);
          // Implement your logic upon successful sign in
          // Navigate to the dashboard based on user type
          if (data.user_type === 'Applicant') {
            navigate("/candidate-homepage");
          } else if (data.user_type === 'Recruiter') {
            navigate("/employer-homepage");
          } else {
            console.error("Unknown user type");
            // Handle unknown user type, possibly navigate to a default or error page
          }
        }  catch (jsonParseError) {
          console.error("Error parsing JSON response", jsonParseError);
          // Handle JSON parsing error (e.g., show a notification to the user)
        }
        
      } else {
        try {
          const errorData = await response.json();
          console.error("Sign in failed", errorData);
          alert(errorData.error); // or a more integrated UI error handling
        } catch (jsonParseError) {
          console.error("Error parsing JSON error response", jsonParseError);
          // The response was not JSON, handle accordingly
          alert("An unexpected error occurred. Please try again.");
        }
      }
    } catch (error) {
      console.error("There was an error signing in", error);
      // Handle the error in the UI
    }
  };

  const handleCreateAccountClick = () => {
    navigate('/candidate-create-account');
  };

  return (
    <div className={styles.container}>
    <form className={styles.mainFrame} onSubmit={handleSignIn}>
      <div className={styles.signInFrame}>
        <h1 className={styles.signIn}>Sign in</h1>
        <div className={styles.textNode}>
          <div className={styles.dontHaveAccount}>Don’t have an account?&nbsp;</div>
          <div 
            className={styles.createAccount}
            onClick={handleCreateAccountClick}
            role="button"
            tabIndex={0}
          >
            Create an Account
          </div>
        </div>
      </div>
      <div className={styles.inputFieldWrapper}>
        <div className={styles.inputField}>
          <input
            className={styles.emailAddress}
            placeholder="Email address"
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className={styles.inputField1}>
          <input
            className={styles.password}
            placeholder="Password"
            type="password" // Use type="password" for password inputs
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
      </div>

      <button className={styles.button} type="submit">
        <div className={styles.primary}>Sign in</div>
        <img
          className={styles.fiarrowRightIcon}
          alt=""
          src="/fiarrowright.svg"
        />
      </button>
    </form>
    </div>
  );
};

export default MainFrame;
