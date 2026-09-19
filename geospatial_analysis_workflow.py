# Geospatial Data Analysis — reproducible workflow
import pandas as pd
import folium
from folium.plugins import MarkerCluster

df = pd.read_csv("illustrative_regional_sales_data.csv")

# Aggregate
state_summary = (df.groupby("State", as_index=False)
    .agg(Users=("Users","sum"), Orders=("Orders","sum"),
         RevenueINR=("RevenueINR","sum"), Cities=("City","count")))
state_summary["RevenuePerUserINR"] = state_summary["RevenueINR"] / state_summary["Users"]
state_summary["DemandIndex"] = state_summary["Users"] + 2*state_summary["Orders"]
state_summary["UnderservedScore"] = state_summary["DemandIndex"] / state_summary["RevenueINR"] * 1e6

# Top 3 opportunity candidates
top3 = df.sort_values("UnderservedScore", ascending=False).head(3)
print(top3[["City","State","Users","Orders","RevenueINR","UnderservedScore"]])

# Interactive map
m = folium.Map(location=[22.5,79.0], zoom_start=5, tiles="CartoDB positron")
cluster = MarkerCluster().add_to(m)
for _, r in df.iterrows():
    folium.CircleMarker(
        [r.Latitude, r.Longitude],
        radius=7,
        popup=f"{r.City}, {r.State} | Revenue ₹{r.RevenueINR:,.0f}",
        fill=True, fill_opacity=0.7
    ).add_to(cluster)

m.save("geospatial_sales_interactive_map.html")
