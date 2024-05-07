SELECT *
FROM table(apEval(
   NULL,
   'SELECT 1.0 ClusterNo, 1.0 Homogeneity, TO_CLOB(NULL) IMAGE FROM dual',
   'PANDAS:dbscan'))
