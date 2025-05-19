import nltk
# Ensure NLTK resources are available (run once)
try:
    nltk.data.find('tokenizers/punkt')
    print("NLTK 'punkt' resource found.")
except LookupError:
    print("NLTK 'punkt' resource not found. Downloading...")
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
    print("NLTK 'stopwords' resource found.")
except LookupError:
    print("NLTK 'stopwords' resource not found. Downloading...")
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
    print("NLTK 'wordnet' resource found.")
except LookupError:
    print("NLTK 'wordnet' resource not found. Downloading...")
    nltk.download('wordnet')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
    print("NLTK 'averaged_perceptron_tagger' resource found.")
except LookupError:
    print("NLTK 'averaged_perceptron_tagger' resource not found. Downloading...")
    nltk.download('averaged_perceptron_tagger')
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
    print("NLTK 'vader_lexicon' resource found.")
except LookupError:
    try:
        nltk.data.find('sentiment/vader_lexicon')
        print("NLTK 'vader_lexicon' resource found.")
    except LookupError:
        print("NLTK 'vader_lexicon' resource not found. Downloading...")
        nltk.download('vader_lexicon')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os # Import os earlier

# --- Configuration ---
CSV_FILE_PATH = '/Users/akshaypulla/Desktop/GroMo/gromo_play_store_reviews_detailed.csv'
FILTER_FUTURE_DATES = True
FUTURE_DATE_THRESHOLD = pd.Timestamp.now() + pd.Timedelta(days=1)

# --- Load and Basic Preprocessing ---
print(f"Loading data from {CSV_FILE_PATH}...")
try:
    df = pd.read_csv(CSV_FILE_PATH)
except FileNotFoundError:
    print(f"Error: File not found at {CSV_FILE_PATH}. Please check the path.")
    exit()

print("Initial DataFrame Info:")
df.info()
print("\nFirst 5 rows:")
print(df.head())

df['Review_Date'] = pd.to_datetime(df['Review_Date'], errors='coerce')

original_row_count = len(df)
if FILTER_FUTURE_DATES:
    future_dates_mask = df['Review_Date'] > FUTURE_DATE_THRESHOLD
    num_future_dates = future_dates_mask.sum()
    if num_future_dates > 0:
        print(f"\nWarning: Found {num_future_dates} reviews with dates beyond {FUTURE_DATE_THRESHOLD}.")
        df = df[~future_dates_mask].copy()
        print(f"Filtered out {num_future_dates} rows with future dates. New row count: {len(df)}")

df.dropna(subset=['Review_Date'], inplace=True)
print(f"Rows after handling date issues: {len(df)}")

df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df.dropna(subset=['Rating'], inplace=True)
df['Rating'] = df['Rating'].astype(int)

# --- 1. Rating Distribution ---
print("\n--- 1. Rating Distribution ---")
plt.figure(figsize=(8, 6))
# For Seaborn v0.14.0+ warnings:
# sns.countplot(x='Rating', data=df, hue='Rating', palette='viridis', order=sorted(df['Rating'].unique()), legend=False)
sns.countplot(x='Rating', data=df, palette='viridis', order=sorted(df['Rating'].unique()))
plt.title('Distribution of GroMo Partner Ratings')
plt.xlabel('Rating (Stars)')
plt.ylabel('Number of Reviews')
plt.grid(axis='y', linestyle='--')
plt.savefig('rating_distribution.png')

average_rating = df['Rating'].mean()
print(f"Average Rating: {average_rating:.2f} stars")

# --- 2. Review Volume Over Time ---
print("\n--- 2. Review Volume Over Time ---")
df_time = df.set_index('Review_Date').copy()
# reviews_per_month = df_time['Rating'].resample('M').count() # Old
reviews_per_month = df_time['Rating'].resample('ME').count() # New: 'ME' for Month End

if not reviews_per_month.empty and len(reviews_per_month) > 1:
    plt.figure(figsize=(12, 6))
    reviews_per_month.plot(kind='line', marker='o')
    plt.title('Number of GroMo Partner Reviews Over Time (Monthly)')
    plt.xlabel('Month')
    plt.ylabel('Number of Reviews')
    plt.grid(True)
    plt.savefig('reviews_over_time.png')
else:
    print("Not enough data points or time range for monthly review volume plot after date filtering.")

# --- 3. Average Rating Over Time ---
print("\n--- 3. Average Rating Over Time ---")
# average_rating_per_month = df_time['Rating'].resample('M').mean() # Old
average_rating_per_month = df_time['Rating'].resample('ME').mean() # New: 'ME' for Month End

if not average_rating_per_month.empty and len(average_rating_per_month) > 1:
    plt.figure(figsize=(12, 6))
    average_rating_per_month.plot(kind='line', marker='o', color='green')
    plt.title('Average GroMo Partner Rating Over Time (Monthly)')
    plt.xlabel('Month')
    plt.ylabel('Average Rating')
    plt.ylim(1, 5)
    plt.grid(True)
    plt.axhline(average_rating, color='red', linestyle='--', label=f'Overall Avg ({average_rating:.2f})')
    plt.legend()
    plt.savefig('average_rating_over_time.png')
else:
    print("Not enough data points or time range for monthly average rating plot after date filtering.")

# --- 4. Text Preprocessing ---
print("\n--- 4. Text Preprocessing ---")
stop_words_list = stopwords.words('english')
custom_stopwords_list = ['gromo', 'app', 'application', 'please', 'also', 'get', 'even', 'would', 'could', 'make']
stop_words_set = set(stop_words_list + custom_stopwords_list)

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    if pd.isna(text): return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words_set and len(word) > 2]
    return " ".join(tokens)

if 'Review_Message' in df.columns:
    print("Preprocessing review messages...")
    df['Processed_Message'] = df['Review_Message'].apply(preprocess_text)
    print("Text preprocessing complete.")
    print(df[['Review_Message', 'Processed_Message']].head())
    if isinstance(df_time.index, pd.DatetimeIndex) and not df_time.empty:
        # df_time is already indexed by 'Review_Date'. We need to ensure 'Processed_Message' from 'df' (with its original index)
        # is correctly aligned to 'df_time'.
        # We can do this by setting 'Review_Date' as index on 'df' temporarily for this assignment.
        temp_df_for_merge = df.set_index('Review_Date')
        df_time['Processed_Message'] = temp_df_for_merge['Processed_Message']
        # Verify alignment (optional, for debugging)
        # print("df_time head after adding Processed_Message:")
        # print(df_time.head())
    else:
        print("Warning: df_time is not properly set up with DatetimeIndex. Cannot assign 'Processed_Message'.")
else:
    print("Error: 'Review_Message' column not found. Cannot perform text analysis.")
    df['Processed_Message'] = ""
    if 'Processed_Message' not in df_time.columns: # ensure df_time gets an empty column too if base df does
        df_time['Processed_Message'] = ""


# --- 5. Most Common Words/Phrases (N-grams) ---
def plot_top_ngrams(corpus, title, ngram_range=(1,1), top_n=20, filename='top_ngrams.png'):
    if not corpus.empty and corpus.str.strip().any():
        try:
            vec = CountVectorizer(ngram_range=ngram_range, stop_words=list(stop_words_set)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
            words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)

            if not words_freq:
                print(f"No n-grams found for '{title}' after vectorization.")
                return

            top_df = pd.DataFrame(words_freq[:top_n], columns=['Ngram', 'Frequency'])
            plt.figure(figsize=(12, 8))
            # For Seaborn v0.14.0+ warnings:
            # sns.barplot(x='Frequency', y='Ngram', data=top_df, hue='Ngram', palette='mako', legend=False)
            sns.barplot(x='Frequency', y='Ngram', data=top_df, palette='mako')
            plt.title(title)
            plt.tight_layout()
            plt.savefig(filename)
        except ValueError as e:
            print(f"Could not generate n-grams for '{title}': {e}.")
    else:
        print(f"Corpus for '{title}' is empty or contains only whitespace. Skipping n-gram plot.")

if 'Processed_Message' in df.columns:
    print("\n--- 5. Most Common Words/Phrases (N-grams) ---")
    negative_reviews_text = df[df['Rating'] <= 2]['Processed_Message'].dropna()
    plot_top_ngrams(negative_reviews_text, 'Top Unigrams in Negative Reviews (1-2 Stars)', ngram_range=(1,1), filename='top_unigrams_negative.png')
    plot_top_ngrams(negative_reviews_text, 'Top Bigrams in Negative Reviews (1-2 Stars)', ngram_range=(2,2), filename='top_bigrams_negative.png')
    plot_top_ngrams(negative_reviews_text, 'Top Trigrams in Negative Reviews (1-2 Stars)', ngram_range=(3,3), filename='top_trigrams_negative.png')

    if not negative_reviews_text.empty:
        all_negative_text = " ".join(review for review in negative_reviews_text if review.strip())
        if all_negative_text.strip():
            wordcloud = WordCloud(stopwords=stop_words_set, background_color="white", width=800, height=400, collocations=False).generate(all_negative_text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.title('Word Cloud for Negative Reviews (1-2 Stars)')
            plt.savefig('wordcloud_negative_reviews.png')
        else:
            print("No text available for negative review word cloud after processing.")
    else:
        print("No negative reviews found for word cloud.")
else:
    print("Skipping N-gram analysis as 'Processed_Message' is not available.")

# --- 6. Sentiment Analysis (VADER) ---
print("\n--- 6. Sentiment Analysis (VADER) ---")
if 'Review_Message' in df.columns:
    analyzer = SentimentIntensityAnalyzer()
    df['VADER_Sentiment_Compound'] = df['Review_Message'].astype(str).apply(lambda x: analyzer.polarity_scores(x)['compound'])
    def categorize_sentiment(compound_score):
        if compound_score >= 0.05: return 'Positive'
        elif compound_score <= -0.05: return 'Negative'
        else: return 'Neutral'
    df['VADER_Sentiment_Label'] = df['VADER_Sentiment_Compound'].apply(categorize_sentiment)
    print(df[['Rating', 'Review_Message', 'VADER_Sentiment_Compound', 'VADER_Sentiment_Label']].head())

    plt.figure(figsize=(8, 6))
    # For Seaborn v0.14.0+ warnings:
    # sns.countplot(x='VADER_Sentiment_Label', data=df, hue='VADER_Sentiment_Label', palette='coolwarm', order=['Positive', 'Neutral', 'Negative'], legend=False)
    sns.countplot(x='VADER_Sentiment_Label', data=df, palette='coolwarm', order=['Positive', 'Neutral', 'Negative'])
    plt.title('Sentiment Distribution of Reviews (VADER)')
    plt.savefig('vader_sentiment_distribution.png')

    plt.figure(figsize=(10, 7))
    # For Seaborn v0.14.0+ warnings:
    # sns.boxplot(x='Rating', y='VADER_Sentiment_Compound', data=df, hue='Rating', palette='viridis', legend=False)
    sns.boxplot(x='Rating', y='VADER_Sentiment_Compound', data=df, palette='viridis')
    plt.title('VADER Sentiment Compound Score vs. Star Rating')
    plt.savefig('vader_vs_star_rating.png')
else:
    print("Skipping VADER sentiment analysis as 'Review_Message' is not available.")

# --- 7. Developer Engagement Analysis ---
print("\n--- 7. Developer Engagement Analysis ---")
if 'Has_Developer_Reply' in df.columns:
    if df['Has_Developer_Reply'].dtype == 'object':
        df['Has_Developer_Reply'] = df['Has_Developer_Reply'].map({'Yes': True, 'No': False, True: True, False: False}).fillna(False)
    reply_counts = df['Has_Developer_Reply'].value_counts(normalize=True) * 100
    print("Percentage of Reviews with Developer Reply:")
    print(reply_counts)
    if not reply_counts.empty:
        plt.figure(figsize=(7, 5))
        # For Seaborn v0.14.0+ warnings:
        # sns.barplot(x=reply_counts.index.astype(str), y=reply_counts.values, hue=reply_counts.index.astype(str), palette=['lightcoral', 'lightgreen'], legend=False)
        sns.barplot(x=reply_counts.index, y=reply_counts.values, palette=['lightcoral', 'lightgreen'])
        plt.title('Developer Reply Rate')
        plt.xlabel('Has Developer Reply?')
        plt.ylabel('Percentage of Reviews')
        reply_index_labels = ['No Reply' if idx == False else 'Has Reply' for idx in reply_counts.index]
        plt.xticks(ticks=range(len(reply_counts.index)), labels=reply_index_labels)
        plt.savefig('developer_reply_rate.png')

    reply_rate_by_rating = df.groupby('Rating')['Has_Developer_Reply'].mean() * 100
    if not reply_rate_by_rating.empty:
        plt.figure(figsize=(10, 6))
        reply_rate_by_rating.plot(kind='bar', color='skyblue')
        plt.title('Developer Reply Rate by Star Rating')
        plt.xlabel('Star Rating')
        plt.ylabel('Percentage of Reviews with Reply (%)')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--')
        plt.savefig('developer_reply_rate_by_rating.png')
else:
    print("Skipping Developer Engagement analysis as 'Has_Developer_Reply' is not available.")

# --- 8. PAIN POINT ANALYSIS OVER TIME ---
print("\n--- 8. Pain Point Analysis Over Time ---")

# Corrected condition for starting pain point analysis
# df_time must exist, be indexed by Datetime, and have 'Processed_Message'
if ('df_time' in locals() and isinstance(df_time.index, pd.DatetimeIndex) and
    'Processed_Message' in df_time.columns and 'Processed_Message' in df.columns):

    pain_point_keywords = {
        'payment_issues': ['payment', 'payout', 'withdrawal', 'withdraw', 'money', 'amount', 'transaction', 'upi', 'bank', 'credit', 'stuck', 'pending', 'failed', 'delay'],
        'customer_support': ['support', 'customer', 'care', 'service', 'helpline', 'help', 'response', 'reply', 'contact', 'call', 'resolve', 'query', 'agent', 'representative', 'team', 'executive'],
        'app_performance': ['slow', 'lag', 'crash', 'bug', 'hang', 'error', 'freeze', 'stuck', 'loading', 'performance', 'issue', 'problem', 'working', 'opening', 'interface', 'ui', 'ux', 'navigation', 'update'],
        'commission_earnings': ['commission', 'earning', 'income', 'incentive', 'rate', 'percentage', 'profit', 'benefit', 'referral', 'amount', 'low', 'less'],
        'account_kyc': ['kyc', 'account', 'verification', 'document', 'profile', 'activation', 'login', 'register', 'block', 'suspend', 'otp', 'number', 'issue'],
        'product_info_training': ['product', 'training', 'information', 'detail', 'knowledge', 'misleading', 'understand', 'learn', 'guidance', 'policy', 'explain', 'video', 'material'],
        'lead_issues': ['lead', 'client', 'customer', 'conversion', 'fake', 'genuine', 'interest', 'quality', 'generate', 'provide']
    }

    pain_point_plot_dir = "pain_point_plots"
    if not os.path.exists(pain_point_plot_dir):
        os.makedirs(pain_point_plot_dir)

    for category, keywords in pain_point_keywords.items():
        print(f"\nAnalyzing pain point: {category.replace('_', ' ').title()}...")
        pattern = r'\b(' + '|'.join(keywords) + r')\b'

        # Ensure 'Processed_Message' is not all NaN or empty strings in df_time, which can happen if it wasn't populated correctly
        if df_time['Processed_Message'].isna().all() or not df_time['Processed_Message'].str.strip().any():
            print(f"  Warning: 'Processed_Message' in df_time is empty or all NaN for {category}. Skipping trend.")
            df[f'mentions_{category}'] = False # Still create the column in df for consistency, but all False
            if f'mentions_{category}' not in df_time.columns:
                df_time[f'mentions_{category}'] = False
            continue

        # Apply pattern to df for initial identification and counts (on original df)
        df[f'mentions_{category}'] = df['Processed_Message'].str.contains(pattern, case=False, na=False)
        # Apply pattern to df_time for time-series analysis
        df_time[f'mentions_{category}'] = df_time['Processed_Message'].str.contains(pattern, case=False, na=False)


        pain_point_reviews_df = df[df[f'mentions_{category}']]
        total_mentions = pain_point_reviews_df.shape[0]

        if total_mentions > 0:
            first_occurrence_date = pain_point_reviews_df['Review_Date'].min()
            print(f"  First noted: {first_occurrence_date.strftime('%Y-%m-%d') if pd.notnull(first_occurrence_date) else 'N/A'}")
            print(f"  Total mentions: {total_mentions}")

            # monthly_total_reviews = df_time['Rating'].resample('M').count() # Old
            # monthly_pain_point_mentions = df_time[df_time[f'mentions_{category}'] == True][f'mentions_{category}'].resample('M').count() # Old

            monthly_total_reviews = df_time['Rating'].resample('ME').count() # New
            monthly_pain_point_mentions = df_time[df_time[f'mentions_{category}'] == True][f'mentions_{category}'].resample('ME').count() # New


            monthly_pain_point_mentions = monthly_pain_point_mentions.reindex(monthly_total_reviews.index, fill_value=0)
            monthly_frequency_percent = (monthly_pain_point_mentions / monthly_total_reviews * 100).fillna(0)

            if not monthly_frequency_percent.empty and len(monthly_frequency_percent) > 1:
                plt.figure(figsize=(12, 6))
                monthly_frequency_percent.plot(kind='line', marker='o')
                plt.title(f"Monthly Frequency of '{category.replace('_', ' ').title()}' Mentions")
                plt.xlabel('Month')
                plt.ylabel('% of Reviews Mentioning Pain Point')
                plt.grid(True)
                plt.ylim(bottom=0)
                plot_filename = os.path.join(pain_point_plot_dir, f'trend_{category}.png')
                plt.savefig(plot_filename)
                print(f"  Trend plot saved to {plot_filename}")
            else:
                print(f"  Not enough data points or time range to plot monthly trend for '{category}'.")
        else:
            print(f"  No reviews found mentioning keywords for '{category}'.")
else:
    print("Skipping Pain Point Analysis due to missing data or incorrect setup:")
    if 'df_time' not in locals():
        print("  - 'df_time' DataFrame not defined.")
    elif not isinstance(df_time.index, pd.DatetimeIndex):
        print("  - 'df_time' is not indexed by Datetime.")
    if 'Processed_Message' not in df.columns:
        print("  - 'Processed_Message' column missing in main DataFrame 'df'.")
    if 'df_time' in locals() and 'Processed_Message' not in df_time.columns:
        print("  - 'Processed_Message' column missing in 'df_time' DataFrame.")


if any(plt.get_fignums()):
    print("\nDisplaying generated plots...")
    plt.show()
else:
    print("\nNo plots were generated to display.")

print("\n--- Analysis Complete ---")
print("Generated plots have been saved as PNG files in the script's directory and 'pain_point_plots' subdirectory.")