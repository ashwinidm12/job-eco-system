import React, { useEffect, useState } from "react";
import "./App.css";
import Login from "./Login";
import { authFetch } from "./api";

// Restore session: user = { email } and token in localStorage
function getStoredUser() {
  const token = localStorage.getItem("token");
  const userStr = localStorage.getItem("user");
  if (!token || !userStr) return null;
  try {
    return JSON.parse(userStr);
  } catch {
    return null;
  }
}

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("");
  const [company, setCompany] = useState("");
  const [selectedJob, setSelectedJob] = useState(null);
  const [user, setUser] = useState(getStoredUser);
  const [jobsLoading, setJobsLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      setJobsLoading(false);
      return;
    }
    authFetch("/jobs")
      .then((res) => {
        if (!res) {
          setUser(null);
          return;
        }
        if (!res.ok) throw new Error("Server error");
        return res.json();
      })
      .then((data) => data && setJobs(data.jobs || []))
      .catch((err) => console.log("Fetch skipped:", err))
      .finally(() => setJobsLoading(false));
  }, [user]);


  const filteredJobs = jobs.filter(job =>
  (search === "" || job.title.toLowerCase().includes(search.toLowerCase())) &&
  (location === "" || job.location.toLowerCase().includes(location.toLowerCase())) &&
  (company === "" || job.company.toLowerCase().includes(company.toLowerCase()))
);


  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
  };

  if (!user) {
    return <Login onLogin={setUser} />;
  }

  return (
    <div className="page">
      <nav className="navbar">
        <span>🚀 Job Eco System</span>
        <div className="nav-right">
          <span className="nav-email">{user.email}</span>
          <button type="button" className="btn-logout" onClick={logout}>
            Logout
          </button>
        </div>
      </nav>

      <div className="container">

        <h2 className="title">Find Your Job</h2>
        {jobsLoading && <p className="loading">Loading jobs…</p>}

        <div className="filters">
          <input placeholder="Search title…" value={search} onChange={e => setSearch(e.target.value)} />
          <input placeholder="Location…" value={location} onChange={e => setLocation(e.target.value)} />
          <input placeholder="Company…" value={company} onChange={e => setCompany(e.target.value)} />
        </div>

        <div className="grid">
          {filteredJobs.map((job, index) => (
            <div className="card" key={index}>
              <h3>{job.title}</h3>
              <p>{job.company}</p>
              <span>{job.location}</span>
              <button onClick={() => setSelectedJob(job)}>
                View Details
              </button>
            </div>
          ))}
        </div>

      </div>

      {selectedJob && (
        <div className="modal-overlay" onClick={() => setSelectedJob(null)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h2>{selectedJob.title}</h2>
            <p><strong>Company:</strong> {selectedJob.company}</p>
            <p><strong>Location:</strong> {selectedJob.location}</p>
            <p className="desc">
              This is a preview job description. Later we will fetch real job
              data automatically.
            </p>
            <button className="close" onClick={() => setSelectedJob(null)}>
              Close
            </button>
          </div>
        </div>
      )}

    </div>
  );
}

export default App;
