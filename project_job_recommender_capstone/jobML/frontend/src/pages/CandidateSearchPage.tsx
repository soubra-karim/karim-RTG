import { FunctionComponent } from "react";
import { useLocation , useNavigate} from "react-router-dom";
import Navigation1 from "../components/Navigation1";
import Footer from "../components/Footer";
import styles from "./CandidateSearchPage.module.css";

const CandidateSearchPage: FunctionComponent = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const jobs = location.state?.jobs || [];
  const searchQuery = location.state?.searchQuery;
  const token = localStorage.getItem('token');


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
  return (
    <div className={styles.candidateSearchPage}>
      <Navigation1 />
      <div className={styles.jobListingsContainer}>
      <h1 className={styles.searchResultsTitle}>Search results for "{searchQuery}"</h1>
        {jobs.map((job: any) => (
          <div key={job.id} className={styles.jobCard}>
            <div>
              <h2 className={styles.jobTitle}>{job.title}</h2>
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
        ))}
      </div>
      <Footer />
    </div>
  );
};

export default CandidateSearchPage;


