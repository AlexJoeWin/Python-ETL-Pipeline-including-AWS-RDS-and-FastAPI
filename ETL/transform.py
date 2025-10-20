# TRANSFORM FUNCTION
import logging

def transform(raw_data):
    # Raise error in case NaNs overwhelm
    miss_ratio_mask = raw_data.isna().sum() / raw_data.shape[0]
    aff_data = raw_data.loc[:, miss_ratio_mask > 0.4]
    if aff_data.shape[1] != 0:
        logging.warning(f"Data lacking. Affected features: {aff_data.columns}\n")

    # Dropping rows with multiple missing values
    mask = raw_data.isna().sum(axis=1) > 2
    drop_rows = raw_data.loc[mask]
    if drop_rows.shape[0] != 0:
        raw_data = raw_data.drop(drop_rows.index)
        logging.info(f"Number of rows to be dropped: {len(drop_rows)}.")
        logging.debug(f"Rows to be dropped: {drop_rows}\n")

    # Fill NaNs with previous value
    for c in raw_data.columns:
        raw_data[c] = raw_data[c].ffill()

    if raw_data.isna().any().any() == False:
        logging.info(f"No missing values.\n")
    else:
        logging.warning(f"Values are still missing.\n")

    # Double checking data types
    count = 0
    for c in raw_data.columns:
        prop = raw_data[c].apply(type).unique()
        if len(prop) > 1:
            logging.warning(f"{c} is compromised: {prop}\n")
            count += 1
        else:
            continue

    cleaned_data = raw_data
    del raw_data
    return cleaned_data