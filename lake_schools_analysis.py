#!/usr/bin/env python3
"""
Lake Schools Financial Analysis
Douglas County - Zephyr Cove Elementary & George Whittell High School

Analyzes the PCFP (Pupil-Centered Funding Plan) data to build a financial case
for keeping the lake schools open.
"""

import pandas as pd
import warnings
warnings.filterwarnings('ignore')

EXCEL_FILE = 'PCFP Model 2025-2027_L01_Final_6-4-25.xlsx'

def load_data():
    """Load the Excel file."""
    return pd.ExcelFile(EXCEL_FILE)

def get_enrollment_data(xlsx):
    """Get Douglas County school enrollment data."""
    df = pd.read_excel(xlsx, sheet_name='1.2 Budgeted Enrollment YR1', header=7)
    douglas = df[df['County'].astype(str).str.lower().str.contains('douglas', na=False)]
    return douglas

def get_size_adjustment_data(xlsx, year=1):
    """Get District Size Adjustment data by attendance area."""
    sheet = '2.4 District Size Adj. YR1' if year == 1 else '6.4 District Size Adj. YR2'
    df = pd.read_excel(xlsx, sheet_name=sheet, header=12)
    return df

def analyze_funding_impact():
    """Main analysis function."""
    xlsx = load_data()

    # Key constants from the data
    ZEPHYR_ENROLLMENT_YR1 = 272.768698
    ZEPHYR_SIZE_ADJ_YR1 = 2119889
    ZEPHYR_PP_ADJ_YR1 = 7771.745873

    ZEPHYR_SIZE_ADJ_YR2 = 2135622
    ZEPHYR_PP_ADJ_YR2 = 7829.424779

    GARDNERVILLE_PP_ADJ = 745.121817
    STATEWIDE_BASE_PP = 9432

    DISTRICT_TOTAL_ENROLLMENT = 4790.585946
    DISTRICT_TOTAL_SIZE_ADJ = 5784916

    print("=" * 80)
    print("LAKE SCHOOLS FINANCIAL IMPACT ANALYSIS")
    print("Zephyr Cove Elementary & George Whittell High School")
    print("Douglas County School District, Nevada")
    print("=" * 80)

    # School enrollment details
    enrollment_df = get_enrollment_data(xlsx)
    zephyr_elem = enrollment_df[enrollment_df['District Name'].str.contains('Zephyr Cove Elementary', na=False)]['Enrollment (projected)'].values[0]
    whittell_hs = enrollment_df[enrollment_df['District Name'].str.contains('George Whittell', na=False)]['Enrollment (projected)'].values[0]

    print(f"""
SCHOOL ENROLLMENT (FY2026 Projected):
-------------------------------------
  Zephyr Cove Elementary School:    {zephyr_elem:>8.1f} students
  George Whittell High School:      {whittell_hs:>8.1f} students
  ─────────────────────────────────────────────
  TOTAL LAKE SCHOOLS:               {zephyr_elem + whittell_hs:>8.1f} students

  % of Douglas County District:     {(zephyr_elem + whittell_hs)/DISTRICT_TOTAL_ENROLLMENT*100:.1f}%
""")

    print("""
═══════════════════════════════════════════════════════════════════════════════
KEY FINDING: SMALL SCHOOL SIZE ADJUSTMENT
═══════════════════════════════════════════════════════════════════════════════

Nevada's Pupil-Centered Funding Plan (PCFP) includes a "District Size
Adjustment" that provides additional per-pupil funding for small, isolated
attendance areas. This adjustment recognizes that small schools have higher
per-pupil costs but serve important community needs.
""")

    print(f"""
ZEPHYR COVE ATTENDANCE AREA vs. GARDNERVILLE/MINDEN:
────────────────────────────────────────────────────────────────────────────────
                              Zephyr Cove     Gardnerville/Minden     Difference
────────────────────────────────────────────────────────────────────────────────
Enrollment:                   {ZEPHYR_ENROLLMENT_YR1:>10.1f}          4,496.1
Per-Pupil Size Adjustment:    ${ZEPHYR_PP_ADJ_YR1:>9,.2f}          ${GARDNERVILLE_PP_ADJ:>9,.2f}          ${ZEPHYR_PP_ADJ_YR1 - GARDNERVILLE_PP_ADJ:>+10,.2f}
Total Size Adjustment:        ${ZEPHYR_SIZE_ADJ_YR1:>9,}        ${3350112:>11,}
────────────────────────────────────────────────────────────────────────────────

The Zephyr Cove area receives {ZEPHYR_PP_ADJ_YR1/GARDNERVILLE_PP_ADJ:.1f}x MORE per-pupil funding adjustment
than Gardnerville/Minden due to the small school size formula.
""")

    print("""
═══════════════════════════════════════════════════════════════════════════════
FUNDING LOSS IF LAKE SCHOOLS CLOSE
═══════════════════════════════════════════════════════════════════════════════
""")

    yr1_loss = ZEPHYR_SIZE_ADJ_YR1 - (ZEPHYR_ENROLLMENT_YR1 * GARDNERVILLE_PP_ADJ)
    yr2_loss = ZEPHYR_SIZE_ADJ_YR2 - (ZEPHYR_ENROLLMENT_YR1 * GARDNERVILLE_PP_ADJ * 1.007)  # Est. inflation

    print(f"""
If lake schools close and students transfer to Gardnerville/Minden schools:

YEAR 1 (FY2026):
  Current Size Adjustment (Zephyr Cove):    ${ZEPHYR_SIZE_ADJ_YR1:>12,}
  Would receive at G/M rate:                 ${int(ZEPHYR_ENROLLMENT_YR1 * GARDNERVILLE_PP_ADJ):>12,}
  ─────────────────────────────────────────────────────────────
  ANNUAL LOSS TO DISTRICT:                   ${int(yr1_loss):>12,}

YEAR 2 (FY2027):
  Current Size Adjustment (Zephyr Cove):    ${ZEPHYR_SIZE_ADJ_YR2:>12,}
  Would receive at G/M rate:                 ${int(ZEPHYR_ENROLLMENT_YR1 * GARDNERVILLE_PP_ADJ * 1.007):>12,}
  ─────────────────────────────────────────────────────────────
  ANNUAL LOSS TO DISTRICT:                   ${int(yr2_loss):>12,}

════════════════════════════════════════════════════════════════════════════════
  BIENNIAL (2-YEAR) FUNDING LOSS:            ${int(yr1_loss + yr2_loss):>12,}
════════════════════════════════════════════════════════════════════════════════
""")

    print("""
═══════════════════════════════════════════════════════════════════════════════
PROPORTION OF DISTRICT FUNDING AT RISK
═══════════════════════════════════════════════════════════════════════════════
""")

    print(f"""
The lake schools represent a DISPROPORTIONATE share of the district's
Size Adjustment funding:

  Lake Schools Enrollment:        {ZEPHYR_ENROLLMENT_YR1/DISTRICT_TOTAL_ENROLLMENT*100:>6.1f}% of district
  Lake Schools Size Adjustment:   {ZEPHYR_SIZE_ADJ_YR1/DISTRICT_TOTAL_SIZE_ADJ*100:>6.1f}% of district's total

In other words, while the lake schools serve only 5.7% of students, they
bring in 36.6% of the district's Size Adjustment funding - this is by
design, to support small, isolated schools.

Closing these schools would mean losing ${ZEPHYR_SIZE_ADJ_YR1:,} annually in
Size Adjustment funding that CANNOT be replaced by transferring students
to larger schools.
""")

    print("""
═══════════════════════════════════════════════════════════════════════════════
ADDITIONAL CONSIDERATIONS
═══════════════════════════════════════════════════════════════════════════════

1. TRANSPORTATION COSTS
   - Students would need to be bused ~30+ miles to Gardnerville/Minden
   - Additional transportation costs would offset some "savings" from closure
   - Current transportation funding: $3,977,265 (district total)

2. COMMUNITY IMPACT
   - Schools are community anchors in the Lake Tahoe basin
   - Property values and community viability depend on local schools
   - Families may leave the area, causing enrollment decline district-wide

3. BASE FUNDING FOLLOWS STUDENTS
   - The ~$2.6M in base per-pupil funding follows students wherever they go
   - Only the SIZE ADJUSTMENT (~$1.9M/year) is lost to the district

4. NEVADA PCFP INTENT
   - The small school adjustment was specifically designed to protect
     small, isolated schools like Zephyr Cove
   - Closing these schools undermines the policy intent

═══════════════════════════════════════════════════════════════════════════════
SUMMARY
═══════════════════════════════════════════════════════════════════════════════

CLOSING THE LAKE SCHOOLS WOULD RESULT IN:

  → ~$1.9 MILLION annual loss in state funding to Douglas County
  → ~$3.9 MILLION loss over the 2025-2027 biennium
  → Loss of 36.6% of the district's Size Adjustment funding
  → Increased transportation costs
  → Community and economic impacts on the Lake Tahoe area

The small school funding adjustment exists precisely to prevent the closure
of schools like Zephyr Cove Elementary and George Whittell High School.
""")

    return {
        'yr1_loss': yr1_loss,
        'yr2_loss': yr2_loss,
        'biennial_loss': yr1_loss + yr2_loss,
        'zephyr_enrollment': ZEPHYR_ENROLLMENT_YR1,
        'zephyr_size_adj_yr1': ZEPHYR_SIZE_ADJ_YR1,
        'zephyr_size_adj_yr2': ZEPHYR_SIZE_ADJ_YR2,
    }


def compare_attendance_areas(xlsx):
    """Compare Zephyr Cove to other small attendance areas in Nevada."""
    df = get_size_adjustment_data(xlsx)

    # Clean up the dataframe
    df = df.dropna(subset=[df.columns[0], df.columns[2]])  # Drop rows without district and enrollment
    df = df[~df[df.columns[0]].astype(str).str.contains('Total|Calculation|NaN', na=False)]

    print("\n" + "=" * 80)
    print("COMPARABLE SMALL ATTENDANCE AREAS IN NEVADA")
    print("=" * 80)
    print("\nAttendance areas with similar enrollment to Zephyr Cove (200-400 students):\n")

    # This would need proper column mapping, showing structure for now
    print("(See sheet '2.4 District Size Adj. YR1' for full comparison)")


def run_scenario_analysis(retention_rate=1.0):
    """
    Run scenario analysis based on student retention rate.

    Args:
        retention_rate: Fraction of students who would transfer to valley schools (0.0 to 1.0)
    """
    # Key constants
    ZEPHYR_ENROLLMENT = 272.768698
    ZEPHYR_SIZE_ADJ = 2119889
    GARDNERVILLE_PP_ADJ = 745.121817
    STATEWIDE_BASE_PP = 9432

    students_retained = ZEPHYR_ENROLLMENT * retention_rate
    students_lost = ZEPHYR_ENROLLMENT * (1 - retention_rate)

    # Base funding impact (lost if students leave district)
    base_funding_current = ZEPHYR_ENROLLMENT * STATEWIDE_BASE_PP
    base_funding_after = students_retained * STATEWIDE_BASE_PP
    base_funding_loss = base_funding_current - base_funding_after

    # Size adjustment impact (mostly lost regardless, but some retained at G/M rate)
    size_adj_current = ZEPHYR_SIZE_ADJ
    size_adj_after = students_retained * GARDNERVILLE_PP_ADJ
    size_adj_loss = size_adj_current - size_adj_after

    total_loss = base_funding_loss + size_adj_loss

    return {
        'retention_rate': retention_rate,
        'students_retained': students_retained,
        'students_lost': students_lost,
        'base_funding_loss': base_funding_loss,
        'size_adj_loss': size_adj_loss,
        'total_annual_loss': total_loss,
        'biennial_loss': total_loss * 2.01,  # ~1% inflation year 2
    }


def print_scenario_comparison():
    """Print comparison of different retention scenarios."""
    print("\n" + "=" * 80)
    print("SCENARIO ANALYSIS: IMPACT BY STUDENT RETENTION RATE")
    print("=" * 80)

    scenarios = [
        (1.0, "100% transfer to valley (Best Case)"),
        (0.75, "75% transfer to valley"),
        (0.50, "50% transfer to valley (Moderate)"),
        (0.25, "25% transfer to valley"),
        (0.10, "10% transfer to valley (Survey-Based)"),
    ]

    print(f"\n{'Scenario':<40} {'Annual Loss':>15} {'Biennial Loss':>15}")
    print("-" * 72)

    for rate, description in scenarios:
        result = run_scenario_analysis(rate)
        print(f"{description:<40} ${result['total_annual_loss']:>13,.0f} ${result['biennial_loss']:>13,.0f}")

    print("-" * 72)
    print("\nNote: Lower retention = more students leave district entirely = greater loss")
    print("      Survey data suggests only 5-10% of families would transfer to valley schools")

    # Detail for worst case
    worst = run_scenario_analysis(0.10)
    print(f"""
DETAILED BREAKDOWN (10% Retention - Survey-Based):
  Students transferring to valley:     {worst['students_retained']:>8.1f}
  Students leaving district:           {worst['students_lost']:>8.1f}

  Base funding loss (students leave):  ${worst['base_funding_loss']:>12,.0f}
  Size adjustment loss:                ${worst['size_adj_loss']:>12,.0f}
  ──────────────────────────────────────────────────
  TOTAL ANNUAL LOSS:                   ${worst['total_annual_loss']:>12,.0f}
""")


if __name__ == '__main__':
    results = analyze_funding_impact()
    print_scenario_comparison()
    print(f"\nAnalysis complete. See Lake_Schools_Board_Report.md for full report.")
