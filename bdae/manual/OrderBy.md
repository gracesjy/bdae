### ORDER BY
```
select  A,B,C,D,E,F,G,H, trim(D) as version_number,
        nvl(LPAD(trim(regexp_substr(D, '[^.]+', 1, 1)),3,'0'),'000') AS Major,
        nvl(LPAD(trim(regexp_substr(D, '[^.]+', 1, 2)),3,'0'),'000') AS Minor, 
        nvl(LPAD(trim(regexp_substr(D, '[^.]+', 1, 3)),3,'0'),'000') AS Revision
        from TEST_RETURN
        ORDER BY Major asc, Minor asc, Revision ASC
```
