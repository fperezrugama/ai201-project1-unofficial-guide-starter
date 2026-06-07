# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

#### The Unofficial Guide is a Retrieval-Augmented Generation (RAG) system focused on the University of California, Merced Computer Science and Engineering (CSE) program. The system combines official university information with student experiences gathered from sources such as Reddit, Coursicle, Quora, and Rate My Professor.This knowledge is valuable because many questions students have are not fully answered through official university resources. While the catalog and program requirements explain what courses are required, they do not describe teaching styles, course difficulty, workload, student experiences, or recommendations for electives. Students often need to search through multiple websites, discussion forums, and review platforms to gather this information. The goal of this project is to provide a single interface where students can ask questions about CSE courses, professors, degree requirements, electives, and student experiences, while receiving answers grounded in collected documents and accompanied by source attribution.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 |UC Merced CSE Four-Year Course Plan (2023–2024) | Official Catalog|cse_catalog_course_plan.txt https://catalog.ucmerced.edu/content.php?catoid=22&navoid=2362 |
| 2 | UC Merced CSE Major Requirements | Official Catalog | cse_major_requirements.txt https://catalog.ucmerced.edu/preview_program.php?catoid=22&poid=2703|
| 3 |UC Merced CSE Program Map (2021–2022) | Advising Document |cse_program_map.txt https://engr-advising.ucmerced.edu/sites/g/files/ufvvjh2091/f/page/documents/cse_flow_21_22_final_0.pdf |
| 4 | UC Merced CSE Faculty Directory | Department Website |cse_faculty_page.txt https://engineering.ucmerced.edu/departments/computer-science-engineering-cse |
| 5 | Coursicle UC Merced CSE Courses | Course Reviews | coursicle_reviews.txt https://www.coursicle.com/ucmerced/courses/CSE/|
| 6 | Reddit: Hardest and Easiest CSE Electives | Reddit Discussion |reddit_hardest_electives.txt https://www.reddit.com/r/ucmerced/comments/1nu6w64/comment/ngzspcp/ |
| 7 | Reddit: How is the CSE Program at UC Merced? | Reddit Discussion | reddit_cse_program.txt  https://www.reddit.com/r/ucmerced/comments/1i1njqh/how_is_the_computer_science_and_engineering/ |
| 8 | Reddit: Will CSE Become Impacted? | Reddit Discussion | reddit_cse_impacted_advice.txt https://www.reddit.com/r/ucmerced/comments/1gvksls/will_cse_ever_be_impacted_at_ucm/ |
| 9 |Quora: Does the CSE Major Focus on Programming? | Quora Discussion | quora_programming_focus.txt https://www.quora.com/Does-the-major-of-computer-science-and-engineering-have-a-focus-on-programming-at-all-I-am-interested-in-programming-and-want-to-go-to-UC-Merced |
| 10 |Rate My Professor – Angelo Kyrilov | Student Reviews | rmp_angelo_kyrilov.txt https://www.ratemyprofessors.com/professor/2287924 |
| 11 | Rate My Professor – Pengfei Su | Student Reviews |rmp_pengfei_su.txt https://www.ratemyprofessors.com/professor/2723300 |
| 12 | Rate My Professor – Santosh Chandrasekhar | Student Reviews | rmp_santosh_chandrasekhar.txt https://www.ratemyprofessors.com/professor/2426500 |
| 13 | Rate My Professor – Stefano Carpin | Student Reviews | rmp_stefano_carpin.txt ttps://www.ratemyprofessors.com/professor/2613245 |
| 14 | Rate My Professor – Ammon Hepworth | Student Reviews | rmp_ammon_hepworth.txt  https://www.ratemyprofessors.com/professor/2767416 |
| 15 | Rate My Professor – Ross Greer | Student Reviews | rmp_ross_greer.txt  https://www.ratemyprofessors.com/professor/3105710 |
| 16 | Rate My Professor – Hua Huang | Student Reviews |rmp_hua_huang.txt https://www.ratemyprofessors.com/professor/2778518 |
| 17 | Rate My Professor – Yiwei Wang  | Student Reviews | rmp_yiwei_wang.txt https://www.ratemyprofessors.com/professor/3163467 |
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->


**Chunk size:**
#### Long official university documents were chunked into sections of approximately 300–500 words. 

**Overlap:**
#### An overlap of approximately 75 words was used for longer official documents to preserve context between adjacent chunks.

**Why these choices fit your documents:**

#### The corpus contains two different document types. Official university documents such as program maps, catalogs, and degree requirements are relatively long and contain structured information that benefits from larger chunks and overlap. Student review documents from Reddit, Coursicle, and Rate My Professor are already organized into self-contained sections. For these sources, complete sections were preserved whenever possible rather than splitting them mechanically. Before chunking, metadata headers such as Title, Source Type, URL, and Document Category were extracted and stored separately. The chunking process used only the document body content so that repeated metadata was not embedded into every chunk.

**Final chunk count:**

#### The final corpus contained 17 source documents and 81 chunks.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

#### I used all-MiniLM-L6-v2 from the Sentence Transformers library as the embedding model for this project. The model generates 384-dimensional embeddings and runs locally without requiring an API key or external service. I selected it because it is widely used for semantic search tasks, integrates easily with ChromaDB, and provides a good balance between retrieval quality, speed, and ease of deployment. Since my document collection is relatively small (17 documents and 81 chunks), all-MiniLM-L6-v2 was more than sufficient while keeping indexing and retrieval fast.

**Production tradeoff reflection:**
#### If I were deploying this system for real students and cost was not a constraint, I would evaluate larger embedding models that provide stronger semantic understanding and better retrieval performance on educational and review-based content. One important consideration would be retrieval accuracy for course-specific and professor-specific questions, since those queries require distinguishing between many similar course numbers and instructors. I would also consider multilingual support. While the current corpus is entirely in English, a production system serving a broader student population could benefit from embeddings that perform well across multiple languages. Another tradeoff would be latency versus retrieval quality. Larger embedding models often produce more accurate semantic representations but require more computation and storage. For a university advising system with frequent student use, I would need to balance response speed with retrieval accuracy. Finally, I would compare locally hosted embeddings against API-hosted embedding services. Local embeddings provide greater privacy, lower operating costs over time, and no dependency on external providers. However, API-based models may offer better performance and receive continuous improvements without requiring infrastructure maintenance.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
#### The system uses a retrieval-augmented generation (RAG) pipeline in which relevant document chunks are retrieved from ChromaDB before a response is sent to the LLM. The retrieved chunks are formatted into a context block and passed to the model along with a grounding prompt. The prompt explicitly instructs the model to answer only from the retrieved documents and not rely on outside knowledge. The key instructions include: Answer using only the provided context. Do not guess or fill in missing information. If the retrieved documents do not contain enough information to answer the question, respond with: "I don't have enough information in the provided documents to answer that." Reference supporting sources using source labels such as [S1], [S2], and [S3]. In addition to the prompt instructions, only the top retrieved chunks from the vector database are provided to the model. This limits the model's available information to the documents collected for this project and reduces the likelihood of unsupported answers.

**How source attribution is surfaced in the response:**
#### Source attribution is generated programmatically rather than relying entirely on the LLM. During retrieval, each chunk includes metadata such as filename, title, chunk ID, URL, and retrieval distance score. Retrieved chunks are assigned source labels (for example, [S1], [S2], [S3], and [S4]) before being sent to the model. The LLM uses these labels when writing its response, allowing statements in the answer to be linked to specific retrieved documents. After generation, the application displays a separate source panel that lists:Source label, Document title, Source filename, Chunk ID, Retrieval distance score, Original source URL. This design allows users to verify where information originated and makes it easier to distinguish document-supported answers from unsupported claims. For example, a response about CSE electives may cite [S1] from the Reddit electives discussion and [S2] from a Rate My Professor summary, while the interface simultaneously displays the corresponding documents and links.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What lower-division courses must a UC Merced student complete before taking most upper-division CSE courses? | Should identify the prerequisite sequence leading into upper-division coursework, including CSE 022, CSE 024, CSE 030, CSE 031, and CSE 100. | The system correctly identified CSE 100 and CSE 031 as key prerequisites for many upper-division courses and referenced the program map. It also mentioned the CSE 022 → CSE 024 → CSE 030 → CSE 031 sequence. However, the answer focused more on direct upper-division prerequisites than the full prerequisite pathway. | Relevant | Partially accurate |
| 2 | Which CSE electives do students describe as the hardest and easiest? | Should summarize Reddit opinions about easiest and hardest electives and mention that many students view CSE 100 as difficult. | The system identified CSE 160 and CSE 176 as difficult electives and listed CSE 108, CSE 107, and CSE 111 as easier options. It also incorporated supporting evidence from professor reviews describing CSE 100 as challenging. | Relevant | Accurate |
| 3 | What courses are taught by Professor Stefano Carpin? | Should identify courses associated with Stefano Carpin from faculty information and student reviews. | The system correctly identified CSE 015 (Discrete Mathematics) and CSE 180 (Introduction to Robotics) as courses taught by Professor Stefano Carpin. Retrieved sources came directly from Stefano Carpin review documents. | Relevant | Accurate |
| 4 | Is the UC Merced CSE major heavily focused on programming? | Should combine Quora and official curriculum information to explain the role of programming within the major. | The system concluded that the CSE major is strongly programming-focused, especially during the lower-division sequence. It supported the answer using Quora discussions, Reddit discussions, and faculty information. | Relevant | Accurate |
| 5 | Which courses are required for graduation in the UC Merced CSE major? | Should identify major preparation, lower-division requirements, upper-division requirements, and elective requirements. | The system correctly listed mathematics requirements, physics requirements, lower-division CSE courses, upper-division core courses, technical electives, and ENGR 091. The answer was grounded primarily in the official major requirements document. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
#### Which professor and course are considered the hardest in the UC Merced CSE program?

**What the system returned:**
#### The system identified Professor Stefano Carpin and CSE 015 as among the hardest professor-course combinations in the CSE program.

**Root cause (tied to a specific pipeline stage):**
#### This issue originated during the retrieval and generation stages. The retrieval system successfully found documents mentioning student complaints about CSE 015 and comments describing the course as difficult. However, those chunks did not fully represent the overall sentiment found across the collected reviews. Rate My Professor data for Stefano Carpin contains both positive and negative feedback. While some students described CSE 015 as challenging, Professor Carpin's overall rating remained relatively strong. Because retrieval selects only a small number of relevant chunks, the LLM received evidence emphasizing course difficulty without receiving enough balancing evidence about the professor's overall reputation. As a result, the generated answer overemphasized negative feedback and could lead a student to incorrectly conclude that Professor Carpin is generally considered one of the hardest professors in the department. 

**What you would change to fix it:**
#### I would improve retrieval by incorporating sentiment-aware aggregation or professor-level summary chunks. Instead of relying only on the top retrieved review sections, the system could retrieve an overall professor summary alongside course-specific feedback. This would help the model distinguish between a difficult course and a poorly rated professor. Another improvement would be reranking retrieved chunks to ensure that both positive and negative evidence are included before generation.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
#### The planning document helped me make implementation decisions before writing code. For example, I already knew I wanted to use the all-MiniLM-L6-v2 embedding model, retrieve the top 4 chunks, and use different chunking strategies for official documents versus student-generated content. Having those decisions written down made it much easier to guide AI tools during development because I could provide specific requirements instead of asking for generic RAG code. The Evaluation Plan was also useful because it gave me concrete questions to test throughout development. Rather than waiting until the end, I was able to verify chunking, retrieval, and generation using questions that reflected the actual goals of the project. This helped me identify retrieval issues before moving to later milestones.

**One way your implementation diverged from the spec, and why:**
#### One way my implementation diverged from the original plan was during the embedding stage. Initially, I planned to embed only the chunk text itself. However, after testing retrieval, I noticed that professor-specific questions sometimes retrieved the wrong course chunks. To improve retrieval quality, I modified the embedding process so that metadata such as the title, filename, category, and chunk ID were included in the embedding text while still preserving the original chunk text for display. This improved retrieval performance without changing the source documents. Another small difference was the addition of a Gradio interface with a customized UC Merced-inspired design. The planning document mentioned using either a command-line interface or a simple web interface, but I ultimately chose Gradio because it provided a more user-friendly experience and made it easier to demonstrate the project during testing and the final video.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
#### I gave Claude a detailed overview of my project, including the domain, my document folder structure, and my Milestone 3 goals. I explained that I already had 17 cleaned .txt files in documents/raw/, including Rate My Professor summaries, Reddit discussions, Quora posts, Coursicle reviews, catalog information, and faculty information. I also told it not to implement the whole pipeline at once and asked it to work in checkpoints: ingestion, verification, chunking, chunk inspection, and chunk quality validation.
- *What it produced:*
#### Claude helped plan the ingestion and chunking pipeline. It suggested functions for loading raw documents, extracting metadata, preserving filenames and URLs, and splitting the documents into chunks. It also helped create diagnostic checks that printed the total number of documents loaded, sample text, total chunk count, minimum and maximum word count, and chunk counts grouped by source file.
- *What I changed or overrode:*
#### I did not let the AI implement everything at once. I made it pause after each checkpoint so I could run the code, inspect the output, and decide whether to continue. I also directed the chunking strategy so that long official documents used 300–500 word chunks with overlap, while review-style documents preserved complete course or professor sections. I specifically asked the AI to avoid modifying the raw documents and to avoid moving ahead into embeddings, ChromaDB, retrieval, or generation during Milestone 3.

**Instance 2**

- *What I gave the AI:*
#### I asked AI for help testing and improving the embedding and retrieval stage. I provided the output from my retrieval tests, including distance scores and the returned chunks for questions such as “What do students say about CSE 022 with Angelo Kyrilov?” and “Which CSE electives do students say are hardest or easiest?” I also explained when the results looked wrong, such as when a professor-specific query returned a chunk from a different professor.
- *What it produced:*
#### The AI helped diagnose that the retrieval issue was caused by the embeddings using only the chunk text. Some course-specific chunks did not include enough professor context in the chunk body, so the vector search did not always connect “Angelo Kyrilov” with the correct CSE 022, CSE 024, or CSE 030 chunks. It suggested using metadata-aware embedding text by including information such as title, filename, category, and chunk ID when creating embeddings.
- *What I changed or overrode:*
#### I kept the original chunk text for display and source attribution, but changed the embedding step so that the vector store embedded enriched text containing both metadata context and the chunk body. This improved retrieval without changing the raw documents, ingestion pipeline, or chunking pipeline. I then rebuilt the vector store and reran the same retrieval tests to verify that the correct Angelo course-specific chunks were returned near the top.
