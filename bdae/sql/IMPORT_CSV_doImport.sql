# First of All
# execute
# 

# SELECT *
# FROM table(apEval(
#   cursor(
#      SELECT 
#            '/home/oracle/breast_cancer.csv' FILENAME 
#      FROM dual),
#   'SELECT CAST(''A'' AS VARCHAR2(40)) SUBJECT, CAST(''A'' AS VARCHAR2(40)) SQL_COLUMN FROM dual',
#  'IMPORT_CSV:getColumns'));

# --- and then ... make output SQL using above second column list, ..

SELECT *
FROM table(apEval(
   cursor(
      SELECT 
            '/home/oracle/breast_cancer.csv' FILENAME 
      FROM dual),
   'SELECT 
    1.0 mean_radius,
    1.0 mean_texture,
    1.0 mean_perimeter,
    1.0 mean_area,
    1.0 mean_smoothness,
    1.0 mean_compactness,
    1.0 mean_concavity,
    1.0 mean_concave_points,
    1.0 mean_symmetry,
    1.0 mean_fractal_dimension,
    1.0 radius_error,
    1.0 texture_error,
    1.0 perimeter_error,
    1.0 area_error,
    1.0 smoothness_error,
    1.0 compactness_error,
    1.0 concavity_error,
    1.0 concave_points_error,
    1.0 symmetry_error,
    1.0 fractal_dimension_error,
    1.0 worst_radius,
    1.0 worst_texture,
    1.0 worst_perimeter,
    1.0 worst_area,
    1.0 worst_smoothness,
    1.0 worst_compactness,
    1.0 worst_concavity,
    1.0 worst_concave_points,
    1.0 worst_symmetry,
    1.0 worst_fractal_dimension,
    1 class
   FROM dual',
   'IMPORT_CSV:doImport')) ;
