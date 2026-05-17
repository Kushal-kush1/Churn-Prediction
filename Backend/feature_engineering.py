def feature_eng(X):
    """
    Performs feature engineering by creating an 'AgeGroup' feature 
    from the 'Age' column.

    The age is categorized into:
    - Youth (18–40)
    - Adult (41–60)
    - Senior (60+)

    Returns:
    - Transformed DataFrame with new 'AgeGroup' column
    """
    x=X.copy()
    def mapping(age):
        if age>=18 and age <=40:
            return 'Youth'
        elif age>=41 and age<=60:
            return 'Adult'
        else :
            return 'Senior'
    x['Age_group']= x['Age'].apply(mapping)
    return x 