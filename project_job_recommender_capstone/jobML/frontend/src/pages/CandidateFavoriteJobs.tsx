import { FunctionComponent } from "react";
import { useLocation , useNavigate} from "react-router-dom";
import Navigation1 from "../components/Navigation1";
import Footer from "../components/Footer";
import styles from "./CandidateFavoriteJobs.module.css";
import { useEffect, useState } from "react";

const CandidateFavouriteJobs: FunctionComponent = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const [jobs, setJobs] = useState([]);


  useEffect(() => {
    const handleLikedJobs = async () => {
      console.log("Fetching liked jobs...");
    
      try {
        const response = await fetch('http://localhost:8000/Applicant/liked_jobs/', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
    
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
    
        const data = await response.json();
        setJobs(data.jobs);
    } catch (error) {
      console.error("There was an error with the search:", error);
    }
  };
    handleLikedJobs();
  }, [token]);
  const viewJob = async (jobId : number)=>{
    console.log("job clicked")
    try {
      const response = await fetch('http://localhost:8000/Applicant/get_jobpost/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ job_id: jobId}),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('job response:', data);
      navigate(`/job/${jobId}`,{state: {job : data.job_post, job_id : jobId}})
    } catch (error) {
      console.error('Error sending dislike:', error);
    }
  }

  // const viewJob = (jobId: number, job: any) => {
  //   // This will navigate to a new route and add the job ID to the URL path.
  //   // It will also pass the job data to the route so it can be displayed on the next page.

  //   navigate(`/job/${jobId}`, { state: { job } });
  // };


return (
  <div className={styles.candidateSearchPage}>
    <Navigation1 />
    {/* New heading for liked jobs */}
    <div className={styles.jobListingsContainer}>
    <h2 className={styles.searchResultsTitle}>Your liked jobs...</h2>
      {jobs.length > 0 ? (
        jobs.map((job: any) => (
          <div key={job.id} className={styles.jobCard}>
            <div>
              <h3 className={styles.jobTitle}>{job.title}</h3>
              <div className={styles.jobDetails}>
                <span className={styles.companyName}>{job.company_name}</span>
                <span className={styles.location}>{job.location}</span>
              </div>
            </div>
            <button
              className={styles.viewJobButton}
              onClick={() => viewJob(job.id)}
            >
              View Job
            </button>
          </div>
        ))
      ) : (
        <div className={styles.noResults}>No liked jobs to display.</div>
      )}
    </div>
    <div className={styles.footer}>
    <Footer />
    </div>
  </div>
);

};

export default CandidateFavouriteJobs;


