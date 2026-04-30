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

1. User inputs research interests

2. Scrape faculty data from department website

3. Preprocess and clean data

4. Compute base relevance using faculty profile

5. Retrieve publications from Semantic Scholar

6. Compute publication relevance (normalized)

7. Combine scores: final_score = profile_score + 0.5 * publication_score

8. Rank faculty by final score

The output will include each professor’s name, title, contact information, webpage, and final relevance score. 

You can rerun the program with different research interests to explore different recommendations.