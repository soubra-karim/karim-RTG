import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import Navigation3 from "../components/Navigation3";
import styles from './EmployerCreateAccount.module.css';

const EmployerCreateAccount = () => {
  // State for form inputs
  const [fullName, setCompanyName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [phoneNumber, setPhoneNumber] = useState("");
  const navigate = useNavigate();

  // Handler for form submission
  const handleFormSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("username", username);
    formData.append("name", fullName);
    formData.append("email", email);
    formData.append("phone_number", phoneNumber);
    formData.append("password", password);
    formData.append("user_type", "Recruiter");

    try {
      const response = await fetch('http://localhost:8000/UserAuth/Signup/', {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        },
      });

      if (response.ok) {
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
          navigate("/employer-homepage");
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
      console.error("There was an error during the signup process", error);
    }
  };

  const handleApplicantClick = () => {
    navigate('/candidate-create-account');
  };

  const handleLogInClick = () => {
    navigate('/');
  };

  return (
    <>
    <Navigation3 />
    <div className={styles.employerCreateAccount}>
      <div className={styles.createAccountFrame}>
      <form className={styles.anotherFrame} onSubmit={handleFormSubmit}>
        <div className={styles.selectionFrameParent}>
          <div className={styles.selectionFrame}>
            <h3 className={styles.createAnEmployer}>Create an Employer account.</h3>
            <div className={styles.alreadyHaveAccountParent}>
              <div className={styles.alreadyHaveAccount}>Already have account?&nbsp; </div>
              <div className={styles.logIn}
              onClick={handleLogInClick}
              role="button"
              tabIndex={0}
              >Log In</div>
            </div>
          </div>
          <button className={styles.select}>
            <div className={styles.selected}
              onClick={handleApplicantClick} role="button" tabIndex={0}>Are you an Applicant?</div>
          </button>
        </div>
        <div className={styles.inputFieldEmail}>
          <div className={styles.inputFieldFrame}>
            <div className={styles.inputField}>
              <input className={styles.emailAddress} placeholder="Company Name" type="text" value={fullName} onChange={(e) => setCompanyName(e.target.value)} />
            </div>
            <div className={styles.inputField1}>
              <input className={styles.emailAddress1} placeholder="Username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
            </div>
          </div>
          <div className={styles.inputField2}>
            <input className={styles.emailAddress2} placeholder="Email address" type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
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
            <input className={styles.password} placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className={styles.inputField4}>
            <input className={styles.password1} placeholder="Confirm Password" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
          </div>
        </div>
        <button className={styles.button}>
          <div className={styles.primary}>Create account</div>
        </button>
      </form>
      </div>
    </div>
    </>
  );
};

export default EmployerCreateAccount;
