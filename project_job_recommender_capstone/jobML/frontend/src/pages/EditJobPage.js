import React, { useState, useEffect } from 'react';
import Footer from '../components/Footer';
import Navigation2 from '../components/Navigation2';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from './EditJobPage.module.css';

const EditJobPage = () => {

  const [formData, setFormData] = useState({
    title: '',
    company_name: '',
    location: '',
    job_description: '',
    posted_date: '',
    application_deadline: '',
    skills: '',
    benefits: '',
    employment_type: '',
  });

  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Check if there is state in the location object and if it has a job property
    if (location.state && location.state.job) {
      const job = location.state.job;
      console.log(job)
      // Update the form data with the job data
      setFormData({
        id: job.id, // Make sure to set the id as well
        title: job.title || '',
        company_name: job.company_name || '',
        location: job.location || '',
        job_description: job.job_description || '',
        posted_date: job.posted_date || '',
        application_deadline: job.application_deadline || '',
        skills: Array.isArray(job.skills) ? job.skills.join(', ') : '', // Join the array back to string if needed
        benefits: job.benefits || '',
        employment_type: job.employment_type || '',
      });
    }
  }, [location.state]);



  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };



  const handleEditJob = async (e) => {
    e.preventDefault();

    // Convert job_skills from string to array of trimmed strings
    const formDataWithSkillsArray = {
      ...formData,
      skills: formData.skills.split(',').map(skill => skill.trim()),
    };
    const job_id = formData.id
    console.log('job_id',job_id)
    console.log(formData)
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/UserAuth/edit-job/', {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      
      body: JSON.stringify({job_id: job_id, formDataWithSkillsArray}),
    });

    if (response.ok) {
      // If you expect a response, you can await it here
      const data = await response.json();
      // Replace '/path-to-redirect-after-creation' with your actual path
      navigate('/employer-homepage');
    } else {
      // Log or handle errors here
      console.error('Failed to create job posting');
    }
  };
  
  return (
    <>
      <Navigation2 />
      <div className={styles.createJobFormContainer}>
        <h2>Edit your job posting</h2>
        <div className={styles.formRow}>
          <div className={styles.formColumn}>
            {/* Left column fields */}
            <div className={styles.formGroup}>
              <label>Title</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                placeholder="Enter job title"
              />
            </div>
            <div className={styles.formGroup}>
              <label>Company Name</label>
              <input
                type="text"
                name="company_name"
                value={formData.company_name}
                onChange={handleInputChange}
                placeholder="Enter company name"
              />
            </div>
            <div className={styles.formGroup}>
              <label>Location</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                placeholder="Enter job location"
              />
            </div>
            <div className={styles.formGroup}>
              <label>Posted Date</label>
              <input
                type="date"
                name="posted_date"
                value={formData.posted_date}
                onChange={handleInputChange}
              />
            </div>
            <div className={styles.formGroup}>
              <label>Application Deadline</label>
              <input
                type="date"
                name="application_deadline"
                value={formData.application_deadline}
                onChange={handleInputChange}
              />
            </div>
            <div className={styles.formGroup}>
              <label>Benefits</label>
              <input
                type="text"
                name="benefits"
                value={formData.benefits}
                onChange={handleInputChange}
                placeholder="Enter benefits"
              />
            </div>
            <div className={styles.formGroup}>
              <label>Employment Type</label>
              <input
                type="text"
                name="employment_type"
                value={formData.employment_type}
                onChange={handleInputChange}
                placeholder="Enter employment type"
              />
            </div>
          </div>
          <div className={styles.formColumn}>
            {/* Right column fields */}
            <div className={styles.formGroup}>
              <label>Job Description</label>
              <textarea
                name="job_description"
                value={formData.job_description}
                onChange={handleInputChange}
                placeholder="Enter job description"
              />
            </div>
            <div className={styles.formSkill}>
              <label>Job Skills</label>
              <textarea
                name="skills"
                value={formData.skills}
                onChange={handleInputChange}
                placeholder="Enter required job skills"
              />
            </div>
          </div>
        </div>
        <button className={styles.formButton} onClick={handleEditJob}>Update Job</button>
      </div>
      <Footer />
    </>
  );
};


export default EditJobPage;