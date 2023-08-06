# Sqlalchemy Sqlite Session

This is tools to get session and engine for Sqlalchemy Sqlite. 


### install package
``` 
pip install sqlalchemy-sqlite-session 
```

### example
```
from sqlalchemy_sqlite_session.adapters import get_sqlite_session

session = get_sqlite_session('C:\sqlite_path.db')

engine = get_sqlite_engine('C:\sqlite_path.db')

```