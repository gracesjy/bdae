SELECT *
FROM table(apEval(
   NULL,
   'XML',
   'chart_3d_surface:make_plot'))
