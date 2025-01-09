import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate hook for programmatic navigation
import styles from "./Navigation1.module.css";

const Navigation1 = () => {
  const navigate = useNavigate(); // useNavigate hook for navigation
  const [searchQuery, setSearchQuery] = useState(""); // State to keep track of the search query

  const handleLogout = () => {
    console.log("Logging out...");
    localStorage.removeItem('token');
    navigate('/');
  };

  const handleFindJob = async () => {
    console.log("Finding job...");
    console.log("Search query:", searchQuery); // Print the search query
  
    try {
      const response = await fetch('http://localhost:8000/Applicant/search_jobs/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // 'X-CSRFToken': csrfToken // Include this if you're not exempting CSRF verification
        },
        body: JSON.stringify({ q: searchQuery }),
        credentials: 'include' // Required if you're sending CSRF token from a cookie
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      navigate('/candidate-search-page', { state: { searchQuery, jobs: data.jobs } });
    } catch (error) {
      console.error("There was an error with the search:", error);
    }
  };
  

  return (
    <div className={styles.navigation1}>
      <div className={styles.categoryIconGroup}>
          <div className={styles.sitelogo}>
            <div className={styles.digitalMarketing} />
            <div className={styles.digitalMarketing1} />
            <div className={styles.digitalMarketing2} />
            <div className={styles.sitelogo1} />
          </div>
          <h3 className={styles.jobsync}>JobSync</h3>
      </div>
      <div className={styles.videoAnimation}>
        <div className={styles.search}>
          <img className={styles.fisearchIcon} alt="" src="/fisearch.svg" />
          <input
            className={styles.jobTitleKeyword}
            placeholder="Job title, keyword, company"
            type="text"
            value={searchQuery} // Controlled input
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleFindJob();
              }
            }}
          />
          <button className={styles.findJobButton} onClick={handleFindJob}>Search</button> {/* Added find job button */}
        </div>
      </div>
      <div className={styles.science}>
        <button className={styles.navButton} onClick={() => navigate('/candidate-homepage')}>Home</button>
        <button className={styles.navButton} onClick={() => navigate('/candidate-liked-jobs')}>Liked Jobs</button>
        <button className={styles.navButton} onClick={() => navigate('/candidate-stats')}>Stats</button>
        <button className={styles.navButton} onClick={() => navigate('/candidate-my-profile')}>My Profile</button>
        <button className={styles.navButton} onClick={handleLogout}>Log-out</button>
      </div>
    </div>

);
};

export default Navigation1;
