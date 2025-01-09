import { FunctionComponent } from "react";
import Navigation2 from "../components/Navigation2";
import EmployerProfile from "../components/EmployerProfile";
import styles from "./EmployerMyProfile.module.css";

const EmployerMyProfile = () => {
  return (
    <div className={styles.candidateSettingAccount}>
      <Navigation2 />
      <section className={styles.candidateSettingsWrapper}>
        <EmployerProfile />
      </section>
    </div>
  );
};

export default EmployerMyProfile;
