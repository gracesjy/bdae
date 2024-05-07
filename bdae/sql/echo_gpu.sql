SELECT * FROM table (
   apEval (
      NULL,
      'select 1.0 as no, ''AAAAAAAAAAAAAAAAAAAAA'' as name from dual',
      'pandasUtil:df_echo'))
