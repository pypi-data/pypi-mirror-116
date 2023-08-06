# Risk Tools
Documentation to be completed

## Installation
`pip install johnshopeetools`
## Sample Usage: dpd
```
from strategy_analysis import dpd
dpd = dpd.dpd() #initialize dpd class
df.groupby(['term']).apply(dpd.dpd_basic)
df.groupby(['term']).apply(dpd.dpd_checking)
```
## Sample Usage: prefilters
```
from strategy_analysis import prefilters
pf = prefilters.prefilters_v2(['R001','R002','R003','R004','R005','R006','R007','R008','R009','R010','R011','R012','R013','R014'])

df = pf2.decompose_reason_codes(df)
df = pf2.generate_hit_cols(df)
df.groupby(['user_type']).apply(pf2.rejection_rate,'R013')
```

## Sample Usage: presto connector
```
from pyhive import presto
conn=presto.connect('presto-secure.idata.shopeemobile.com',
                        catalog='hive',
                        username='jack.yangjy@seamoney.com',
                        password='&~ED17##irOt',
                        schema='shopee',
                        port='443',
                        protocol='https')
```

```
from strategy_analysis import getdata

query = """SELECT * FROM seamoney_reg_risk_anlys.regds_kredit_prod_id__application_credit_score_mega_activate LIMIT 10"""

getdata.run_shopee_presto(query, conn)
```