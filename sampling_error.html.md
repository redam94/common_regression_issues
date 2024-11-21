# Sampling Error in Exogenous Variables
Matthew Reda

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

Error in exogenous variables—those not influenced by other variables in
a model—can significantly compromise the integrity of regression
analyses. When these variables are inaccurately measured and the errors
are not properly addressed, several issues may arise:

- **Attenuation Bias**: This occurs when sampling errors lead to biased
  and inconsistent parameter estimates, typically causing the estimated
  coefficients to be closer to zero than their true values (Bound,
  Brown, and Mathiowetz 2001).
- **Reduced Statistical Power**: Sampling errors increase the variance
  of estimators, making it more challenging to detect significant
  relationships between variables.  
- **Misleading Inferences**: Ignoring sampling errors can result in
  incorrect conclusions about the relationships between variables,
  potentially leading to flawed policy decisions or interpretations
  (Bound, Brown, and Mathiowetz 2001).

This website is dedicated to exploring the challenges posed by sampling
errors in exogenous variables within regression models. We provide
comprehensive insights into how these errors can distort results and
discuss effective strategies to mitigate their impact.

By understanding and addressing sampling errors in exogenous variables,
data scientists can enhance the validity and reliability of their
regression analyses.

## Survey Data

When analyzing survey data, it’s crucial to assess the precision of
population parameter estimates. This precision is influenced by factors
such as sample size, sampling design, and measurement error within the
survey data.

## Impact of Sampling Error on Regression Models

Incorporating imprecise measurements into regression models can lead to
biased and inconsistent coefficient estimates. This issue persists even
with unbiased sampling designs and accurate respondent answers. In
survey research, where sample sizes are often limited and sampling
designs complex, measurement errors can significantly affect the
precision of population parameter estimates.

<div id="exm-binary-outcome" class="theorem example">

<span class="theorem-title">**Example 1 (Sampling Error in a Binary
Outcome Variable)**</span> Consider a weekly survey involving
approximately 500 participants, selected randomly to represent the
general population. Participants are asked if they recall seeing a
specific brand’s advertisement, with data collected via phone and online
methods.

Assuming perfect recall accuracy, we aim to estimate the effect of
advertisement recall on the brand’s sales using a simple linear
regression model. To explore this, we can simulate three years of survey
data to analyze the relationship between advertisement recall and sales.

</div>

<div>

> **Helper Functions**
>
> ------------------------------------------------------------------------
>
> <a
> href="https://github.com/redam94/common_regression_issues/blob/main/common_regression_issues/sampling_error.py#L21"
> target="_blank" style="float:right; font-size:smaller">source</a>
>
> ### random_walk_awareness_model
>
> >      random_walk_awareness_model
> >                                   (periods:list|pandas.core.indexes.datetimes.
> >                                   DatetimeIndex|numpy.ndarray)
>
> <table>
> <colgroup>
> <col style="width: 9%" />
> <col style="width: 38%" />
> <col style="width: 52%" />
> </colgroup>
> <thead>
> <tr class="header">
> <th></th>
> <th><strong>Type</strong></th>
> <th><strong>Details</strong></th>
> </tr>
> </thead>
> <tbody>
> <tr class="odd">
> <td>periods</td>
> <td>list | pandas.core.indexes.datetimes.DatetimeIndex |
> numpy.ndarray</td>
> <td>Time periods to simulate</td>
> </tr>
> <tr class="even">
> <td><strong>Returns</strong></td>
> <td><strong>Model</strong></td>
> <td><strong>PyMC model for the random walk awareness model</strong></td>
> </tr>
> </tbody>
> </table>
>
> ``` python
> dates = pd.date_range(start='2021-01-01', periods=156, freq='W-MON')
> awareness_model = random_walk_awareness_model(dates)
> starting_awareness = 0.025
> logit_starting_awareness = np.log(starting_awareness/(1-starting_awareness))
> generative_model = pm.do(
>   awareness_model, 
>   {
>     'weekly_variation': .1, 
>     'initial_awareness': logit_starting_awareness,
>     'weekly_shock': .01
>   }
> )
> population_awareness = pm.draw(generative_model['awareness'], random_seed=23)
> population_awareness = xr.DataArray(
>   population_awareness,
>   dims=['Period'],
>   coords={'Period': dates}
> )
> ```
>
> ![](00_sampling_error_files/figure-commonmark/fig-population-awareness-output-1.png)
>
> ------------------------------------------------------------------------
>
> <a
> href="https://github.com/redam94/common_regression_issues/blob/main/common_regression_issues/sampling_error.py#L43"
> target="_blank" style="float:right; font-size:smaller">source</a>
>
> ### survey_obs_model
>
> >      survey_obs_model (population_awareness:xarray.core.dataarray.DataArray|py
> >                        tensor.tensor.variable.TensorVariable,
> >                        avg_weekly_participants:float=500.0, coords:dict=None,
> >                        model:pymc.model.core.Model=None)
>
> <table>
> <colgroup>
> <col style="width: 6%" />
> <col style="width: 25%" />
> <col style="width: 34%" />
> <col style="width: 34%" />
> </colgroup>
> <thead>
> <tr class="header">
> <th></th>
> <th><strong>Type</strong></th>
> <th><strong>Default</strong></th>
> <th><strong>Details</strong></th>
> </tr>
> </thead>
> <tbody>
> <tr class="odd">
> <td>population_awareness</td>
> <td>xarray.core.dataarray.DataArray |
> pytensor.tensor.variable.TensorVariable</td>
> <td></td>
> <td>Population awareness</td>
> </tr>
> <tr class="even">
> <td>avg_weekly_participants</td>
> <td>float</td>
> <td>500.0</td>
> <td>Average number of participants per week</td>
> </tr>
> <tr class="odd">
> <td>coords</td>
> <td>dict</td>
> <td>None</td>
> <td>Coordinates for the PyMC model</td>
> </tr>
> <tr class="even">
> <td>model</td>
> <td>Model</td>
> <td>None</td>
> <td>PyMC model to add the survey observation model</td>
> </tr>
> <tr class="odd">
> <td><strong>Returns</strong></td>
> <td><strong>Model</strong></td>
> <td></td>
> <td></td>
> </tr>
> </tbody>
> </table>
>
> ------------------------------------------------------------------------
>
> <a
> href="https://github.com/redam94/common_regression_issues/blob/main/common_regression_issues/sampling_error.py#L65"
> target="_blank" style="float:right; font-size:smaller">source</a>
>
> ### simulate_awareness_survey_data
>
> >      simulate_awareness_survey_data (start_date:str='2020-01-01',
> >                                      n_weeks:int=156,
> >                                      avg_weekly_participants:float=500.0,
> >                                      weekly_awareness_variation:float=0.08,
> >                                      starting_population_aware:float=0.025,
> >                                      weekly_shock:float=0.01,
> >                                      random_seed:int=42)
>
> <table>
> <colgroup>
> <col style="width: 6%" />
> <col style="width: 25%" />
> <col style="width: 34%" />
> <col style="width: 34%" />
> </colgroup>
> <thead>
> <tr class="header">
> <th></th>
> <th><strong>Type</strong></th>
> <th><strong>Default</strong></th>
> <th><strong>Details</strong></th>
> </tr>
> </thead>
> <tbody>
> <tr class="odd">
> <td>start_date</td>
> <td>str</td>
> <td>2020-01-01</td>
> <td>Start date of the survey data</td>
> </tr>
> <tr class="even">
> <td>n_weeks</td>
> <td>int</td>
> <td>156</td>
> <td>Number of weeks to simulate</td>
> </tr>
> <tr class="odd">
> <td>avg_weekly_participants</td>
> <td>float</td>
> <td>500.0</td>
> <td>Average number of participants per week</td>
> </tr>
> <tr class="even">
> <td>weekly_awareness_variation</td>
> <td>float</td>
> <td>0.08</td>
> <td>Std. dev. of gaussian inovations for weekly awareness</td>
> </tr>
> <tr class="odd">
> <td>starting_population_aware</td>
> <td>float</td>
> <td>0.025</td>
> <td>Starting population awareness</td>
> </tr>
> <tr class="even">
> <td>weekly_shock</td>
> <td>float</td>
> <td>0.01</td>
> <td>Std. dev. of gaussian noise for weekly deviation from random
> walk</td>
> </tr>
> <tr class="odd">
> <td>random_seed</td>
> <td>int</td>
> <td>42</td>
> <td>Random seed for reproducibility</td>
> </tr>
> <tr class="even">
> <td><strong>Returns</strong></td>
> <td><strong>Dataset</strong></td>
> <td></td>
> <td><strong>Simulated awareness survey data as an xarray
> dataset</strong></td>
> </tr>
> </tbody>
> </table>
>
> ------------------------------------------------------------------------
>
> <a
> href="https://github.com/redam94/common_regression_issues/blob/main/common_regression_issues/sampling_error.py#L94"
> target="_blank" style="float:right; font-size:smaller">source</a>
>
> ### plot_survey_sim_data
>
> >      plot_survey_sim_data (data:xarray.core.dataset.Dataset)
>
> <table>
> <colgroup>
> <col style="width: 9%" />
> <col style="width: 38%" />
> <col style="width: 52%" />
> </colgroup>
> <thead>
> <tr class="header">
> <th></th>
> <th><strong>Type</strong></th>
> <th><strong>Details</strong></th>
> </tr>
> </thead>
> <tbody>
> <tr class="odd">
> <td>data</td>
> <td>Dataset</td>
> <td>Simulated survey data must contain ‘awareness’ and
> ‘estimated_awareness’ variables</td>
> </tr>
> <tr class="even">
> <td><strong>Returns</strong></td>
> <td><strong>None</strong></td>
> <td><strong>Plot of the simulated survey data</strong></td>
> </tr>
> </tbody>
> </table>

</div>

## Simulation Approach

1.  **Data Generation**: Create a dataset representing weekly survey
    responses over three years, including variables for advertisement
    recall (binary) and corresponding sales figures.
2.  **Model Specification**: Define a linear regression model with sales
    as the dependent variable and advertisement recall as the
    independent variable.
3.  **Analysis**: Fit the model to the simulated data to assess the
    estimated effect of advertisement recall on sales.

#### Generate Survey Responses

``` python
trace = simulate_awareness_survey_data(random_seed=23)
plot_survey_sim_data(trace)
```

![](00_sampling_error_files/figure-commonmark/fig-survey-sim-data-output-1.png)

#### Generate Sales Data

The sales data is simulated using the following equation:

<span id="eq-sales">
$$
\begin{align\*}
log(S_t) &= \beta \text{pop\\awareness}\_t + \alpha + \varepsilon_t \\
\varepsilon_t &\sim \mathcal{N}(0, \sigma^2)
\end{align\*}
 \qquad(1)$$
</span>

Lets see if the true coeff *β* can be estimated using the simulated
data.

``` python
ACTUAL_AWARENESS_COEFF = 30
log_sales = trace.awareness*ACTUAL_AWARENESS_COEFF + 10 + np.random.normal(0, 0.03, trace.awareness.shape)
sales = np.exp(log_sales)
```

![](00_sampling_error_files/figure-commonmark/fig-simulated-sales-output-1.png)

### The naive model

Let’s try ignoring the data generation process and fit a simple linear
regression model to the data.

<div class="cell-output cell-output-display">

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<caption>OLS Regression Results</caption>
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Dep. Variable:</td>
<td>awareness</td>
<td data-quarto-table-cell-role="th">R-squared:</td>
<td>0.418</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Model:</td>
<td>OLS</td>
<td data-quarto-table-cell-role="th">Adj. R-squared:</td>
<td>0.414</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Method:</td>
<td>Least Squares</td>
<td data-quarto-table-cell-role="th">F-statistic:</td>
<td>113.0</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Date:</td>
<td>Tue, 19 Nov 2024</td>
<td data-quarto-table-cell-role="th">Prob (F-statistic):</td>
<td>3.91e-20</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Time:</td>
<td>22:38:07</td>
<td data-quarto-table-cell-role="th">Log-Likelihood:</td>
<td>135.42</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">No. Observations:</td>
<td>156</td>
<td data-quarto-table-cell-role="th">AIC:</td>
<td>-266.8</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Df Residuals:</td>
<td>154</td>
<td data-quarto-table-cell-role="th">BIC:</td>
<td>-260.7</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Df Model:</td>
<td>1</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Covariance Type:</td>
<td>HAC</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
</tbody>
</table>

OLS Regression Results

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td></td>
<td data-quarto-table-cell-role="th">coef</td>
<td data-quarto-table-cell-role="th">std err</td>
<td data-quarto-table-cell-role="th">z</td>
<td data-quarto-table-cell-role="th">P&gt;|z|</td>
<td data-quarto-table-cell-role="th">[0.025</td>
<td data-quarto-table-cell-role="th">0.975]</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">const</td>
<td>10.2477</td>
<td>0.018</td>
<td>566.284</td>
<td>0.000</td>
<td>10.212</td>
<td>10.283</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">estimated_awareness</td>
<td>12.2445</td>
<td>1.152</td>
<td>10.628</td>
<td>0.000</td>
<td>9.987</td>
<td>14.502</td>
</tr>
</tbody>
</table>

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Omnibus:</td>
<td>2.478</td>
<td data-quarto-table-cell-role="th">Durbin-Watson:</td>
<td>1.084</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Prob(Omnibus):</td>
<td>0.290</td>
<td data-quarto-table-cell-role="th">Jarque-Bera (JB):</td>
<td>2.377</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Skew:</td>
<td>0.233</td>
<td data-quarto-table-cell-role="th">Prob(JB):</td>
<td>0.305</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Kurtosis:</td>
<td>2.615</td>
<td data-quarto-table-cell-role="th">Cond. No.</td>
<td>142.</td>
</tr>
</tbody>
</table>

<br/><br/>Notes:<br/>[1] Standard Errors are heteroscedasticity and autocorrelation robust (HAC) using 1 lags and without small sample correction

</div>

We can see from the results in
<a href="#tbl-measurement-error" class="quarto-xref">Table 1</a> that
the estimated coefficient is biased. The true coefficient for the effect
of the populations ability to recall the brand’s advertisement on the
brand’s sales is 30. The estimated coefficient is much less.

### Next the simple moving average model

Let’s try a simple moving average model to see if we can improve the
estimate of the coefficient. We will ignore the data generation process
and take the moving average of the estimated awareness directly.

![](00_sampling_error_files/figure-commonmark/fig-mov-avg-awareness-1-output-1.png)

<div class="cell-output cell-output-display">

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<caption>OLS Regression Results</caption>
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Dep. Variable:</td>
<td>awareness</td>
<td data-quarto-table-cell-role="th">R-squared:</td>
<td>0.722</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Model:</td>
<td>OLS</td>
<td data-quarto-table-cell-role="th">Adj. R-squared:</td>
<td>0.721</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Method:</td>
<td>Least Squares</td>
<td data-quarto-table-cell-role="th">F-statistic:</td>
<td>328.0</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Date:</td>
<td>Tue, 19 Nov 2024</td>
<td data-quarto-table-cell-role="th">Prob (F-statistic):</td>
<td>1.39e-39</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Time:</td>
<td>22:38:19</td>
<td data-quarto-table-cell-role="th">Log-Likelihood:</td>
<td>192.34</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">No. Observations:</td>
<td>152</td>
<td data-quarto-table-cell-role="th">AIC:</td>
<td>-380.7</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Df Residuals:</td>
<td>150</td>
<td data-quarto-table-cell-role="th">BIC:</td>
<td>-374.6</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Df Model:</td>
<td>1</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Covariance Type:</td>
<td>HAC</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
</tbody>
</table>

OLS Regression Results

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td></td>
<td data-quarto-table-cell-role="th">coef</td>
<td data-quarto-table-cell-role="th">std err</td>
<td data-quarto-table-cell-role="th">z</td>
<td data-quarto-table-cell-role="th">P&gt;|z|</td>
<td data-quarto-table-cell-role="th">[0.025</td>
<td data-quarto-table-cell-role="th">0.975]</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">const</td>
<td>10.1037</td>
<td>0.016</td>
<td>634.219</td>
<td>0.000</td>
<td>10.072</td>
<td>10.135</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">estimated_awareness</td>
<td>22.9943</td>
<td>1.270</td>
<td>18.111</td>
<td>0.000</td>
<td>20.506</td>
<td>25.483</td>
</tr>
</tbody>
</table>

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Omnibus:</td>
<td>0.405</td>
<td data-quarto-table-cell-role="th">Durbin-Watson:</td>
<td>0.989</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Prob(Omnibus):</td>
<td>0.817</td>
<td data-quarto-table-cell-role="th">Jarque-Bera (JB):</td>
<td>0.371</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Skew:</td>
<td>0.119</td>
<td data-quarto-table-cell-role="th">Prob(JB):</td>
<td>0.831</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Kurtosis:</td>
<td>2.951</td>
<td data-quarto-table-cell-role="th">Cond. No.</td>
<td>209.</td>
</tr>
</tbody>
</table>

<br/><br/>Notes:<br/>[1] Standard Errors are heteroscedasticity and autocorrelation robust (HAC) using 1 lags and without small sample correction

</div>

We can see from
<a href="#tbl-moving-avg-model" class="quarto-xref">Table 2</a> that we
are doing better than the naive model. The estimated coefficient is
closer to the true coefficient. However, the estimated coefficient is
still biased.

### Moving Average (Correctly this time)

Let’s try a moving average model again, but this time we will take the
moving average of the number of survey participants and the number of
positive results before dividing each.

``` python
moving_sum_n_positive = trace.n_positive.rolling(Period=5).sum().shift(Period=-2)
moving_sum_n_participants = trace.n_survey_participants.rolling(Period=5).sum().shift(Period=-2)
moving_avg_awareness = moving_sum_n_positive/moving_sum_n_participants
```

![](00_sampling_error_files/figure-commonmark/fig-mov-avg-awareness-2-output-1.png)

<div class="cell-output cell-output-display">

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<caption>OLS Regression Results</caption>
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Dep. Variable:</td>
<td>awareness</td>
<td data-quarto-table-cell-role="th">R-squared:</td>
<td>0.721</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Model:</td>
<td>OLS</td>
<td data-quarto-table-cell-role="th">Adj. R-squared:</td>
<td>0.719</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Method:</td>
<td>Least Squares</td>
<td data-quarto-table-cell-role="th">F-statistic:</td>
<td>337.5</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Date:</td>
<td>Tue, 19 Nov 2024</td>
<td data-quarto-table-cell-role="th">Prob (F-statistic):</td>
<td>3.19e-40</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Time:</td>
<td>22:38:25</td>
<td data-quarto-table-cell-role="th">Log-Likelihood:</td>
<td>191.85</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">No. Observations:</td>
<td>152</td>
<td data-quarto-table-cell-role="th">AIC:</td>
<td>-379.7</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Df Residuals:</td>
<td>150</td>
<td data-quarto-table-cell-role="th">BIC:</td>
<td>-373.7</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Df Model:</td>
<td>1</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Covariance Type:</td>
<td>HAC</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
</tbody>
</table>

OLS Regression Results

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td></td>
<td data-quarto-table-cell-role="th">coef</td>
<td data-quarto-table-cell-role="th">std err</td>
<td data-quarto-table-cell-role="th">z</td>
<td data-quarto-table-cell-role="th">P&gt;|z|</td>
<td data-quarto-table-cell-role="th">[0.025</td>
<td data-quarto-table-cell-role="th">0.975]</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">const</td>
<td>10.1025</td>
<td>0.016</td>
<td>637.292</td>
<td>0.000</td>
<td>10.071</td>
<td>10.134</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Moving Avg Awareness</td>
<td>23.1316</td>
<td>1.259</td>
<td>18.370</td>
<td>0.000</td>
<td>20.664</td>
<td>25.600</td>
</tr>
</tbody>
</table>

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Omnibus:</td>
<td>0.594</td>
<td data-quarto-table-cell-role="th">Durbin-Watson:</td>
<td>0.980</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Prob(Omnibus):</td>
<td>0.743</td>
<td data-quarto-table-cell-role="th">Jarque-Bera (JB):</td>
<td>0.506</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Skew:</td>
<td>0.141</td>
<td data-quarto-table-cell-role="th">Prob(JB):</td>
<td>0.776</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Kurtosis:</td>
<td>2.982</td>
<td data-quarto-table-cell-role="th">Cond. No.</td>
<td>210.</td>
</tr>
</tbody>
</table>

<br/><br/>Notes:<br/>[1] Standard Errors are heteroscedasticity and autocorrelation robust (HAC) using 1 lags and without small sample correction

</div>

This model
(<a href="#tbl-corrected-moving-avg" class="quarto-xref">Table 3</a>) is
only slightly better than the simple moving average model. The estimated
coefficient is still biased.

### Latent Variable Model

Let us now try to first estimate the population level awareness using a
bayesian model and then use the estimated population level awareness in
the regression model.

``` python
dates = trace["Period"].values
awareness_model = random_walk_awareness_model(dates)

with awareness_model as survey_model:
    survey_obs_model(awareness_model['awareness'], avg_weekly_participants=500, coords={'Period': dates})
    
with pm.observe(
  pm.do(
    survey_model, 
    {'n_survey_participants': trace.n_survey_participants.values} # apply the number of survey participants
    ), 
  {'n_positive': trace.n_positive.values} # observe the number of positive responses
  ):
    obs_trace = pm.sample(random_seed=42)
```

![](00_sampling_error_files/figure-commonmark/fig-modeled-awareness-output-1.png)

<div class="cell-output cell-output-display">

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<caption>OLS Regression Results</caption>
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Dep. Variable:</td>
<td>awareness</td>
<td data-quarto-table-cell-role="th">R-squared:</td>
<td>0.838</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Model:</td>
<td>OLS</td>
<td data-quarto-table-cell-role="th">Adj. R-squared:</td>
<td>0.837</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Method:</td>
<td>Least Squares</td>
<td data-quarto-table-cell-role="th">F-statistic:</td>
<td>688.1</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Date:</td>
<td>Tue, 19 Nov 2024</td>
<td data-quarto-table-cell-role="th">Prob (F-statistic):</td>
<td>1.09e-58</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Time:</td>
<td>22:39:03</td>
<td data-quarto-table-cell-role="th">Log-Likelihood:</td>
<td>235.35</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">No. Observations:</td>
<td>156</td>
<td data-quarto-table-cell-role="th">AIC:</td>
<td>-466.7</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Df Residuals:</td>
<td>154</td>
<td data-quarto-table-cell-role="th">BIC:</td>
<td>-460.6</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Df Model:</td>
<td>1</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Covariance Type:</td>
<td>HAC</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
</tbody>
</table>

OLS Regression Results

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td></td>
<td data-quarto-table-cell-role="th">coef</td>
<td data-quarto-table-cell-role="th">std err</td>
<td data-quarto-table-cell-role="th">z</td>
<td data-quarto-table-cell-role="th">P&gt;|z|</td>
<td data-quarto-table-cell-role="th">[0.025</td>
<td data-quarto-table-cell-role="th">0.975]</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">const</td>
<td>10.0235</td>
<td>0.014</td>
<td>697.016</td>
<td>0.000</td>
<td>9.995</td>
<td>10.052</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">awareness</td>
<td>29.0012</td>
<td>1.106</td>
<td>26.232</td>
<td>0.000</td>
<td>26.834</td>
<td>31.168</td>
</tr>
</tbody>
</table>

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Omnibus:</td>
<td>2.140</td>
<td data-quarto-table-cell-role="th">Durbin-Watson:</td>
<td>1.175</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Prob(Omnibus):</td>
<td>0.343</td>
<td data-quarto-table-cell-role="th">Jarque-Bera (JB):</td>
<td>1.722</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Skew:</td>
<td>0.160</td>
<td data-quarto-table-cell-role="th">Prob(JB):</td>
<td>0.423</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Kurtosis:</td>
<td>3.404</td>
<td data-quarto-table-cell-role="th">Cond. No.</td>
<td>238.</td>
</tr>
</tbody>
</table>

<br/><br/>Notes:<br/>[1] Standard Errors are heteroscedasticity and autocorrelation robust (HAC) using 1 lags and without small sample correction

</div>

Compared to the previous models the Latent Variable Model is much better
at recovering the ground truth. While the estimated coefficient is still
biased (we haven’t removed all the measurement error), it is much closer
to the true coefficient, than the previous models. Given that the model
can be train quickly on the data and the estimated coefficient is much
closer to the true coefficient, using the latent model is a good choice.

### Using the true awareness

Finally, let’s see how well we can do if we use the true awareness in
the regression model. This is not likely to be possible in practice, but
it should provide a good comparison point.

<div class="cell-output cell-output-display">

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<caption>OLS Regression Results</caption>
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Dep. Variable:</td>
<td>awareness</td>
<td data-quarto-table-cell-role="th">R-squared:</td>
<td>0.946</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Model:</td>
<td>OLS</td>
<td data-quarto-table-cell-role="th">Adj. R-squared:</td>
<td>0.946</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Method:</td>
<td>Least Squares</td>
<td data-quarto-table-cell-role="th">F-statistic:</td>
<td>2938.</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Date:</td>
<td>Tue, 19 Nov 2024</td>
<td data-quarto-table-cell-role="th">Prob (F-statistic):</td>
<td>3.22e-102</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Time:</td>
<td>22:39:04</td>
<td data-quarto-table-cell-role="th">Log-Likelihood:</td>
<td>321.60</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">No. Observations:</td>
<td>156</td>
<td data-quarto-table-cell-role="th">AIC:</td>
<td>-639.2</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Df Residuals:</td>
<td>154</td>
<td data-quarto-table-cell-role="th">BIC:</td>
<td>-633.1</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Df Model:</td>
<td>1</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Covariance Type:</td>
<td>HAC</td>
<td data-quarto-table-cell-role="th"></td>
<td></td>
</tr>
</tbody>
</table>

OLS Regression Results

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td></td>
<td data-quarto-table-cell-role="th">coef</td>
<td data-quarto-table-cell-role="th">std err</td>
<td data-quarto-table-cell-role="th">z</td>
<td data-quarto-table-cell-role="th">P&gt;|z|</td>
<td data-quarto-table-cell-role="th">[0.025</td>
<td data-quarto-table-cell-role="th">0.975]</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">const</td>
<td>10.0014</td>
<td>0.008</td>
<td>1245.901</td>
<td>0.000</td>
<td>9.986</td>
<td>10.017</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">awareness</td>
<td>29.8593</td>
<td>0.551</td>
<td>54.205</td>
<td>0.000</td>
<td>28.780</td>
<td>30.939</td>
</tr>
</tbody>
</table>

<table class="simpletable do-not-create-environment cell"
data-quarto-postprocess="true">
<tbody>
<tr class="odd">
<td data-quarto-table-cell-role="th">Omnibus:</td>
<td>1.415</td>
<td data-quarto-table-cell-role="th">Durbin-Watson:</td>
<td>2.184</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Prob(Omnibus):</td>
<td>0.493</td>
<td data-quarto-table-cell-role="th">Jarque-Bera (JB):</td>
<td>1.363</td>
</tr>
<tr class="odd">
<td data-quarto-table-cell-role="th">Skew:</td>
<td>0.226</td>
<td data-quarto-table-cell-role="th">Prob(JB):</td>
<td>0.506</td>
</tr>
<tr class="even">
<td data-quarto-table-cell-role="th">Kurtosis:</td>
<td>2.924</td>
<td data-quarto-table-cell-role="th">Cond. No.</td>
<td>231.</td>
</tr>
</tbody>
</table>

<br/><br/>Notes:<br/>[1] Standard Errors are heteroscedasticity and autocorrelation robust (HAC) using 1 lags and without small sample correction

</div>

Here we see that not only is the estimate spot on, but the standard
error is also much lower than the other models. The better the measure
of the exogenous variable, the more precise the estimate of the
coefficient we can achieve.

<div id="refs" class="references csl-bib-body hanging-indent"
entry-spacing="0">

<div id="ref-Bound_Brown_Mathiowetz_2001" class="csl-entry">

Bound, John, Charles Brown, and Nancy Mathiowetz. 2001. “Measurement
Error in Survey Data.” In *Handbook of Econometrics*, 3705–3843.
<https://doi.org/10.1016/s1573-4412(01)05012-7>.

</div>

</div>