import React, { useState, useEffect } from "react";
import Navigation3 from "../components/Navigation3";
import styles from "./ResumeUpload.module.css";
import { useNavigate } from "react-router-dom";

const ResumeUpload = () => {
  const [cvFile, setCvFile] = useState(null);
  const [fileUploaded, setFileUploaded] = useState(false);
  // Updating state hooks for individual text boxes
  const [school1, setSchool1] = useState("");
  const [degree1, setDegree1] = useState("");
  const [startDate1, setStartDate1] = useState("");
  const [endDate1, setEndDate1] = useState("");
  const [school2, setSchool2] = useState("");
  const [degree2, setDegree2] = useState("");
  const [startDate2, setStartDate2] = useState("");
  const [endDate2, setEndDate2] = useState("");
  const [companyName1, setCompanyName1] = useState("");
  const [jobTitle1, setJobTitle1] = useState("");
  const [startWorkDate1, setStartWorkDate1] = useState("");
  const [endWorkDate1, setEndWorkDate1] = useState("");
  const [companyName2, setCompanyName2] = useState("");
  const [jobTitle2, setJobTitle2] = useState("");
  const [startWorkDate2, setStartWorkDate2] = useState("");
  const [endWorkDate2, setEndWorkDate2] = useState("");
  const [skills, setSkills] = useState("");
  const [address, setAddress] = useState("");
  const [desc, setDesc] = useState("");
  const [desc2, setDesc2] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
    }
  }, [navigate]);

  // Handle file change
  const handleCvFileChange = (event) => {
    setCvFile(event.target.files[0]);
  };

  const handleResumeUpload = async (event) => {
    event.preventDefault();
    if (!cvFile) {
      alert('Please select a file first!');
      return;
    }
    setIsLoading(true);
    // Create a FormData object to build the multipart/form-data request
    const formData = new FormData();
    formData.append('file', cvFile);
  
    // Send the request
    try {
      const response = await fetch('http://localhost:8000/Applicant/upload-resume/', {
        method: 'POST',
        body: formData,
        // Headers may be configured as needed by your backend
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const result = await response.json();
      console.log('File uploaded successfully', result);
      console.log(result)
            // Assuming result contains the structured data as described
      // Corrected for case sensitivity and key names
      if (result['educations'] && result['educations'].length > 0) {
        // Update for first education entry
        setSchool1(result['educations'][0]['school_name']);
        setDegree1(result['educations'][0]['degree']);
        setStartDate1(result['educations'][0]['start_date']);
        setEndDate1(result['educations'][0]['end_date']);

      }

      if (result['educations'] && result['educations'].length > 1) {
        // Update for first education entry
        setSchool2(result['educations'][1]['school_name']);
        setDegree2(result['educations'][1]['degree']);
        setStartDate2(result['educations'][1]['start_date']);
        setEndDate2(result['educations'][1]['end_date']);
      }

      if (result['work_experiences'] && result['work_experiences'].length > 0) {
        // Update for first work experience entry
        setCompanyName1(result['work_experiences'][0]['company_name']);
        setJobTitle1(result['work_experiences'][0]['job_title']);
        setDesc(result['work_experiences'][0]['job_description']);
        setStartWorkDate1(result['work_experiences'][0]['start_date']);
        setEndWorkDate1(result['work_experiences'][0]['end_date']);
      }

      if (result['work_experiences'] && result['work_experiences'].length > 1) {
        // Update for first work experience entry
        setCompanyName2(result['work_experiences'][1]['company_name']);
        setJobTitle2(result['work_experiences'][1]['job_title']);
        setDesc2(result['work_experiences'][0]['job_description']);
        setStartWorkDate2(result['work_experiences'][1]['start_date']);
        setEndWorkDate2(result['work_experiences'][1]['end_date']);
      }

      // Correct handling for skills (assuming you modify your JSON or parse the string)
      setSkills(result['resume_skills']);

      setAddress(result['Address']);
      setFileUploaded(true);
      setIsLoading(false);
        } catch (error) {
      console.error('There was an error uploading the file', error);
    }
  };
  

  const handleManualUpload = async (event) => {
    setFileUploaded(true);

    }
  



  const handleSubmit = async (event) => {
    event.preventDefault();
    // Construct the payload with the updated structure
    const skillsArray = skills.split(',')
    .map(skill => skill.trim()) // Trim whitespace from each skill
    .filter(skill => skill.length > 0) // Ensure no empty strings are included
    .map(skill_name => ({skill_name}));

    const payload = {
      educations: [
        { school_name: school1, degree: degree1, start_date: startDate1, end_date: endDate1 },
        { school_name: school2, degree: degree2, start_date: startDate2, end_date: endDate2 }
      ],
      work_experiences: [
        { company_name: companyName1, job_title: jobTitle1, job_description: desc, start_date: startWorkDate1, end_date: endWorkDate1 },
        { company_name: companyName2, job_title: jobTitle2, job_description: desc2, start_date: startWorkDate2, end_date: endWorkDate2 }
      ],
      resume_skills: skillsArray,
      //address,
    };
    console.log('payload', payload)
    // Retrieve the token from localStorage
    const token = localStorage.getItem('token'); // Assume the token is stored with the key 'token'
  
    try {
      console.log('Token:', token)
      // Send the POST request with the payload
      const response = await fetch('http://localhost:8000/Applicant/create-resume/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,

          'Content-Type': 'application/json',
      
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const result = await response.json();
      console.log('Resume data submitted successfully', result);
      // Handle successful submission, e.g., redirect or display a success message
      navigate('/candidate-homepage/');
    } catch (error) {
      console.error('There was an error submitting the resume data', error);
      // Handle the error, e.g., display an error message to the user
    }
  };

  const LoadingIcon = () => (
    <div className={styles.loadingContainer}>
      <div className={styles.categoryIconGroup}>
        <div className={styles.sitelogo}>
          <div className={styles.digitalMarketing} />
          <div className={styles.digitalMarketing1} />
          <div className={styles.digitalMarketing2} />
          <div className={styles.sitelogo1} />
        </div>
        <h3 className={styles.jobsync}>JobSync</h3>
    </div>
  </div>
  );



  return (
    <>
      <Navigation3 />
      <div className={styles.container}>
        <h2 className={styles.uploadTitle}>Please upload a PDF of your resume</h2>
        <form>
  <div className={styles.fileUploadContainer}>
    <input
      type="file"
      onChange={handleCvFileChange}
      className={styles.fileInput}
      accept=".pdf"
    />
    {/* Prevent the default form submission behavior */}
    <button type="button" onClick={handleResumeUpload} className={styles.submitButton}>
      Upload
    </button>
    <button type="button" onClick={handleManualUpload} className={styles.submitButton}>
      Manually Upload
    </button>
  </div>
</form>

        {isLoading ? (
        <div className={styles.loadingContainer}>
          <LoadingIcon />
        </div>
      ) : fileUploaded && (
          <>
          <h2 className={styles.formTitle}>Please verify or edit your resume below</h2>
          <form onSubmit={handleSubmit} className={styles.resumeForm}>
            {/* Education 1 inputs */}
            <div className={styles.inputGroup}>
              <h3 className={styles.inputTitle}>Education 1</h3>
              <input type="text" placeholder="School" value={school1} onChange={e => setSchool1(e.target.value)} />
              <input type="text" placeholder="Degree" value={degree1} onChange={e => setDegree1(e.target.value)} />
              <input type="date" placeholder="Start Date" value={startDate1} onChange={e => setStartDate1(e.target.value)} />
              <input type="date" placeholder="End Date" value={endDate1} onChange={e => setEndDate1(e.target.value)} />
            </div>
            {/* Education 2 inputs */}
            <div className={styles.inputGroup}>
              <h3 className={styles.inputTitle}>Education 2</h3>
              <input type="text" placeholder="School" value={school2} onChange={e => setSchool2(e.target.value)} />
              <input type="text" placeholder="Degree" value={degree2} onChange={e => setDegree2(e.target.value)} />
              <input type="date" placeholder="Start Date" value={startDate2} onChange={e => setStartDate2(e.target.value)} />
              <input type="date" placeholder="End Date" value={endDate2} onChange={e => setEndDate2(e.target.value)} />
            </div>
            {/* Work Experience 1 inputs */}
            <div className={styles.inputGroup}>
              <h3 className={styles.inputTitle}>Work Experience 1</h3>
              <input type="text" placeholder="Company Name" value={companyName1} onChange={e => setCompanyName1(e.target.value)} />
              <input type="text" placeholder="Job Title" value={jobTitle1} onChange={e => setJobTitle1(e.target.value)} />
              <input type="text" placeholder="Job Description" value={desc} onChange={e => setDesc(e.target.value)} />
              <input type="date" placeholder="Start Date" value={startWorkDate1} onChange={e => setStartWorkDate1(e.target.value)} />
              <input type="date" placeholder="End Date" value={endWorkDate1} onChange={e => setEndWorkDate1(e.target.value)} />
            </div>
            {/* Work Experience 2 inputs */}
            <div className={styles.inputGroup}>
              <h3 className={styles.inputTitle}>Work Experience 2</h3>
              <input type="text" placeholder="Company Name" value={companyName2} onChange={e => setCompanyName2(e.target.value)} />
              <input type="text" placeholder="Job Title" value={jobTitle2} onChange={e => setJobTitle2(e.target.value)} />
              <input type="text" placeholder="Job Description" value={desc2} onChange={e => setDesc2(e.target.value)} />
              <input type="date" placeholder="Start Date" value={startWorkDate2} onChange={e => setStartWorkDate2(e.target.value)} />
              <input type="date" placeholder="End Date" value={endWorkDate2} onChange={e => setEndWorkDate2(e.target.value)} />
            </div>
            {/* Skills input */}
            <div className={styles.inputGroup}>
              <h3 className={styles.inputTitle}>Skills</h3>
              <input type="text" placeholder="Skills" value={skills} onChange={e => setSkills(e.target.value)} />
            </div>
            {/* Address input */}
            <div className={styles.inputGroup}>
              <h3 className={styles.inputTitle}>Address</h3>
              <input type="text" placeholder="Address" value={address} onChange={e => setAddress(e.target.value)} />
            </div>
            <button type="submit" className={styles.submitFinalButton}>Submit</button>
          </form>
          </>
        )}
      </div>
    </>
  );
};

export default ResumeUpload;
