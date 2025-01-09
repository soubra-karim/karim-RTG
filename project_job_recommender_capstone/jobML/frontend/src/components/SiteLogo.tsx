import { FunctionComponent, useMemo, type CSSProperties } from "react";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; 
import styles from "./SiteLogo.module.css";

export type SiteLogoType = {
  findAJobThatSuitsYourInte?: string;
  jobTittleKeywordPlacehold?: string;

  /** Style props */
  propMinWidth?: CSSProperties["minWidth"];
  propWidth?: CSSProperties["width"];
};

const SiteLogo: FunctionComponent<SiteLogoType> = ({
  findAJobThatSuitsYourInte,
  jobTittleKeywordPlacehold,
  propMinWidth,
  propWidth,
}) => {
  const inputFieldStyle: CSSProperties = useMemo(() => {
    return {
      minWidth: propMinWidth,
    };
  }, [propMinWidth]);

  const jobTittleKeywordStyle: CSSProperties = useMemo(() => {
    return {
      width: propWidth,
    };
  }, [propWidth]);

  const navigate = useNavigate(); // useNavigate hook for navigation
  const [searchQuery, setSearchQuery] = useState(""); // State to keep track of the search query

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
    <section className={styles.siteLogo}>
      <div className={styles.headerSection}>
        <div className={styles.container}>
          <h1 className={styles.findAJob}>{findAJobThatSuitsYourInte}</h1>
          <div className={styles.search}>
            <div className={styles.searchChild} />
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
            <button className={styles.findJobButton} onClick={handleFindJob}>Find Job</button> {/* Added find job button */}
          </div>
        </div>
      </div>
      <img
        className={styles.illustrationIcon}
        loading="eager"
        alt=""
        src="/illustration.svg"
      />
    </section>
  );
};

export default SiteLogo;
