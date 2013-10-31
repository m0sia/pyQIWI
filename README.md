QIWI python API
========

## Overview

Very basic QIWI python API

## Example

```python
# -*- coding: utf-8 -*-
import QIWI
import time
import os

user = "" #User Name
token = "" #Auth token. Unuqie for each auth device.
udid = "000000000000000" 

q = QIWI.QIWI(user,token,udid)
os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

print q.GetBalance()

for transaction in q.GetIncome("hour"):
	print "Time: %s Amount: %s Income: %s Comment: %s ID: %s" % (time.asctime(transaction.time), transaction.amount,transaction.income, transaction.comment, str(transaction.id))

```