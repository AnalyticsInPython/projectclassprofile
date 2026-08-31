# Class Profile Matcher — Project Proposal

**Team:** Malaika K, Obiari U, Hajime T, Justin P

## Overview

We propose to build a website that helps students in our class connect with one another by intelligently matching them using the information already collected in our class profile. Rather than requiring students to manually scan a spreadsheet or slide deck of bios, the site will surface relevant classmates automatically based on shared interests, similar professional/academic backgrounds, geographic proximity, and visual similarity drawn from submitted profile photos.

## Problem Statement

Class profiles are typically distributed as static documents (spreadsheets, PDFs, or slide decks) that are difficult to search or filter. As a result, students rarely discover classmates they would genuinely benefit from meeting — whether for networking, project teams, or simply making friends with people who live nearby or share hobbies. We want to turn this static dataset into an interactive tool that makes those connections easier to find.

## Goals

1. **Ingest and structure the class profile data** into a clean, queryable dataset (interests, background/experience, location, and profile photo).
2. **Build a matching engine** that scores and ranks classmates by:
   - **Interests** — shared hobbies, extracurriculars, or stated interests.
   - **Background** — similar academic, professional, or industry experience.
   - **Proximity** — geographic closeness (hometown, current location, or neighborhood).
   - **Profile photo** — visual similarity across submitted photos, as an additional lightweight matching signal.
3. **Deliver a website** where a student can select or search for themselves and view a ranked list of best-matched classmates, with the reasons for each match shown transparently.
4. **Present results in an intuitive, presentable interface** suitable for a class demo.

## Approach

- **Data processing:** Use Python (pandas) to clean and structure the raw class profile data into a consistent schema.
- **Matching logic:**
  - Interests and background: text similarity / feature-overlap scoring (e.g., TF-IDF or simple keyword-overlap scoring) across profile fields.
  - Proximity: geocode location fields and compute distance-based scores.
  - Profile photo: use a pretrained image embedding model to compute visual similarity between photos as a supplementary signal.
  - Combine individual signals into a single weighted match score per pair of students.
- **Website:** A simple interactive front end (e.g., Streamlit or Flask) that lets a user pick their name and view their top matches, with a breakdown of why each match was suggested.

## Deliverables

- A website with a python backend that visualizes the class profile dataset. 
- A summary file that notes all of teammates observations with claude.
- A short write-up/presentation summarizing our methodology and findings.


