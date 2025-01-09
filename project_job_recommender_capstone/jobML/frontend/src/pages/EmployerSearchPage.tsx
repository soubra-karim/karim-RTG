import { FunctionComponent } from "react";
import { useLocation , useNavigate} from "react-router-dom";
import Navigation2 from "../components/Navigation2";
import Footer from "../components/Footer";
import styles from "./CandidateSearchPage.module.css";
//  key={applicant.name}
const CandidateSearchPage: FunctionComponent = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const applicants = location.state?.applicants || [];
  const searchQuery = location.state?.searchQuery;

  const viewapplicant = (applicant: any) => {
    // This will navigate to a new route and add the job ID to the URL path.
    // It will also pass the job data to the route so it can be displayed on the next page.
    navigate(`/candidatepage/${applicant.id}`, { state: { applicant } });
  };

  return (
    <div className={styles.candidateSearchPage}>
      <Navigation2 />
      <div className={styles.jobListingsContainer}>
      <h1 className={styles.searchResultsTitle}>Search results for "{searchQuery}"</h1>
        {applicants.map((applicant: any) => (
          <div className={styles.jobCard}>
            <div>
              <h2 className={styles.jobTitle}>{applicant.name}</h2>
              <div className={styles.jobDetails}>
                <span className={styles.companyName}>{applicant.phone_number}</span>
                <span className={styles.location}>{applicant.email}</span>
              </div>
            </div>
            <button
              className={styles.viewJobButton}
              onClick={() => viewapplicant(applicant)}
            >
              View Candidate
            </button>
          </div>
        ))}
      </div>
      <Footer />
    </div>
  );
};

export default CandidateSearchPage;


