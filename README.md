# 📊 Indonesian Premium Rice Price Scraper (per Province)

This Python script is used to **scrape the average geometric price of Premium Rice** across all provinces in Indonesia, using data from the [National Food Price Panel](https://panelharga.badanpangan.go.id/). The data is stored in a `.csv` file for further analysis, visualization, or documentation.

---

## 🧠 Key Features

- ✅ Automatically fetches data from the API: `https://api-panelhargav2.badanpangan.go.id`
- 📆 Adjusts the time range from the past 3 years up to today
- 📌 Collects daily price data for 39 provinces of indonesia
- 🔁 Ensures provinces with no data still appear in the dataset (as `NaN`)
- 💾 Appends results into a persistent CSV file: `harga_beras_premium.csv`

---

## ⚠️ WARNING: Use with Caution – Connection May Be Interrupted

> **Please be cautious when running this script!**

### Reason:
- The government API enforces a **rate limit** (HTTP status **429**) if too many requests are sent in a short time.
- If your internet connection is unstable, the script may **fail to fetch data** or return non-JSON responses.
- Some provinces might not report data for certain dates.
- While automatic delays (`time.sleep`) are included, **using public Wi-Fi, VPNs, or unstable connections can worsen reliability**.

---

## 📂 Output File Structure

After running the script, a file named `harga_beras_premium.csv` will be created or updated, with the following structure:

| Date       | Commodity      | Province             | Price     |
|------------|----------------|----------------------|-----------|
| 01/01/2022 | Premium Rice   | Central Java         | 12450.0   |
| 01/01/2022 | DKI Jakarta    | NaN                  | NaN       |
| ...        | ...            | ...                  | ...       |

Note: `Price` will be `NaN` if no data is available for that date.

---

## ▶️ How to Run

### Requirements

Make sure you have:

- Python 3.x
- Libraries: `requests`, `pandas`, `numpy`

### Install dependencies:

```bash
pip install requests pandas numpy
