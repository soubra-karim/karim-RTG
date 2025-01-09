import { FunctionComponent, useMemo, type CSSProperties } from "react";
import styles from "./Footer.module.css";

export type FooterType = {
  /** Style props */
  propMargin?: CSSProperties["margin"];
  propMargin1?: CSSProperties["margin"];
  propMargin2?: CSSProperties["margin"];
};

const Footer: FunctionComponent<FooterType> = ({
  propMargin,
  propMargin1,
  propMargin2,
}) => {
  const quickLink1Style: CSSProperties = useMemo(() => {
    return {
      margin: propMargin,
    };
  }, [propMargin]);

  const candidate1Style: CSSProperties = useMemo(() => {
    return {
      margin: propMargin1,
    };
  }, [propMargin1]);

  const employers1Style: CSSProperties = useMemo(() => {
    return {
      margin: propMargin2,
    };
  }, [propMargin2]);

  return (
    <footer className={styles.footer}>
      <div className={styles.frameFooterLink}>
        <div className={styles.frameFooterLink1}>
          <div className={styles.frameFooterLink2} />
        </div>
        <div className={styles.frameFooterLink3}>
          <div className={styles.frameFooterLinkInner}>
            <div className={styles.jobSyncTextParent}>
              <div className={styles.jobSyncText} />
              <div className={styles.siteLogoText}>
                <div className={styles.footerLinksContainer} />
                <div className={styles.footerLinksContainer1}>
                  <h2 className={styles.jobsync}>JobSync</h2>
                  <div className={styles.sitelogo} />
                </div>
              </div>
            </div>
          </div>
          <div className={styles.callnowText}>
            <div className={styles.callNow}>Call now:</div>
            <div className={styles.callToAction}> 1(800) 123-4567</div>
          </div>
        </div>
      </div>
      <div className={styles.footer1}>
        <div className={styles.com}>
          <h3 className={styles.quickLink} style={quickLink1Style}>
            Quick Link
          </h3>
          <div className={styles.link}>
            <div className={styles.footerLink}>
              <img
                className={styles.fiarrowRightIcon}
                alt=""
                src="/fiarrowright2.svg"
              />
              <div className={styles.footerLink1}>About</div>
            </div>
            <div className={styles.footerLink2}>
              <div className={styles.contact}>Contact</div>
            </div>
          </div>
        </div>
        <div className={styles.candidate}>
          <h3 className={styles.candidate1} style={candidate1Style}>
            Candidate
          </h3>
          <div className={styles.link1}>
            <div className={styles.footerLink3}>
              <img
                className={styles.fiarrowRightIcon1}
                alt=""
                src="/fiarrowright2.svg"
              />
              <div className={styles.footerLink4}>Browse Jobs</div>
            </div>
            <div className={styles.footerLink5}>
              <img
                className={styles.fiarrowRightIcon2}
                alt=""
                src="/fiarrowright2.svg"
              />
              <div className={styles.footerLink6}>Browse Employers</div>
            </div>
            <div className={styles.footerLink7}>
              <img
                className={styles.fiarrowRightIcon3}
                alt=""
                src="/fiarrowright2.svg"
              />
              <div className={styles.footerLink8}>Candidate Dashboard</div>
            </div>
            <div className={styles.footerLink9}>
              <img
                className={styles.fiarrowRightIcon4}
                alt=""
                src="/fiarrowright2.svg"
              />
              <div className={styles.footerLink10}>Saved Jobs</div>
            </div>
          </div>
        </div>
        <div className={styles.employers}>
          <h3 className={styles.employers1} style={employers1Style}>
            Employers
          </h3>
          <div className={styles.link2}>
            <div className={styles.footerLink11}>
              <img
                className={styles.fiarrowRightIcon5}
                alt=""
                src="/fiarrowright2.svg"
              />
              <div className={styles.footerLink12}>Post a Job</div>
            </div>
            <div className={styles.footerLink13}>
              <img
                className={styles.fiarrowRightIcon6}
                alt=""
                src="/fiarrowright2.svg"
              />
              <div className={styles.footerLink14}>Browse Candidates</div>
            </div>
            <div className={styles.footerLink15}>
              <img
                className={styles.fiarrowRightIcon7}
                alt=""
                src="/fiarrowright2.svg"
              />
              <div className={styles.employersDashboard}>
                Employers Dashboard
              </div>
            </div>
            <div className={styles.footerLink16}>
              <img
                className={styles.fiarrowRightIcon8}
                alt=""
                src="/fiarrowright2.svg"
              />
              <div className={styles.footerLink17}>Applications</div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
