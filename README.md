# Predicting County Recession Recovery

(Header image)

Can we model which counties of the US are most likely to recover form the 2020 recession?

With the COVID-19 pandemic still active in the United States, millions of Americans are without work, and the economy remains in a precarious position. Additionally, since the start of the 21st century, the United States as spent only seven out of twenty years in a period of recession or recovery. With this project, I intend to model country-level economic performance (jobs) from the last two recessions, and predict which counties are most likely to recover from this recession in time for the next one.

## Definitions and Assumptions:

I will be considering only the raw number of jobs in any given county. A county will be defined as "recovered" if the number of jobs in any fiscal quarter after the recession event surpasses its peak before the event. I will not be taking into account population change, nor will I be considering if a single person holds more than one job.
The "recovery event" for both recessions (2001 & 2007) are in Q3 of 2001 and Q3 of 2008 (Sept. 11 and the 2008 housing price collapse). This does not necessarily correspond with the beginning of the official recession, but as these are the most dramatic periods of shift in the economy.
I will not be considering wages within the county, or the number of firms offering jobs (like I did last time).
All feature measures will be taken from the quarter of the

## Dataset:

My dataset is comprised of three main sources:

1. County and State population estimates from the U.S. Census
2. State level political data (state expenditures), partisan state legislative control, and state gubernatorial partisanship (various sources).
3. Industry makeup (proportion) of each county's jobs numbers, from the Bureau of Labor Statistics(BLS) Quarterly Census of Employment and Wages (QCEW).

Targets are computed from the QCEW as well.

The timeframes in question are from Q1 2000 to Q4 2006 for the first recession, and Q1 2007 to Q4 2019 for the second.

See full data dictionary for further descriptions and sources.

### Necessary Sacrifices:

Not every county made it into the dataset. A scattered handful did not have data for one of the other time period. Additionally, the State of Alaska had some reclassification of their counties and corresponding area_fips codes.
The QCEW also contains job numbers for multi-county, undefined, and out-of-state. These are marginal numbers and their precise definitons elude me, so I've dropped them.
Legislative control and budget data was not readily available for the District of Columbia, Puerto Rico, The U.S Virgin Islands, or Guam, and this data is excluded.
All cities, MicroSAs, and similar statistical designations are excluded, as they often straddle state lines.

My original plan was to use the timeline data to compute *how long* each county took to recover (in quarters)- but I could not consistently get my code to return the correct results. At this point I shifted the target from # of quarters to the delta between the job "peak" before and after the recession.

### Missing Data

Due to reclassification of some industries in 2005, the QCEW created some new industry classifcations. This resulted in a good deal of industry codes with nans for the 2001 recession data. I filled them with zeros to prevent those counties from being dropped as well.

## Exploratory Data Analysis:

[put maps here]

Initial exploration of the data showed some counter-intuitive results. Despite the 2008 recession being much deeper than 2001, there was considerably more time to recover before the next recession (12 years vs. only 6). However the 2008 recession showed slightly recovery rates than 2001. Additionally the distribution is roughly normal, save a Loving County Texas here or there.

<style type="text/css">
.tg  {border-collapse:collapse;border-color:#93a1a1;border-spacing:0;}
.tg td{background-color:#fdf6e3;border-color:#93a1a1;border-style:solid;border-width:1px;color:#002b36;
  font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{background-color:#657b83;border-color:#93a1a1;border-style:solid;border-width:1px;color:#fdf6e3;
  font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-ezbu{background-color:#eee8d5;border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
.tg .tg-fymr{border-color:inherit;font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-d421{background-color:#eee8d5;border-color:inherit;font-style:italic;text-align:left;vertical-align:top}
.tg .tg-f8tv{border-color:inherit;font-style:italic;text-align:left;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-0pky"></th>
    <th class="tg-fymr">2001</th>
    <th class="tg-fymr">2008</th>
    <th class="tg-fymr">Both</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-d421">n</td>
    <td class="tg-ezbu">3264</td>
    <td class="tg-ezbu">3257</td>
    <td class="tg-ezbu">6521</td>
  </tr>
  <tr>
    <td class="tg-f8tv">% Recovered</td>
    <td class="tg-c3ow">62%<br></td>
    <td class="tg-c3ow">52%</td>
    <td class="tg-c3ow">57%</td>
  </tr>
  <tr>
    <td class="tg-d421">Mean</td>
    <td class="tg-ezbu">0.05</td>
    <td class="tg-ezbu">0.06</td>
    <td class="tg-ezbu">0.05</td>
  </tr>
  <tr>
    <td class="tg-f8tv">St. Dev</td>
    <td class="tg-c3ow">0.58</td>
    <td class="tg-c3ow">0.62</td>
    <td class="tg-c3ow">0.60<br></td>
  </tr>
  <tr>
    <td class="tg-d421">Min</td>
    <td class="tg-ezbu">-3.68</td>
    <td class="tg-ezbu">-1.42</td>
    <td class="tg-ezbu">-3.68</td>
  </tr>
  <tr>
    <td class="tg-f8tv">25%</td>
    <td class="tg-c3ow">-0.03</td>
    <td class="tg-c3ow">-0.05</td>
    <td class="tg-c3ow">-0.04</td>
  </tr>
  <tr>
    <td class="tg-d421">Median</td>
    <td class="tg-ezbu">0.02</td>
    <td class="tg-ezbu">0.01</td>
    <td class="tg-ezbu">0.01</td>
  </tr>
  <tr>
    <td class="tg-f8tv">75%</td>
    <td class="tg-c3ow">0.07</td>
    <td class="tg-c3ow">0.07</td>
    <td class="tg-c3ow">0.07</td>
  </tr>
  <tr>
    <td class="tg-d421">Max</td>
    <td class="tg-ezbu">28.19<br></td>
    <td class="tg-ezbu">29.67<br></td>
    <td class="tg-ezbu">29.67<br></td>
  </tr>
</tbody>
</table>

[insert maps and distplots here]


## Journey to a model:

My first task was to attempt some dimensionality reduction. I had about 2500 features in my dataset, and they were sparse, specific, and overlapping. I attempted Principal Component Analysis, getting my feature numbers down to 665 (with 85% of variance captured). SVD and NMF gave similar results, but PCA seemed to have the best variance capture.

To do some basic sanity checks on my PCA, I ran basic Logistic Regression models, and the accuracy score dipped from about 69% to 54%. I begin to use GridSearch to investigate which type of model to use, but I was not happy with the AUC scores I was getting. I dropped the PCA and got a good boost in model accuracy, so I started from scratch in GridSearch without any dimensionality reduction.

[put ROC curves here]

Around this time I discovered an issue with the data. Due to a mistake in indexing, most of the political data I had collected did not find its way to the final dataset. I had a dilemma here, I could remove the political data and proceed with only the industry and population data. This would, however, negate any reason to drop non-county datapoints(Cities and MicroSA) from my dataset. I would need to re-tune the models with nearly twice as much data. Or I could fix the problem and re-tune with the correct pollitical variables. I went with option 2.
