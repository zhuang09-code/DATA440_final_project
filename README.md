# DATA440_final_project

## Overview

This project builds an automated faculty recommendation system to help students find professors whose research aligns with their interests.

Finding the right faculty is important because it can improve research opportunities, mentorship, and academic success. Currently, students rely on manually browsing faculty webpages across multiple sources. This process is time-consuming and makes it difficult to identify which faculty members are the best match for their research interests. In addition, faculty webpages may not always provide enough detailed or consistent information to support effective decision-making. There is also a lack of simple tools that can automatically recommend faculty based on a student’s research focus.

This project addresses these challenges by using publicly available faculty and publication data to automate the matching process and generate ranked recommendations.

## How It Works

The system generates faculty recommendations through the following steps:

- User input
- Collect faculty profile data from the department website
- Match user research interests with faculty profile information to compute a base score
- Retrieve publication data from Semantic Scholar
- Compute a publication-based relevance score (normalized by total publications)
- Combine scores: final_score = profile_score + 0.5 × publication_score
- Rank faculty members from highest to lowest final score

## How To Run The Project

From the repository root, run:

```bash
uv run main.py
```

You will be prompted to enter one or more research interests:

```bash
Enter your research interests:
```

After entering your input, the system will generate ranked faculty recommendations based on your research interests.

For each professor, the output includes:

- Name – faculty member’s full name
- Title – academic position
- Contact information – email for outreach
- Webpage – direct link to faculty's personal website (if any) or faculty's department profile
- Final relevance score – combined score based on profile and publications

You can rerun the program with different research interests to explore different recommendations.

## Limitations

Semantic Scholar author matching may not always be accurate, which can lead to incorrect or missing publication data for some faculty members. In addition, some faculty may not have publication data available in Semantic Scholar, which may affect the completeness of the recommendation results. Finally, the system relies on simple keyword matching rather than advanced semantic understanding, which may limit its ability to capture more complex research relationships.

We aimed to address this issue by "scoring" professors. For example, when the query searches for an author after the user input is processed, there may be multiple people with similar names in Semantic Scholar. The system in `scoring.py` is used to compare each possible professor candidate and give them a score based on how well they match the target person. The system is roughly structured like this:

1. Name similarity (most important)
2. Institution match (context clue)
3. Interest overlap (small bonus)

This information comes from the Semantic Scholar website, where some professors may not have profiles complete and set up, so resulting names that may not be accurate show up as a warning to the user. The professor with the highest score is treated as one of the better matches to what the user inputs.
