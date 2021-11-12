# Vet Hospital Visits for Pets

## 1. Introduction

This is a python project with an ETL pipeline for vet hospital visits data with an accompanying dimensional model.

## 2. Requirements

To set up in a new python environment run `pip install -r requirements.txt`. 
Add new package names to requirements.in, make sure pip-tools is installed (`pip install pip-tools`)  and run `pip-compile requirements.in` to set a specific package version of any new requirements.

## 3. ETL (Extract, Transformation, and Loading) Pipeline

## 4. Dimensional Modelling

### 4.1 Business Process

Assumption that the model is being built for Senior Management to get a holistic view of vet hospital visits and procedures carried out.

### 4.2 Grain

An individual pet hospital visit, billed in a specified currency with a visit cost equal to the total cost of the procedure carried out at that visit, for an owners pet of a given species and breed.

### 4.3 Dimensions and facts

These are outlined in the next section diagram.

## 5. ERD (Entity Relationship Diagram)

![](visits_erd.png)

## 6. Stakeholder Q's

    1. Ask about what sort of analysis is required  e.g. averages, counts, totals, KPIs and other derived figures
    2. Procedure list including cost - fixed per currency or not?
    3. Hospital List
    4. What currencies are visits currently billed in? Is it a single currency per hospital based on location?
    5. Are exchange rates required / available?
    6. Interest in owner geolocations and analysis?

## 7. Other Assumptions

    1. Only one procedure per visit
    2. Visits can't overlap
    2. The procedure and cost of scheduled future visits (e.g. those in the data in 2022) are fixed so they don't need to be treated differently to prior visits

## 8. Further steps

   1. Data cleaning / validation - e.g. check types, formats for dates, visit cost, etc
   2. Add error handling for all functions
   3. Set up AWS account and test
   4. Build unit and integration tests using pytest
   5. CI using black, pylint, lizard, flake8, bandit, and pytest
