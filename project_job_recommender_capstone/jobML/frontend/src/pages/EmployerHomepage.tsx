import React, { useEffect, useState } from 'react';
import SiteLogo2 from '../components/SiteLogo2';
import Footer from '../components/Footer';
import Navigation2 from '../components/Navigation2';
import { useNavigate } from 'react-router-dom';
import styles from './EmployerHomepage.module.css';
import { FunctionComponent } from "react";

const EmployerHomepage: FunctionComponent = () => {
  const [jobPostings, setJobPostings] = useState([]);
  const token = localStorage.getItem('token');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchJobPostings = async () => {
      try {
        const response = await fetch('http://localhost:8000/Recruiter/jobPostingListView/', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setJobPostings(data.jobs); // Adjust this if the structure of your data is different
      } catch (error) {
        console.error('Error fetching job postings:', error);
        setJobPostings([]); // Set jobPostings to an empty array in case of error
      }
    };

    fetchJobPostings();
  }, [token]);

  const viewCandidates = (jobId: number , job: any) => {
    // You can pass additional state to the route as needed
    navigate(`/recommended-candidates/${jobId}`, { state: { job } });
  };
  const editJob = (jobId: number , job: any) => {
    // You can pass additional state to the route as needed
    navigate(`/edit-job/${jobId}`, { state: { job } });
  };

  return (
    <div className={styles.employerHomepage}>
      <Navigation2 />
      <SiteLogo2 findAJobThatSuitsYourInte="Find a candidate that suits your needs." />
      <div className={styles.jobListingsContainer}>
        <h2 className={styles.yourJobPostingsHeading}>Your Job Postings...&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h2>
        {Array.isArray(jobPostings) && jobPostings.length > 0 ? (
          jobPostings.map((job: any) => (
            <div className={styles.jobCard} key={job.id}>
              <div>
                <h2 className={styles.jobTitle}>{job.title}</h2>
                <div className={styles.jobDetails}>
                  <span className={styles.companyName}>{job.company_name}</span>
                  <span className={styles.location}>{job.location}</span>
                </div>
              </div>
              <div className={styles.buttonsContainer}> 
              <button
              
            className={styles.editJobButton}
            onClick={() => editJob(job.id, job)} // Use the viewCandidates function here
          >
            Edit Job
          </button>
              <button
            className={styles.viewJobButton}
            onClick={() => viewCandidates(job.id, job)} // Use the viewCandidates function here
          >
            View Candidates
          </button>
            </div>
            </div>
          ))
        ) : (
          <div className={styles.noJobsMessageContainer}>
            <h2 className={styles.noJobsMessage}>You have not created any jobs yet.</h2>
          </div>
        )}
        {/* This button will always be rendered below the job cards */}
        <button className={styles.createJobButton2} onClick={() => navigate('/create-job')}>
          Create a Job
        </button>
      </div>
      <Footer />
    </div>
  );
  
  
};

export default EmployerHomepage;
