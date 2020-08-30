# Predicting County Recession Recovery

<img src="/img/recession.jpeg" alt="Recession" style=" width:100%;"/>

Can we model which counties of the US are most likely to recover form the 2020 recession?

With the COVID-19 pandemic still active in the United States, millions of Americans are without work, and the economy remains in a precarious position. Additionally, since the start of the 21st century, the United States as spent only seven out of twenty years in a period of recession or recovery. With this project, I intend to model country-level economic performance (jobs) from the last two recessions, and predict which counties are most likely to recover from this recession in time for the next one.

## Definitions and Assumptions:

I will be considering only the raw number of jobs in any given county. A county will be defined as "recovered" if the number of jobs in any fiscal quarter after the recession event surpasses its peak before the event. I will not be taking into account population change, nor will I be considering if a single person holds more than one job.
The "recovery event" for both recessions (2001 & 2007) are in Q3 of 2001 and Q3 of 2008 (Sept. 11 and the 2008 housing price collapse). This does not necessarily correspond with the beginning of the official recession, but as these are the most dramatic periods of shift in the economy.
I will not be considering wages within the county, or the number of firms offering jobs (like I did last time).
All feature measures will be taken from the quarter of the recession event.

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

### 2001 Job Growth Map
<img src="/img/2001percap.png" alt="2001 Growth" style=" width:100%;"/>

### 2008 Job Growth Map
<img src="/img/2008percap.png" alt="2001 Growth" style=" width:100%;"/>

Initial exploration of the data showed some counter-intuitive results. Despite the 2008 recession being much deeper than 2001, there was considerably more time to recover before the next recession (12 years vs. only 6). However the 2008 recession showed slightly recovery rates than 2001. Additionally the distribution is roughly normal, save a Loving County Texas here or there.

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

### Job Growth Distribution
<img src="/img/distributions.png" alt="2001 Growth" style=" width:100%;"/>


## Journey to a model:

My first task was to attempt some dimensionality reduction. I had about 2500 features in my dataset, and they were sparse, specific, and overlapping. I attempted Principal Component Analysis, getting my feature numbers down to 665 (with 85% of variance captured). SVD and NMF gave similar results, but PCA seemed to have the best variance capture.

To do some basic sanity checks on my PCA, I ran basic Logistic Regression models, and the accuracy score dipped from about 69% to 54%. I begin to use GridSearch to investigate which type of model to use, but I was not happy with the AUC scores I was getting. I dropped the PCA and got a good boost in model accuracy, so I started from scratch in GridSearch without any dimensionality reduction.


Around this time I discovered an issue with the data. Due to a mistake in indexing, most of the political data I had collected did not find its way to the final dataset. I had a dilemma here, I could remove the political data and proceed with only the industry and population data. This would, however, negate any reason to drop non-county datapoints(Cities and MicroSA) from my dataset. I would need to re-tune the models with nearly twice as much data. Or I could fix the problem and re-tune with the correct political variables. I went with option 2.

After some serious GridSearch time, I managed to get both a Random Forest and Gradient Boost model working well enough. Since this situation does not really favor prescision over recall, I used f1 as my metric for evaluating the model.

(See appendix for GridSearch records)

I also decided to use the model hyperparameters on the Regeressor versions of the three best-performing models, to see if I could also predict the change in jobs (rather than just whether a county would recover).

<table class="tg">
<thead>
  <tr>
    <th class="tg-jo73"></th>
    <th class="tg-cvjw">AUC</th>
    <th class="tg-cvjw">Accuracy</th>
    <th class="tg-cvjw">Precision</th>
    <th class="tg-cvjw">Recall</th>
    <th class="tg-cvjw">f1</th>
    <th class="tg-cvjw">r**2</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-8385">Decision Tree</td>
    <td class="tg-rai2">.63</td>
    <td class="tg-rai2">.60</td>
    <td class="tg-rai2">.79</td>
    <td class="tg-rai2">.41</td>
    <td class="tg-rai2">.54</td>
    <td class="tg-rai2">.13</td>
  </tr>
  <tr>
    <td class="tg-d0s8">Random Forest</td>
    <td class="tg-gegp">.65</td>
    <td class="tg-gegp">.67</td>
    <td class="tg-gegp">.70</td>
    <td class="tg-gegp">.73</td>
    <td class="tg-gegp">.71</td>
    <td class="tg-gegp">.33</td>
  </tr>
  <tr>
    <td class="tg-qpy6">Gradient Boost</td>
    <td class="tg-k0nx">.66</td>
    <td class="tg-k0nx">.67</td>
    <td class="tg-k0nx">.71</td>
    <td class="tg-k0nx">.71</td>
    <td class="tg-k0nx">.71</td>
    <td class="tg-k0nx">.46</td>
  </tr>
  <tr>
    <td class="tg-zlpz">XG Boost</td>
    <td class="tg-wqgo"></td>
    <td class="tg-wqgo"></td>
    <td class="tg-wqgo"></td>
    <td class="tg-wqgo"></td>
    <td class="tg-wqgo"></td>
    <td class="tg-wqgo"></td>
  </tr>
  <tr>
    <td class="tg-1mhx">Bernoulli NB</td>
    <td class="tg-bk7u">.58</td>
    <td class="tg-bk7u">.54</td>
    <td class="tg-bk7u">.72</td>
    <td class="tg-bk7u">.33</td>
    <td class="tg-bk7u">.46</td>
    <td class="tg-bk7u"></td>
  </tr>
  <tr>
    <td class="tg-bt07">Complement NB</td>
    <td class="tg-1uui">.48</td>
    <td class="tg-1uui">.52</td>
    <td class="tg-1uui">.56</td>
    <td class="tg-1uui">.75</td>
    <td class="tg-1uui">.63</td>
    <td class="tg-1uui"></td>
  </tr>
  <tr>
    <td class="tg-u7jh">Gaussian NB</td>
    <td class="tg-487o">.52</td>
    <td class="tg-487o">.45</td>
    <td class="tg-487o">.85</td>
    <td class="tg-487o">.05</td>
    <td class="tg-487o">.10</td>
    <td class="tg-487o"></td>
  </tr>
  <tr>
    <td class="tg-ynie">Multinomial NB</td>
    <td class="tg-9jwl">.48</td>
    <td class="tg-9jwl">.52</td>
    <td class="tg-9jwl">.56</td>
    <td class="tg-9jwl">.75</td>
    <td class="tg-9jwl">.64</td>
    <td class="tg-9jwl"></td>
  </tr>
</tbody>
</table>

### Confusion Matrices

<img src="/img/dtc.png" alt="Decision Tree" style=" width:25%;"/><img src="/img/rfc.png" alt="Random Forest" style=" width:25%;"/><img src="/img/gbc.png" alt="Gradient Boost" style=" width:25%;"/>

<img src="/img/bnc.png" alt="Bernoulli NB" style=" width:25%;"/><img src="/img/gnb.png" alt="Gaussian NB" style=" width:25%;"/><img src="/img/cnb.png" alt="Complement NB" style=" width:25%;"/><img src="/img/mnb.png" alt="Mulitnomial NB" style=" width:25%;"/>

Naive Bayes didn't pay off for me (neither did a Dense Multilayer Percpitron network), so I didn't spend too much time tuning them. After a long night, I landed on some optimal parameters.

While for the classifiers, Random Forest performed the best, but not by much (the f1 score difference is lost in the rounding), but the r2 score is much better from Gradient Boosting, which gives it the advantage.

### Feature Importance

Feature importance is not really key to my goal of predicting the outcome of this recession, but there is a great deal of data excluded for lack of political data. The only political data that shows up high in the feature importance of any model is the State Expenditures- removing it from future research will have minimal impact and allow me to include the excluded data to train future models.

## Results:

### 2020 Recession Likelihood of Recovery

<img src="/img/2020_prediction.png" alt="2020 Prediction" style=" width:100%;"/>


## Future Steps:

I'm exited to work more with this data, and will be doing so in the future. Here is a list of possible avenues to continue this research:

1. Solve the "time to recover" problem, and produce a model to predict that.
2. Update the prediction data with 2020 population/industry.
3. Run the models using monthly rather than quarterly data, whicb might provide additional insight.
4. Run the models on *wages* rather than raw job numbers.
5. Use Flask to make a "report card" on a given area, showing its history and forecast for the future.
