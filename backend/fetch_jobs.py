from pymongo import MongoClient

# paste your MongoDB Atlas connection string below
client = MongoClient("mongodb+srv://admin:admin123@cluster0.2mpolvg.mongodb.net/?appName=Cluster0")

db = client["job_ecosystem"]
collection = db["jobs"]


def fetch_jobs():
    jobs = [
        {
            "title": "Java Backend Developer",
            "company": "Infosys",
            "location": "Bangalore"
        },
        {
            "title": "Python AI Intern",
            "company": "Startup Labs",
            "location": "Remote"
        }
    ]
    return jobs


def save_jobs(jobs):
    for job in jobs:
        if collection.find_one(job) is None:
            collection.insert_one(job)
            print("Saved:", job["title"])
        else:
            print("Duplicate skipped:", job["title"])


def main():
    print("Fetching jobs...\n")
    jobs = fetch_jobs()
    save_jobs(jobs)


if __name__ == "__main__":
    main()
