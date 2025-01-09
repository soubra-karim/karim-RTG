import { useEffect, useState } from "react";
import Navigation1 from "../components/Navigation1";
import SiteLogo from "../components/SiteLogo";
import FeaturedJob from "../components/FeaturedJob";
import Footer from "../components/Footer";
import styles from "./CandidateHomepage.module.css";

const CandidateHomepage = () => {
  const [featuredJobs, setFeaturedJobs] = useState([]);
  const [isLoading, setIsLoading] = useState(true); // State to track loading status
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchRecommendedJobs = async () => {
      setIsLoading(true); // Start loading before fetching
      try {
        const response = await fetch('http://localhost:8000/Applicant/send-recommendations/', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const json = await response.json();
        console.log('Received jobs:', json);
        
        let jobsArray = json.recommended_jobs.map(item => {
          // Transform the item into something else
          console.log(item)
          return {
            id: item.id,
            title: item.title,
              company: item.company,
              location: item.location,
              score: item.score
            
          };
        });
        console.log("logging jobs array")
        console.log(jobsArray)
        setFeaturedJobs(jobsArray);


     
      } catch (error) {
        console.error('Error fetching recommended jobs:', error);
      } finally {
        setIsLoading(false); // Stop loading after fetching
      }
    };

    if (token) {
      fetchRecommendedJobs();
    }
  }, [token]);

  // Loading Icon component using your logo
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
    <div className={styles.candidateHomepage}>
      <Navigation1 />
      <SiteLogo
        findAJobThatSuitsYourInte={`Find a job that suits your interest & skills.`}
        jobTitleKeywordPlacehold="Job title, Keyword..."
      />
      {isLoading ? (
        <LoadingIcon />
      ) : (
        <FeaturedJob
          jobsYouMightLike="Jobs you might like...&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
          featuredJobs={featuredJobs} // Pass the fetched jobs to the FeaturedJob component
        />
      )}
      <Footer />
    </div>
  );
};

export default CandidateHomepage;
