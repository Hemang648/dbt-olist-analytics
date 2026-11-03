# License and attribution for the files in this folder

The CSV files in `ci_data/` are a **modified subset** of the *Brazilian E-Commerce Public Dataset by Olist*, published on Kaggle. They are used only to run automated tests in CI.

- **Original dataset:** Brazilian E-Commerce Public Dataset by Olist (Kaggle). Confirm the exact title and link on the dataset page.
- **Original license:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0), https://creativecommons.org/licenses/by-nc-sa/4.0/
- **Changes made:** a deterministic sample of about 3,000 orders was selected, along with the customers, items, payments, reviews, products and sellers linked to those orders. Geolocation was reduced to a few rows per zip code prefix. No values were altered. The script that produces the sample is `scripts/make_ci_sample.py`.

## License of these files

Because these files are adapted from a ShareAlike-licensed dataset, they are shared under the same license: **CC BY-NC-SA 4.0**.

- **Attribution:** credit Olist as the source, link to the license, and note that the data was modified.
- **NonCommercial:** do not use these files for commercial purposes.
- **ShareAlike:** if you build on these files, share your contribution under the same license.

The dbt code in this repository is separate from the data and may be licensed differently (see the repository root).

This is a plain-language summary, not legal advice. The full license text is at the link above.