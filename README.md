## This application was created for fun and self-education
###### But if you find something useful I will be glad to share with you my pieces of knowledge

### Application _crypto_stat_
This part of the application was created for calculating profit/loss while crypto trading.
- all deals adding manually in the admin panel 
- editing of all coins price in admin panel too

![](https://github.com/DanilRusakov/monobank_stat/blob/main/crypto_stat/static/coin_stat.png)

### Application _mono_
This application was created for displaying deep statistic usage monobank 
- all transactions parsed from monobank API using celery
- user token adding manually in the admin panel
- for displaying all statistics using "chart js"


![](https://github.com/DanilRusakov/monobank_stat/blob/main/mono/static/transaction_stat.png)
![](https://github.com/DanilRusakov/monobank_stat/blob/main/mono/static/spend.png)

###How to start working with mono project
1. Install all requirements
2. Create superuser for django admin
3. Add token into mono->mono users
4. Run celery commands for parsing transactions from mono API 
(each command in a separate terminal window, simultaneously)

`celery -A monobank_stat worker -l INFO --pool=solo`

`celery -A monobank_stat beat -l INFO`
