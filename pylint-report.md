Pylint:
```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:82:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:100:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:106:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:145:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:189:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:211:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:224:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:237:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:253:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:295:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:24:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:37:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module draw
draw.py:1:0: C0114: Missing module docstring (missing-module-docstring)
draw.py:5:0: C0103: Variable name "ITERATIONS" doesn't conform to snake_case naming style (invalid-name)
draw.py:10:8: C0103: Variable name "ITERATIONS" doesn't conform to snake_case naming style (invalid-name)
draw.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module drawings
drawings.py:1:0: C0114: Missing module docstring (missing-module-docstring)
drawings.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
drawings.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
drawings.py:88:0: C0116: Missing function or method docstring (missing-function-docstring)
drawings.py:126:0: C0116: Missing function or method docstring (missing-function-docstring)
drawings.py:154:0: C0116: Missing function or method docstring (missing-function-docstring)
drawings.py:182:0: C0116: Missing function or method docstring (missing-function-docstring)
drawings.py:207:0: C0116: Missing function or method docstring (missing-function-docstring)
drawings.py:219:0: C0116: Missing function or method docstring (missing-function-docstring)
drawings.py:260:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:53:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:64:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:101:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.77/10 (previous run: 8.75/10, +0.03)
```

### Pylint-huomautukset

**C0111 (missing-docstring)**

Pylint valittaa puuttuvista docstring-kommenteista. Näitä ei kuitenkaan käytetty kurssimateriaalissa. Ne on siis jätetty pois tästäkin projektista.


**C0103 (invalid-name)**

Pylint ilmoittaa tiedostossa `config.py` olevasta muuttujasta `secret_key`: 

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Pylintin mukaan tulisi se kirjoittaa isoilla kirjaimilla. Kurssilla kuitenkin käytettiin pieniä kirjaimia.