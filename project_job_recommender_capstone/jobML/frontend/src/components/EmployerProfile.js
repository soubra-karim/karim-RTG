import { FunctionComponent, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./EmployerProfile.module.css";

const EmployerProfile = () => {
  const [name, setName] = useState('');
  const [username, setUsername] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [password, setPassword] = useState('');
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [emailUpdateMessage, setEmailUpdateMessage] = useState('');
  const [passwordUpdateMessage, setPasswordUpdateMessage] = useState('');
  const token = localStorage.getItem('token');

  const handleEmailClick = async (event) => {
    event.preventDefault();
    const payload = { new_email: newEmail, password: password };

    try {
      const response = await fetch('http://localhost:8000/UserAuth/update-email/', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,

          'Content-Type': 'application/json',
      
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('Email update success:', data);
        setEmailUpdateMessage('Email has been updated.'); // Set success message
        setTimeout(() => setEmailUpdateMessage(''), 5000); // Optional: Clear message after 5 seconds
      } else {
        console.error('Email update error:', data.result);
      }
    } catch (error) {
      console.error('Email update failed:', error);
    }
  };

  const handlePasswordClick = async (event) => {
    event.preventDefault();
    const payload = { password: oldPassword, new_password: newPassword };

    if (newPassword !== confirmNewPassword) {
      console.error('New passwords do not match.');
      setPasswordUpdateMessage('New passwords do not match.');
      setTimeout(() => setEmailUpdateMessage(''), 5000); // Optional: Clear message after 5 seconds
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/UserAuth/update-password/', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,

          'Content-Type': 'application/json',
      
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('Password update success:', data);
        setPasswordUpdateMessage('Password has been changed.'); // Set success message
        setTimeout(() => setPasswordUpdateMessage(''), 5000); // Optional: Clear message after 5 seconds
      } else {
        console.error('Password update error:', data.result);
      }
    } catch (error) {
      console.error('Password update failed:', error);
    }
  };
  
  return (
  <form className={styles.candidateSettings}>
    {/* Update Email Section */}
    <h2 className={styles.settings}>Update Email</h2>
    <div className={styles.inputFieldParent}>
      <div className={styles.inputField}>
        <input
          placeholder="New Email"
          type="email"
          value={newEmail}
          onChange={(e) => setNewEmail(e.target.value)}
        />
      </div>
      <div className={styles.inputField}>
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
    </div>
    {emailUpdateMessage && <div className={styles.updateMessage}>{emailUpdateMessage}</div>}
    <button onClick={handleEmailClick} className={styles.button}>
      Save Changes
    </button>

    {/* Change Password Section */}
    <h2 className={styles.settings}>Change Your Password</h2>
    <div className={styles.inputFieldParent}>
      <div className={styles.inputField}>
        <input
          placeholder="Old Password"
          type="password"
          value={oldPassword}
          onChange={(e) => setOldPassword(e.target.value)}
        />
      </div>
      <div className={styles.inputField}>
        <input
          placeholder="New Password"
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
      </div>
      <div className={styles.inputField}>
        <input
          placeholder="Confirm New Password"
          type="password"
          value={confirmNewPassword}
          onChange={(e) => setConfirmNewPassword(e.target.value)}
        />
      </div>
    </div>
    {passwordUpdateMessage && <div className={styles.updateMessage}>{passwordUpdateMessage}</div>}
    <button onClick={handlePasswordClick} className={styles.button}>
      Save Changes
    </button>


  </form>
);

};

export default EmployerProfile;