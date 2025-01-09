import { FunctionComponent } from "react";
import Navigation2 from "../components/Navigation2";
import EmployerStatsComponent from "../components/EmployerStatsComponent";
import DashBoard from "../components/PieChart";
import MapComponent from "../components/MapComponent"; // Import the MapComponent
import styles from "./CandidateStats.module.css";
import Footer from "../components/Footer";

const EmployerStats: FunctionComponent = () => {
  return (
    <>
      <Navigation2 />
      <h1 className={styles.searchResultsTitle}>Statistics</h1>
      <div className={styles.candidateDashboard}>
        <EmployerStatsComponent />
        <MapComponent /> {styles.mapContainer}
        <Footer/>
      </div>
      
    </>
  );
};

export default EmployerStats;
