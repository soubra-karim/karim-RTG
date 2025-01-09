import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./CreateFrame.module.css";

const CreateFrame = () => {
  const [fullName, setFullName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");

  const navigate = useNavigate(); // useNavigate hook for navigation
  const handleFormSubmit = async (event) => {
    event.preventDefault();

    // Validation logic here
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    const formData = new FormData();
    formData.append("username", username);
    formData.append("name", fullName);
    formData.append("email", email);
    formData.append("phone_number", phoneNumber);
    formData.append("password", password);
    formData.append("user_type", "Applicant");

    try {
      const signupResponse = await fetch('http://localhost:8000/UserAuth/Signup/', {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        },
      });

      if (signupResponse.ok) {
        // Assume the response from signup does not automatically sign in the user
        // Therefore, proceed to sign in the user using the provided credentials
        const loginResponse = await fetch('http://localhost:8000/UserAuth/Login/', {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, password }),
        });

        if (loginResponse.ok) {
          const loginData = await loginResponse.json();
          localStorage.setItem('token', loginData.token);
          console.log('Auto sign-in successful', loginData);

          // Since this page is only for applicants, navigate directly to the resume upload page
          navigate("/resume-upload");
        } else {
          // Handle failed login
          console.error("Auto sign-in failed after account creation");
          // Optionally, provide user feedback here
        }
      } else {
        // Handle account creation error
        const errorData = await signupResponse.json();
        console.error("Signup failed:", errorData);
        // Optionally, provide user feedback here
      }
    } catch (error) {
      console.error("There was an error during the signup or login process", error);
      // Optionally, provide user feedback here
    }
  };


  const handleLogInClick = () => {
    navigate('/');
  };

  const handleEmployerClick = () => {
    navigate('/employer-create-account');
  };

  return (
    <div className={styles.container}>
    <form className={styles.createFrame} onSubmit={handleFormSubmit}>
      <div className={styles.frameParent}>
        <div className={styles.createAnApplicantAccountParent}>
          <h3 className={styles.createAnApplicant}>
            Create an Applicant account.
          </h3>
          <div className={styles.logInText}>
            <div className={styles.alreadyHaveAccount}>
              Already have account?&nbsp; 
            </div>
            <div className={styles.logIn}
            onClick={handleLogInClick}
            role="button"
            tabIndex={0}
            >Log In</div>
          </div>
        </div>
        <div className={styles.select}>
          <div className={styles.selected}
          onClick={handleEmployerClick}
          role="button"
          tabIndex={0}
          >Are you an employer?</div>
        </div>
      </div>
      <div className={styles.emailInputField}>
        <div className={styles.inputFieldEmailAddress}>
          <div className={styles.inputField}>
            <input
              className={styles.emailAddress}
              placeholder="Full Name"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
          </div>
          <div className={styles.inputField1}>
            <input
              className={styles.emailAddress1}
              placeholder="Username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
        </div>
        <div className={styles.inputField2}>
          <input
            className={styles.emailAddress2}
            placeholder="Email address"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className={styles.inputField5}>
          <input
            className={styles.phoneNumber}
            placeholder="Phone Number"
            type="phone_number"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
          />
        </div>
        <div className={styles.inputField3}>
          <input
            className={styles.password}
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {/* Password visibility toggle */}
        </div>
        <div className={styles.inputField4}>
          <input
            className={styles.password1}
            placeholder="Confirm Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          {/* Password visibility toggle */}
        </div>
      </div>
      <button className={styles.button} type="submit">
        <div className={styles.primary}>Create account</div>
        {/* Icon for the button */}
      </button>
    </form>
    </div>
  );
};

export default CreateFrame;
