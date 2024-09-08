# Problem statement

```bash

>> The goal is to develop a portfolio optimization strategy using the given stock market data. This involves analyzing historical price trends, calculating key financial metrics, and applying Modern Portfolio Theory (MPT) to construct an efficient portfolio. The primary objectives are:

1 Identify trends in stock prices using moving averages and other technical indicators.
2 Calculate the volatility and risk associated with each stock.
3 Determine the correlation between different stocks to understand their relationships and potential diversification benefits.
4 Generate and evaluate a series of random portfolios to identify the optimal portfolio that maximizes the Sharpe ratio, balancing      risk and return effectively.
```



#First ill do in notebook expeeriment then ill convert it into  end to end project

## workflows
1. update config.yaml
2. update secrets.yaml(OP)
3. upadate params.yaml
4. update entity
5. update configuration manager in src config
6. update components 
7. update pipeline
8. update main.py
9. update the dvc.yaml
10. update the app.py


# how to run this project ?



###  Steps:

clone the repository

```bash
https://github.com/kadmanikanta/predictive_analytics.git
```


### step 1 - create environment after opening the respository

```bash 
conda create -n kidney stock -y
```
```bash
conda activate stock
```

### step 2 Install the requirements

```bash
pip install -r requirements.txt
```
