# DATA440_final_project

## How to run the project

From the repository root, run:

```bash
uv run main.py
```

You will be prompted to enter one or more research interests:

```bash
Enter your research interests:
```

After entering your input, the system will:

1.  Scrape faculty data from department website

2. Retrieve publications from Semantic Scholar

3. Compute relevance scores based on profile and publications

4. Display the top recommended faculty members

 For each professor, the output includes:

- **Name** – faculty member’s full name  
- **Title** – academic position  
- **Contact information (email)** – for outreach  
- **Webpage** – direct link to faculty profile  
- **Final relevance score** – combined score based on profile and publications  

You can rerun the program with different research interests to explore different recommendations.