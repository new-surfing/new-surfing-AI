def filter_tech_articles(df, tech_word):
    
    def contains_tech_word(content, tech_word):
        content = content.lower()
        for word in tech_word:
            if word.lower() in content:
                return True
        return False

    filtered_df = df[df['origin_content'].apply(lambda x: contains_tech_word(x, tech_word))].reset_index(drop=True)
    
    return filtered_df

