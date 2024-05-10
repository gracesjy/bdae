 SELECT *
      FROM table(apTableEval(
             cursor(select * from CONFUSION_MATRIX where model_name = 'SGDClassifier'),
             NULL,
            'SELECT TO_CLOB(NULL) IMG FROM dual',      
           'ConfusionMatrix:display'))
