from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# 1. APPLICATION CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Cognifyz | Location Analytics",
    page_icon="📍",
    layout="wide",
)

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

st.title("📍 Cognifyz Restaurant Location Analytics")

st.markdown(
    """
    Explore restaurant locations, ratings, cuisines, costs,
    and geographical distribution through an interactive dashboard.
    """
)


# --------------------------------------------------
# 2. COLUMN DETECTION
# --------------------------------------------------

def normalize_column(column):
    return (
        str(column)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )


COLUMN_ALIASES = {
    "name": [
        "restaurant name",
        "name",
        "restaurant",
    ],
    "city": [
        "city",
        "city name",
    ],
    "locality": [
        "locality",
        "area",
        "neighborhood",
        "neighbourhood",
    ],
    "latitude": [
        "latitude",
        "lat",
    ],
    "longitude": [
        "longitude",
        "long",
        "lon",
        "lng",
    ],
    "rating": [
        "aggregate rating",
        "rating",
        "rate",
    ],
    "cuisines": [
        "cuisines",
        "cuisine",
    ],
    "cost": [
        "average cost for two",
        "average cost",
        "cost for two",
        "cost",
    ],
    "price_range": [
        "price range",
        "price category",
    ],
}


def detect_columns(dataframe):
    normalized = {
        normalize_column(column): column
        for column in dataframe.columns
    }

    detected = {}

    for field, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized:
                detected[field] = normalized[alias]
                break

    return detected


# --------------------------------------------------
# 3. LOAD THE REAL DATASET
# --------------------------------------------------

@st.cache_data
def load_dataset(file_path, modified_time):
    return pd.read_csv(
        file_path,
        encoding="utf-8-sig",
    )


csv_files = sorted(DATA_DIR.glob("*.csv"))

if not csv_files:
    st.error(
        "No CSV dataset found. Place your restaurant dataset "
        "inside the project's data folder."
    )
    st.stop()

# Prefer a filename containing "dataset" if several CSVs exist.
preferred_files = [
    file
    for file in csv_files
    if "dataset" in file.stem.lower()
]

dataset_path = (
    preferred_files[0]
    if preferred_files
    else csv_files[0]
)

df = load_dataset(
    str(dataset_path),
    dataset_path.stat().st_mtime,
)

columns = detect_columns(df)

if (
    "latitude" not in columns
    or "longitude" not in columns
):
    st.error(
        "Latitude or longitude was not detected. "
        "Check your CSV column names."
    )

    st.write("Available columns:", df.columns.tolist())
    st.stop()


# --------------------------------------------------
# 4. PREPARE DATA
# --------------------------------------------------

latitude_col = columns["latitude"]
longitude_col = columns["longitude"]

for field in [
    "latitude",
    "longitude",
    "rating",
    "cost",
    "price_range",
]:
    column = columns.get(field)

    if column:
        df[column] = pd.to_numeric(
            df[column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip(),
            errors="coerce",
        )

rating_col = columns.get("rating")
cost_col = columns.get("cost")
price_col = columns.get("price_range")
city_col = columns.get("city")
locality_col = columns.get("locality")
cuisine_col = columns.get("cuisines")
name_col = columns.get("name")

if rating_col:
    df.loc[
        ~df[rating_col].between(0, 5),
        rating_col,
    ] = float("nan")

valid_coordinates = (
    df[latitude_col].between(-90, 90)
    & df[longitude_col].between(-180, 180)
)

map_data = df.loc[valid_coordinates].copy()

st.sidebar.header("🔎 Dashboard Filters")

st.sidebar.caption(
    f"Dataset: {dataset_path.name}"
)


# --------------------------------------------------
# 5. CITY FILTER
# --------------------------------------------------

if city_col:
    cities = sorted(
        df[city_col].dropna().astype(str).unique()
    )

    selected_cities = st.sidebar.multiselect(
        "Select cities",
        options=cities,
        default=[],
    )
else:
    selected_cities = []


# --------------------------------------------------
# 6. LOCALITY FILTER
# --------------------------------------------------

filtered_df = df.copy()

if selected_cities and city_col:
    filtered_df = filtered_df[
        filtered_df[city_col]
        .astype(str)
        .isin(selected_cities)
    ]

if locality_col:
    localities = sorted(
        filtered_df[locality_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_localities = st.sidebar.multiselect(
        "Select localities",
        options=localities,
        default=[],
    )

    if selected_localities:
        filtered_df = filtered_df[
            filtered_df[locality_col]
            .astype(str)
            .isin(selected_localities)
        ]


# --------------------------------------------------
# 7. CUISINE FILTER
# --------------------------------------------------

if cuisine_col:
    cuisines = sorted(
        filtered_df[cuisine_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_cuisines = st.sidebar.multiselect(
        "Select cuisines",
        options=cuisines,
        default=[],
    )

    if selected_cuisines:
        pattern = "|".join(
            pd.Series(selected_cuisines)
            .str.replace(r"([.^$*+?{}\[\]\\|()])", r"\\\1", regex=True)
            .tolist()
        )

        filtered_df = filtered_df[
            filtered_df[cuisine_col]
            .astype(str)
            .str.contains(
                pattern,
                case=False,
                regex=True,
                na=False,
            )
        ]


# --------------------------------------------------
# 8. RATING FILTER
# --------------------------------------------------

if rating_col:
    rating_values = filtered_df[rating_col].dropna()

    if not rating_values.empty:
        minimum_rating = float(rating_values.min())
        maximum_rating = float(rating_values.max())

        if minimum_rating < maximum_rating:
            selected_rating = st.sidebar.slider(
                "Minimum restaurant rating",
                min_value=minimum_rating,
                max_value=maximum_rating,
                value=minimum_rating,
            )

            filtered_df = filtered_df[
                filtered_df[rating_col] >= selected_rating
            ]


# --------------------------------------------------
# 9. COST FILTER
# --------------------------------------------------

if cost_col:
    cost_values = filtered_df[cost_col].dropna()

    if not cost_values.empty:
        minimum_cost = float(cost_values.min())
        maximum_cost = float(cost_values.max())

        if minimum_cost < maximum_cost:
            cost_range = st.sidebar.slider(
                "Average cost range",
                min_value=minimum_cost,
                max_value=maximum_cost,
                value=(minimum_cost, maximum_cost),
            )

            filtered_df = filtered_df[
                filtered_df[cost_col].between(
                    cost_range[0],
                    cost_range[1],
                )
            ]


# --------------------------------------------------
# 10. FILTER MAP DATA
# --------------------------------------------------

filtered_map = filtered_df.loc[
    filtered_df[latitude_col].between(-90, 90)
    & filtered_df[longitude_col].between(-180, 180)
].copy()


# --------------------------------------------------
# 11. KEY PERFORMANCE INDICATORS
# --------------------------------------------------

total_restaurants = len(filtered_df)

average_rating = (
    filtered_df[rating_col].mean()
    if rating_col
    else None
)

unique_cities = (
    filtered_df[city_col].nunique()
    if city_col
    else None
)

restaurants_mapped = len(filtered_map)

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Restaurants",
    f"{total_restaurants:,}",
)

metric2.metric(
    "Average Rating",
    f"{average_rating:.2f}/5"
    if pd.notna(average_rating)
    else "N/A",
)

metric3.metric(
    "Cities",
    f"{unique_cities:,}"
    if unique_cities is not None
    else "N/A",
)

metric4.metric(
    "Mapped Restaurants",
    f"{restaurants_mapped:,}",
)


# --------------------------------------------------
# 12. GEOGRAPHICAL MAP
# --------------------------------------------------

st.subheader("🗺️ Restaurant Geographical Distribution")

if filtered_map.empty:
    st.warning(
        "No restaurants with valid coordinates match "
        "the selected filters."
    )
else:
    hover_columns = [
        column
        for column in [
            name_col,
            city_col,
            locality_col,
            rating_col,
            cuisine_col,
            cost_col,
        ]
        if column and column in filtered_map.columns
    ]

    map_arguments = {
        "data_frame": filtered_map,
        "lat": latitude_col,
        "lon": longitude_col,
        "hover_data": hover_columns,
        "zoom": 3,
        "height": 600,
        "map_style": "open-street-map",
    }

    if name_col:
        map_arguments["hover_name"] = name_col

    if rating_col:
        map_arguments["color"] = rating_col
        map_arguments["color_continuous_scale"] = "RdYlGn"

    map_fig = px.scatter_map(**map_arguments)

    map_fig.update_traces(
        marker={
            "size": 8,
            "opacity": 0.7,
        }
    )

    map_fig.update_layout(
        margin={
            "l": 0,
            "r": 0,
            "t": 20,
            "b": 0,
        }
    )

    st.plotly_chart(
        map_fig,
        use_container_width=True,
    )


# --------------------------------------------------
# 13. CITY ANALYSIS
# --------------------------------------------------

st.subheader("🏙️ City Analysis")

if city_col:
    city_counts = (
        filtered_df[city_col]
        .dropna()
        .value_counts()
        .head(15)
        .sort_values()
    )

    if not city_counts.empty:
        city_fig = px.bar(
            x=city_counts.values,
            y=city_counts.index,
            orientation="h",
            labels={
                "x": "Restaurant Count",
                "y": "City",
            },
            title="Top Cities by Restaurant Count",
        )

        st.plotly_chart(
            city_fig,
            use_container_width=True,
        )

        if rating_col:
            city_ratings = (
                filtered_df
                .dropna(subset=[city_col, rating_col])
                .groupby(city_col)[rating_col]
                .agg(
                    Average_Rating="mean",
                    Rated_Restaurants="count",
                )
                .reset_index()
            )

            city_ratings = city_ratings[
                city_ratings["Rated_Restaurants"] >= 3
            ]

            city_ratings = city_ratings.sort_values(
                "Average_Rating",
                ascending=False,
            )

            st.markdown("**City-wise Rating Summary**")

            st.dataframe(
                city_ratings,
                use_container_width=True,
            )


# --------------------------------------------------
# 14. LOCALITY ANALYSIS
# --------------------------------------------------

st.subheader("📍 Locality Analysis")

if locality_col:
    aggregation = {
        "Restaurant_Count": (locality_col, "size"),
    }

    if rating_col:
        aggregation["Average_Rating"] = (
            rating_col,
            "mean",
        )

    if cost_col:
        aggregation["Average_Cost"] = (
            cost_col,
            "mean",
        )

    locality_summary = (
        filtered_df
        .dropna(subset=[locality_col])
        .groupby(locality_col)
        .agg(**aggregation)
        .reset_index()
        .sort_values(
            "Restaurant_Count",
            ascending=False,
        )
    )

    st.dataframe(
        locality_summary.head(20),
        use_container_width=True,
    )


# --------------------------------------------------
# 15. CUISINE ANALYSIS
# --------------------------------------------------

st.subheader("🍽️ Cuisine Analysis")

if cuisine_col:
    cuisine_counts = (
        filtered_df[cuisine_col]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    cuisine_counts = cuisine_counts[
        cuisine_counts.ne("")
    ]

    cuisine_summary = (
        cuisine_counts
        .value_counts()
        .head(15)
        .sort_values()
    )

    if not cuisine_summary.empty:
        cuisine_fig = px.bar(
            x=cuisine_summary.values,
            y=cuisine_summary.index,
            orientation="h",
            labels={
                "x": "Restaurant Count",
                "y": "Cuisine",
            },
            title="Most Common Cuisines",
        )

        st.plotly_chart(
            cuisine_fig,
            use_container_width=True,
        )


# --------------------------------------------------
# 16. PRICE ANALYSIS
# --------------------------------------------------

st.subheader("💰 Cost Analysis")

if cost_col:
    cost_data = filtered_df[cost_col].dropna()

    if not cost_data.empty:
        cost_fig = px.histogram(
            x=cost_data,
            nbins=25,
            labels={
                "x": "Average Cost",
                "y": "Restaurant Count",
            },
            title="Distribution of Restaurant Costs",
        )

        st.plotly_chart(
            cost_fig,
            use_container_width=True,
        )

        st.write(
            f"Mean average cost: {cost_data.mean():,.2f}"
        )

        st.write(
            f"Median average cost: {cost_data.median():,.2f}"
        )


# --------------------------------------------------
# 17. RATING DISTRIBUTION
# --------------------------------------------------

st.subheader("⭐ Rating Distribution")

if rating_col:
    ratings = filtered_df[rating_col].dropna()

    if not ratings.empty:
        rating_fig = px.histogram(
            ratings,
            x=rating_col,
            nbins=20,
            title="Distribution of Restaurant Ratings",
            labels={
                rating_col: "Rating",
                "count": "Restaurant Count",
            },
        )

        st.plotly_chart(
            rating_fig,
            use_container_width=True,
        )


# --------------------------------------------------
# 18. INSIGHTS
# --------------------------------------------------

st.subheader("💡 Key Insights")

if total_restaurants == 0:
    st.info("No restaurants match the selected filters.")
else:
    st.write(
        f"**Restaurants matching filters:** "
        f"{total_restaurants:,}"
    )

    st.write(
        f"**Restaurants available on the map:** "
        f"{restaurants_mapped:,}"
    )

    if city_col:
        city_counts_all = filtered_df[city_col].value_counts()

        if not city_counts_all.empty:
            st.write(
                f"**City with the most restaurants in the "
                f"filtered dataset:** {city_counts_all.index[0]}"
            )

    if locality_col:
        locality_counts_all = (
            filtered_df[locality_col].value_counts()
        )

        if not locality_counts_all.empty:
            st.write(
                f"**Locality with the most restaurants in "
                f"the filtered dataset:** "
                f"{locality_counts_all.index[0]}"
            )

    if rating_col and pd.notna(average_rating):
        st.write(
            f"**Average rating of filtered restaurants:** "
            f"{average_rating:.2f}/5"
        )


# --------------------------------------------------
# 19. DOWNLOAD REPORTS
# --------------------------------------------------

st.subheader("📥 Download Reports")

csv_bytes = filtered_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="Download Filtered Restaurant Data",
    data=csv_bytes,
    file_name="filtered_restaurant_data.csv",
    mime="text/csv",
)

if city_col:
    downloadable_city_summary = (
        filtered_df
        .dropna(subset=[city_col])
        .groupby(city_col)
        .size()
        .reset_index(name="Restaurant Count")
    )

    st.download_button(
        label="Download City Analysis",
        data=downloadable_city_summary.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="city_analysis.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# 20. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Cognifyz Technologies | Task 4: Location-Based Analysis"
)

st.caption(
    f"Loaded {len(df):,} records from {dataset_path.name}."
)