# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains financial analysis for Douglas County School District (Nevada) regarding the potential consolidation of two lake schools: Zephyr Cove Elementary and George Whittell High School. The analysis uses Nevada's Pupil-Centered Funding Plan (PCFP) data to model funding impacts under various scenarios.

## Key Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the main analysis
python3 lake_schools_analysis.py
```

## Data Sources

- **PCFP Model 2025-2027_L01_Final_6-4-25.xlsx**: Nevada state funding model with enrollment, size adjustments, weighted funding, and transportation allocations
- **DCSD_FY25-26_May_Final_Budget.pdf**: District budget document (unprocessed)

## Architecture

### Main Analysis Script
`lake_schools_analysis.py` - Python script that:
- Reads enrollment data from PCFP Excel sheets (via `openpyxl`/`pandas`)
- Calculates District Size Adjustment impacts using Nevada's tiered formula
- Models funding loss scenarios based on student retention rates (100%, 50%, 10%)

Key functions:
- `analyze_funding_impact()`: Main analysis comparing Zephyr Cove vs Gardnerville/Minden funding
- `run_scenario_analysis(retention_rate)`: Models financial impact based on % of students transferring to valley schools
- `get_size_adjustment_data()`: Extracts size adjustment data from PCFP sheets

### Output Documents
- `Lake_Schools_Board_Report.md`: Formal board presentation with scenario analysis
- `School_Funding_Analysis.md`: Funding contribution leaderboard and net contribution framework
- `SURVEY_BRAINSTORM.md` / `FAMILY_SURVEY_SPEC.md`: Survey design for gathering family intentions

## Key Domain Concepts

**District Size Adjustment**: Nevada's PCFP provides higher per-pupil funding for small, isolated attendance areas. Zephyr Cove receives $7,772/pupil vs $745/pupil for Gardnerville/Minden. This is the critical funding mechanism - closing lake schools loses this differential regardless of student retention.

**Retention Rate Impact**: Financial loss increases as fewer students transfer to valley schools:
- 100% retention: ~$1.9M annual loss (size adjustment only)
- 10% retention: ~$4.4M annual loss (base funding + size adjustment)
