import React, { useState, useEffect } from 'react';
import styles from './Stats.module.css'; // assuming you have this CSS file
import PieChart from '../components/PieChart';
import Graph from "../components/EmployerStatsGraph";

const Stats = () => {
  const [statsData, setStatsData] = useState({
    totalUsers: 0,
    totalRecruiters: 0,
    totalApplicants: 0,
    totalJobPostings: 0,
    dataScienceRoles: 0,
    frontendRoles: 0,
    backend_roles: 0,
    computer_engineering_roles:0,
    electrical_engineering_roles:0,
    python:0,
    java:0,
    css:0,
    html:0,
    c:0,
  });

  useEffect(() => {
    fetchStatsData();
  }, []); // Empty dependency array ensures this effect runs only once on component mount

  const fetchStatsData = async () => {
    try {
      const response = await fetch('http://localhost:8000/UserAuth/stats_view'); // Replace '/api/stats_view' with your actual backend API endpoint
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      const data = await response.json();
      setStatsData({
        totalUsers: data.total_users,
        totalRecruiters: data.total_recruiters,
        totalApplicants: data.total_applicants,
        totalJobPostings: data.total_job_postings,
        dataScienceRoles: data.data_science_roles,
        frontendRoles: data.frontend_roles,
        backend_roles:  data.backend_roles,
        computer_engineering_roles:  data.computer_engineering_roles,
        electrical_engineering_roles:  data.electrical_engineering_roles,
        python:data.python,
        java:data.java,
        css:data.css,
        html:data.html,
        c:data.c,
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className={styles.statsContainer}>
      <div className={styles.statsGroup}>
        <div className={styles.statsBox} style={{ backgroundColor: '#ffffff' }}>
          <img src="/briefcase2.svg" alt="Calendar Icon" className={styles.image} />
          <div className={styles.statsBoxVertical}>
            <div className={styles.statValue}>{statsData.totalApplicants}</div>
            <div className={styles.statLabel}>Total Applicants</div>
          </div>
        </div>
        <div className={styles.statsBox} style={{ backgroundColor: '#ffffff' }}>
          <img src="/user.svg" alt="Calendar Icon" className={styles.image} />
          <div className={styles.statsBoxVertical}>
            <div className={styles.statValue}>{statsData.totalRecruiters}</div>
            <div className={styles.statLabel}>Total Recruiters</div>
          </div>
        </div>
        <div className={styles.statsBox} style={{ backgroundColor: '#ffffff' }}>
          <img src="/users.svg" alt="Calendar Icon" className={styles.image} />
          <div className={styles.statsBoxVertical}>
            <div className={styles.statValue}>{statsData.totalUsers}</div>
            <div className={styles.statLabel}>Total Users</div>
          </div>
        </div>
        <div className={styles.statsBox} style={{ backgroundColor: '#ffffff' }}>
          <img src="/stack.svg" alt="Calendar Icon" className={styles.image} />
          <div className={styles.statsBoxVertical}>
            <div className={styles.statValue}>{statsData.totalJobPostings}</div>
            <div className={styles.statLabel}>Total Job Postings</div>
          </div>
        </div>
      </div>
      <div className={styles.statsGroup2}>
          <div className={styles.statsBox2} style={{ backgroundColor: '#ffc13c38' }}>
            <Graph statsData={statsData} />
          </div>
          <div className={styles.statsBox1} style={{ backgroundColor: '#ff3c9d38' }}>
            <PieChart statsData={statsData} />
        </div>
      </div>
    </div>
  );
};

export default Stats;