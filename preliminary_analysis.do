version 15.0
clear all
set more off
capture log close

* Change this path if needed.
local datafile "working_dataset.dta"
local outdir "stata_review_output"

capture mkdir "`outdir'"
log using "`outdir'/preliminary_analysis.log", text replace
use "`datafile'", clear

* Household identifier is unique within state.
egen hh_tag = tag(state hh_code)

display "1. HOUSEHOLD SIZES AND INDIVIDUALS BY STATE"

* Household counts and household-size distribution.
tab state_labeled if hh_tag, missing
tab state_labeled hhsize if hh_tag, row

* Individual counts and distribution across states.
tab state_labeled, missing
tab sex_labeled, missing

display "2. EDUCATION BY HOUSEHOLD MEMBER AND STATE"
tab relationship_head_labeled general_educ_labeled, row missing
tab state_labeled general_educ_labeled, row missing
tab sex_labeled general_educ_labeled, row missing

display "3. PRIMARY EMPLOYMENT NATURE BY MEMBER, STATE, SEX"
tab relationship_head_labeled employment_nature, row missing
tab state_labeled employment_nature, row missing
tab sex_labeled employment_nature, row missing

display "4. AGE BY HOUSEHOLD MEMBER AND STATE"
tabstat age, by(state_labeled) statistics(n mean p50 min max)
tabstat age, by(relationship_head_labeled) statistics(n mean p50 min max)

display "5. RURAL AND URBAN JOBS BY MEMBER AND STATE"

encode employment_location, gen(job_location_code)
tab employment_location, missing
tab relationship_head_labeled job_location_code, row missing
tab state_labeled job_location_code, row missing

* Rural/urban distribution among records classified as rural or urban.
tab state_labeled employment_location if ///
    inlist(employment_location,"rural","urban"), row

display "6. AVERAGE HOUSEHOLD EXPENDITURE"

* Household-level summaries: count each household once.
tabstat expenditure if hh_tag, by(hhsize) ///
    statistics(n mean p50 sd) columns(statistics)
tabstat expenditure if hh_tag, by(state_labeled) ///
    statistics(n mean p50 sd) columns(statistics)

* Member-level summaries: household expenditure is linked to each member.
tabstat expenditure, by(relationship_head_labeled) ///
    statistics(n mean p50 sd) columns(statistics)
tabstat expenditure, by(general_educ_labeled) ///
    statistics(n mean p50 sd) columns(statistics)
tabstat expenditure, by(status_labeled) ///
    statistics(n mean p50 sd) columns(statistics)

display "7. NATIONAL AND STATE-WISE EMPLOYMENT"
preserve
    * generate new variables to capture conditions
    gen earnings = .
    gen contract_present = .
    gen employed = .

    * capture if last months earnings were above 0
    replace earnings = 1 if earn_l30d > 0
    replace earnings = 0 if earn_l30d == 0
    
    * capture if person has job contract for at least an year or more
    replace contract_present = 0 if contract_type_labeled == 0 | contract_type_labeled == 1
    replace contract_present = 1 if contract_type_labeled == 2 | contract_type_labeled == 3
    encode employment_nature, gen(employment_nature_labeled)
    
    * captrue if current nature of employment directly indicates employment
    replace employed = 0 if employment_nature_labeled == 2 | employment_nature_labeled == 5
    replace employed = 1 if employment_nature_labeled != 2 & employment_nature_labeled != 5
    count if earnings == 1 & contract_present == 1 & employed == 1
    
    * store employment status based on conditions in new variables for tabulations
    gen employed_check = .
    replace employed_check = 1 if earnings == 1 & contract_present == 1 & employed == 1
    replace employed_check = 0 if employed_check == .

    tab state_labeled employed_check, row missing
    tab sex_labeled employed_check, row missing
    tab relationship_head_labeled employed_check, row missing
restore

display "8. WAGE REGRESSIONS: PRIMARY ACTIVITY"

* Only positive recorded wages are used.
* Robust standard errors are reported.
regress d7a1_wage i.sex_labeled if d7a1_wage > 0, vce(robust)
regress d7a1_wage i.sex_labeled##i.general_educ_labeled ///
    if d7a1_wage > 0, vce(robust)
regress d7a1_wage c.hhsize ///
    if d7a1_wage > 0, vce(robust)
regress d7a1_wage i.relationship_head_labeled ///
    if d7a1_wage > 0, vce(robust)
regress d7a1_wage c.hhsize##i.relationship_head_labeled ///
    if d7a1_wage > 0, vce(robust)

display "9. WAGE REGRESSIONS: SECONDARY ACTIVITY"

regress d7a2_wage i.sex_labeled if d7a2_wage > 0, vce(robust)
regress d7a2_wage i.sex_labeled##i.general_educ_labeled ///
    if d7a2_wage > 0, vce(robust)
regress d7a2_wage c.hhsize ///
    if d7a2_wage > 0, vce(robust)
regress d7a2_wage i.relationship_head_labeled ///
    if d7a2_wage > 0, vce(robust)
regress d7a2_wage c.hhsize##i.relationship_head_labeled ///
    if d7a2_wage > 0, vce(robust)

display "END OF ANALYSIS"
log close
