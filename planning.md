# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
#### My project domain is an unofficial guide to the UC Merced Computer Science and Engineering major. This system will help students ask questions about CSE courses, degree requirements, professors, electives, programming focus, and student experiences. This knowledge is valuable because official university pages explain requirements, but they do not always explain what students actually experience in classes or with professors. The information is hard to find because it is spread across the UC Merced catalog, advising pages, program maps, Rate My Professor reviews, Reddit discussions, Quora posts, and course review sites.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | UC Merced CSE Catalog Course Plan | Official 2023 CSE course plan and catalog information | https://catalog.ucmerced.edu/content.php?catoid=22&navoid=2362 |
| 2 | UC Merced CSE Major Requirements | Official required courses and major preparation information|https://catalog.ucmerced.edu/preview_program.php?catoid=22&poid=2703|
| 3 | UC Merced CSE Department / Faculty Page | Faculty information and CSE department overview |https://engineering.ucmerced.edu/departments/computer-science-engineering-cse|
| 4 |CSE Program Map| PDF program map showing course sequencing for the CSE major |https://engr-advising.ucmerced.edu/sites/g/files/ufvvjh2091/f/page/documents/cse_flow_21_22_final_0.pdf|
| 5 | Reddit: Hardest and Easiest CSE Electives | Student discussion about which CSE electives are difficult or manageable |https://www.reddit.com/r/ucmerced/comments/1nu6w64/comment/ngzspcp/ |
| 6 | Reddit: How is the CSE Program? | Student discussion about the quality and experience of the UC Merced CSE program  | https://www.reddit.com/r/ucmerced/comments/1i1njqh/how_is_the_computer_science_and_engineering/ |
| 7 | Quora: Programming Focus in CSE | Discussion about whether UC Merced CSE focuses on programming |https://www.quora.com/Does-the-major-of-computer-science-and-engineering-have-a-focus-on-programming-at-all-I-am-interested-in-programming-and-want-to-go-to-UC-Merced|
| 8 | Rate My Professor | General scores for CSE professors | https://www.ratemyprofessors.com/search/professors/4767?q=*&did=11 |
| 9 | Rate My Professor: Pengfei Su | Student reviews related to CSE 100 Algorithm Design and Analysis | https://www.ratemyprofessors.com/professor/2723300 |
| 10 | Rate My Professor: Hua Huang |Student reviews related to CSE 100, prerequisites, and upper-level courses | https://www.ratemyprofessors.com/professor/2778518 |
| 11 | Rate My Professor: Santosh Chandrasekhar | Student reviews related to CSE 031 Computer Organization and Assembly  and CSE 120 Software Development | https://www.ratemyprofessors.com/professor/2426500 |
| 12 | Rate My Professor: Angelo Kyrilov | Student reviews related to CSE 022 Introduction to Programming, CSE 024 Advanced Programming, and CSE 030 Data Structures | https://www.ratemyprofessors.com/professor/2287924 |
| 13 | Rate My Professor: Stefano Carpin | Student reviews related to CSE 015 Discrete Mathematics and CSE 180 Intro to Robotics | https://www.ratemyprofessors.com/professor/2613245 |
| 14 | Rate My Professor: Ross Greer | Student reviews related to CSE 185 Computer Vision | https://www.ratemyprofessors.com/professor/3105710 |
| 15 | Rate My Professor: Ammon Hepworth | Student reviews related to CSE 108 Web Development | https://www.ratemyprofessors.com/professor/2767416 |
| 16 | Coursicle UC Merced CSE Courses | Course listings and possible student course feedback | https://www.coursicle.com/ucmerced/courses/CSE/ | 

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
