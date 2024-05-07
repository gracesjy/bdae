SELECT *
  FROM table(apTableEval(
   cursor(
   SELECT * FROM AAAA
   ),
   NULL,
   'XML',
   'PyPieChart:make_plot'))
