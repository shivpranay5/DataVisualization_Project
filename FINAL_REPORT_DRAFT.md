# CSE 578 Course Project Final Report

## Title

Income-Related Factor Analysis for UVW College Marketing Profiles Using the Adult Census Income Dataset

## 1. Goals and Business Objective

The main goal of this project is to identify the factors that are most strongly related to whether an individual earns more than $50K per year. The project is based on the Adult Census Income dataset and is framed around the UVW College marketing scenario described in the course project overview. UVW College wants to use income-related demographic and employment information to better understand which groups may respond to different educational marketing strategies.

The business objective is to provide the UVW marketing team with a set of clear, data-driven insights about the attributes that are most related to income. These findings can help the team organize the factors that would later be useful in a future application or model, but this project itself focuses on visual analysis rather than prediction modeling. In other words, the purpose of this report is to answer the customer ask by revealing the factors related to income and communicating those findings through appropriate visualizations.

## 2. Assumptions

The following technical and business assumptions were used in this project:

1. The Adult Census Income dataset is representative enough to support meaningful exploratory analysis of income-related factors.
2. Records containing missing values in key categorical fields could distort visual interpretation, so a no-missing analysis dataset was used for the main charts.
3. The `fnlwgt` attribute was excluded because the course guidance indicated that it should not be used for this project.
4. Income was treated as a binary label with two groups: `<=50K` and `>50K`.
5. Since the final report is intended for the team supporting a future application, the emphasis should be on interpretability and communication rather than algorithmic prediction performance.
6. Some high-cardinality categorical fields were reduced to the most common categories in certain visualizations so the figures would remain readable and useful.
7. The audience of the report is assumed to be a technical-business team that needs explanations of both what the charts show and why those charts were chosen.

## 3. Selected Attributes

This project uses more than the required eight attributes. The selected attributes are:

- `age`
- `education`
- `education_num`
- `workclass`
- `occupation`
- `marital_status`
- `race`
- `sex`
- `capital_gain`
- `capital_loss`
- `hours_per_week`
- `native_country`
- `income`

These attributes were selected because they represent demographic, educational, occupational, and work-related characteristics that are likely to be related to income level and are suitable for multiple visualization techniques.

## 4. Data Preparation and Background Work

The raw Adult dataset contains 32,561 rows. Before beginning the visual analysis, the dataset was cleaned in Python. The cleaning process included assigning clear column names, trimming whitespace in categorical values, replacing question marks with missing values, standardizing the income labels, and removing the `fnlwgt` field. A cleaned dataset with missing values preserved was created, along with a second analysis-ready dataset that excluded rows with missing values. After removing incomplete records, 30,162 rows remained.

The missing-value analysis showed that the fields with the most missing values were `occupation`, `workclass`, and `native_country`. The class distribution in the cleaned no-missing dataset was 22,654 records in the `<=50K` group and 7,508 records in the `>50K` group. Preliminary numerical summaries also showed that individuals in the higher-income group tend to be older, have higher education levels, work more hours per week, and have substantially larger capital gains.

## 5. User Stories

The following user stories were prioritized for the project:

1. As a member of the UVW marketing team, I want to know whether education level is strongly related to income so that the team can understand how education may correspond to earning potential.
2. As a member of the marketing team, I want to understand how marital status and gender relate to income so that the team can identify combined demographic patterns associated with different income groups.
3. As a team analyst, I want to compare age distributions across race groups and income categories so that I can understand whether age patterns differ within demographic segments.
4. As a marketing analyst, I want to examine how weekly work hours vary by occupation and income so that the team can identify occupations whose work patterns are associated with higher earnings.
5. As a member of the development team, I want to compare occupation and workclass combinations by income share so that the team can identify the occupational contexts most associated with higher income.
6. As a member of the UVW marketing team, I want to see how age, education level, weekly work hours, and capital gain vary together across income groups so that I can identify multivariable patterns related to higher earnings.

These user stories collectively cover more than eight attributes and include both univariate and multivariate analysis, with at least three multivariate visualizations as required.

## 6. Visualizations, Design Process, and Conclusions

### 6.1 User Story 1: Education and Income

**Visualization:** Bar chart  
**Figure:** `education_vs_income.png`

This visualization shows the percentage of individuals earning more than $50K across education levels. A bar chart was chosen because education is a categorical variable with ordered educational groups, and the bar chart makes it easy to compare the relative share of higher-income individuals across categories.

The design process was as follows:
1. Order education categories by their average `education_num` level.
2. Compute the share of individuals in each education group whose income is `>50K`.
3. Use a single-color bar chart to keep the chart clean and direct attention to the comparison across categories.
4. Rotate category labels to maintain readability.

This chart demonstrates that education is strongly related to income. Higher education levels tend to have a larger percentage of individuals earning more than $50K. The conclusion is that education is one of the clearest factors related to income and should be treated as a high-priority attribute in the customer’s future application planning.

### 6.2 User Story 2: Marital Status, Gender, and Income

**Visualization:** Mosaic plot  
**Figure:** `gender_marital_status_income_mosaic.png`

This visualization shows the relationship among marital status, gender, and income. A mosaic plot was selected because all of these variables are categorical, and the chart is useful for showing how combinations of categories differ in their distribution of income outcomes.

The design process was as follows:
1. Select the most common marital-status categories to avoid an overcrowded chart.
2. Group the data by marital status, sex, and income.
3. Use rectangle sizes to represent the relative frequency of category combinations.
4. Keep the labels and layout simple so the chart remains readable.

This chart demonstrates that income is not only related to individual attributes, but also to their combinations. Certain marital-status and gender groupings occupy a noticeably larger share of the higher-income category. The conclusion is that combined demographic factors provide richer insight than single categorical variables alone, making this a valuable multivariate story for the customer.

### 6.3 User Story 3: Race, Age, and Income

**Visualization:** Box plot  
**Figure:** `race_age_income_boxplot.png`

This visualization compares age distributions across race groups and income categories. A box plot was chosen because it summarizes the median, quartiles, and spread of age for each group, which makes it effective for comparing distributions rather than just averages.

The design process was as follows:
1. Group observations by race and income.
2. Plot age as the continuous variable on the y-axis.
3. Use separate color coding for income labels.
4. Retain box plots instead of bars so distribution shape and spread can be seen.

This chart demonstrates that age patterns vary across race and income groups, and that the higher-income category tends to be associated with older individuals in several groups. The conclusion is that age is an important income-related factor, but it is more informative when analyzed within demographic segments rather than in isolation.

### 6.4 User Story 4: Occupation, Work Hours, and Income

**Visualization:** Violin plot  
**Figure:** `occupation_hours_income_violin.png`

This visualization shows how weekly work hours vary by occupation and income group. A violin plot was selected because it communicates both the distribution and the density of hours worked, which is more informative than a simple average when comparing occupational groups.

The design process was as follows:
1. Select the most common occupations so the plot remains readable.
2. Plot `hours_per_week` as the continuous variable and occupation as the comparison category.
3. Split or color the violins by income label.
4. Use quartile markers so the central distribution can be interpreted more easily.

This chart demonstrates that hours worked per week and income are related differently across occupations. Some occupations show wider distributions, while others show more concentrated work-hour patterns for the higher-income group. The conclusion is that occupation and hours worked together provide useful context for understanding income, which makes this visualization valuable for the customer’s analysis.

### 6.5 User Story 5: Occupation, Workclass, and Income Share

**Visualization:** Dot plot  
**Figure:** `occupation_workclass_income_dotplot.png`

This visualization compares the percentage of individuals earning more than $50K across occupation and workclass combinations. A dot plot was selected because it is compact, supports ranking, and makes it easy to compare many grouped categories without the visual heaviness of a large grouped bar chart.

The design process was as follows:
1. Focus on the most common workclass groups.
2. Calculate the share of `>50K` income for occupation-workclass combinations.
3. Select the highest-ranked combinations to keep the chart focused.
4. Use dots and guide lines to make the ranking easy to scan.

This chart demonstrates which occupational contexts are most strongly associated with higher income. It prioritizes the combinations that would be most useful for the customer because it highlights where high-income shares are concentrated. The conclusion is that occupation and workclass should be considered jointly when developing income-related marketing profiles.

### 6.6 User Story 6: Multivariable Pattern Comparison

**Visualization:** Parallel coordinates plot  
**Figure:** `parallel_coordinates_income_factors.png`

This visualization shows how age, education level, weekly work hours, and capital gain vary together across the two income groups. A parallel coordinates plot was selected because it is well suited for multivariate analysis and allows several continuous variables to be compared simultaneously.

The design process was as follows:
1. Sample records from each income class to keep the figure readable.
2. Select the four continuous variables most relevant to the business problem.
3. Scale the variables to a common range so they can be displayed on parallel axes.
4. Color the lines by income group to reveal pattern differences.

This chart demonstrates that the `>50K` group tends to follow a different multivariable pattern than the `<=50K` group, especially on education level, hours worked, and capital gain. The conclusion is that higher income is best understood as the result of multiple interacting factors rather than a single attribute. This is one of the most important findings for the team because it supports the customer’s need to identify combined determinants of income.

## 7. Questions That Arose During the Project

Several important questions arose during the project progression:

1. Should missing-value rows be preserved or removed for the main visual analysis?
2. Should the project include predictive modeling because the overview document mentions an application?
3. Which visualization types best match the course material while also communicating the customer’s question clearly?
4. Which variables should be prioritized so that the final report remains focused and readable?

## 8. Implemented Solutions

The following solutions were implemented to address those questions:

1. A separate no-missing dataset was created for the main analysis so the visualizations would be easier to interpret.
2. The project scope was aligned with the course and TA clarification that modeling is not part of the grading criteria.
3. Visualization choices were revised to emphasize chart types taught in the course, including mosaic plots, box plots, violin plots, dot plots, and parallel coordinates.
4. High-priority attributes were selected based on relevance to income and their ability to support clear user stories.

## 9. Postponed Items / Not Doing Now

The following items are not being completed at this time but may be useful in future work:

1. Building and evaluating a prediction model for income classification.
2. Creating an end-user application interface for the marketing team.
3. Performing formal feature selection or model-driven importance ranking.
4. Expanding geographic or country-based analysis beyond the current scope.
5. Testing how the findings would change under alternative missing-data strategies.

These items were postponed because they are outside the grading criteria for this milestone and because the current project is focused on visual analysis rather than application development.

## 10. Overall Findings

Across the selected visualizations, the project consistently shows that income is related to multiple demographic and employment factors. Education is one of the strongest single factors. Age, hours worked, and capital gain also show meaningful differences between income groups. Combined categorical relationships, such as marital status with gender and occupation with workclass, provide useful additional context that would not be visible in a simpler one-variable analysis.

Overall, the final chart set answers the customer ask by identifying which factors appear most related to income and by presenting them through clear visual evidence. The report therefore provides a strong foundation for the team that will later design and maintain a future application.

## 11. Python Code to Submit Separately

The Python code used for this project is in the following files:

- `process_adult_data.py`
- `analyze_adult_data.py`

These files should be included in the separate Python Code PDF required by the project directions.
