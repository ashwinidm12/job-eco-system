import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch("/jobs")
      .then(res => res.json())
      .then(data => setJobs(data.jobs || []));
  }, []);

  const filteredJobs = jobs.filter(job =>
    job.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="app">
      <header className="header">
        <h1>🚀 Job Eco System</h1>
        <p>Smart Job Aggregator Dashboard</p>

        <input
          className="search"
          type="text"
          placeholder="Search jobs..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </header>

      <div className="jobs">
        {filteredJobs.map((job, index) => (
          <div className="job-card" key={index}>
            <h2>{job.title}</h2>
            <p>{job.company}</p>
            <span>{job.location}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
