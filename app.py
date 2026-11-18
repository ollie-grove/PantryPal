
import streamlit as st
import pandas as pd
from datetime import date, timedelta

import database as db

from ai_recipes import generate_recipes

from io import BytesIO


def export_inventory_to_excel(items):
    columns = [
        "ID",
        "Name",
        "Location",
        "Quantity",
        "Unit",
        "Category",
        "Expiration Date",
        "Notes"
    ]

    df = pd.DataFrame(items, columns=columns)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Inventory")

    output.seek(0)

    return output.getvalue()


# Initialize application
st.set_page_config(
    page_title="PantryPal",
    page_icon="🥑",
    layout="wide"
)


st.markdown("""
<style>

/* =================================
   PANTRYPAL - COLOR PALETTE
   ================================= */

:root {
    --sage: #6B9080;
    --eucalyptus: #A4C3B2;
    --seafoam: #CCE3DE;
    --mist: #EAF4F4;
    --fresh: #F6FFF8;
    --text-dark: #263630;
    --text-muted: #62766D;
}

/* Main application background */
.stApp {
    background-color: var(--fresh);
    color: var(--text-dark);
}

/* Main content area */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* =================================
   SIDEBAR
   ================================= */

[data-testid="stSidebar"] {
    background-color: var(--sage);
}

[data-testid="stSidebar"] * {
    color: var(--fresh);
}

/* =================================
   HEADINGS AND TEXT
   ================================= */

h1, h2, h3 {
    color: var(--text-dark) !important;
    font-weight: 800 !important;
}

p, label {
    color: var(--text-dark);
}

/* =================================
   NAVIGATION TABS
   ================================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid var(--seafoam);
}

.stTabs [data-baseweb="tab"] {
    background-color: var(--mist);
    border-radius: 5px 5px 0 0;
    color: var(--text-dark);
    padding: 10px 18px;
}

.stTabs [aria-selected="true"] {
    background-color: var(--sage) !important;
    color: white !important;
}

/* =================================
   BUTTONS
   ================================= */

.stButton > button,
.stDownloadButton > button {
    background-color: var(--sage);
    color: white;
    border: 1px solid var(--sage);
    border-radius: 5px;
    font-weight: 700;
    transition: background-color 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #527765;
    color: white;
    border-color: #527765;
}

/* =================================
   METRIC CARDS
   ================================= */

[data-testid="stMetric"] {
    background-color: var(--seafoam);
    border: 1px solid var(--eucalyptus);
    border-radius: 6px;
    padding: 16px;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted);
}

[data-testid="stMetricValue"] {
    color: var(--text-dark);
}

/* =================================
   INPUT FIELDS
   ================================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: var(--mist);
    color: var(--text-dark);
    border-color: var(--eucalyptus);
}

.stSelectbox [data-baseweb="select"] {
    background-color: var(--mist);
}

/* Checkboxes */
.stCheckbox label {
    color: var(--text-dark);
}

/* =================================
   MASKING TAPE LABELS
   ================================= */

.tape-label {
    display: inline-block;
    background-color: var(--eucalyptus);
    color: var(--text-dark);
    padding: 7px 18px;
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 1px;
    transform: rotate(-1deg);
    box-shadow: 1px 2px 3px rgba(0,0,0,0.10);
    margin: 8px 0 16px 0;
}

/* Small kitchen labels */
.kitchen-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    color: var(--sage);
    text-transform: uppercase;
}

/* Inventory panels */
.storage-panel {
    background-color: var(--mist);
    border: 1px solid var(--seafoam);
    border-radius: 5px;
    padding: 18px;
    margin-bottom: 15px;
}

/* =================================
   DIVIDERS AND TABLES
   ================================= */

hr {
    border-color: var(--seafoam);
}

/* =================================
   ALERTS
   ================================= */

[data-testid="stAlert"] {
    border-radius: 5px;
}

/* =================================
   EXPANDERS
   ================================= */

[data-testid="stExpander"] {
    background-color: var(--mist);
    border: 1px solid var(--seafoam);
    border-radius: 5px;
}

</style>
""", unsafe_allow_html=True)


db.initialize_database()

# Load inventory
items = db.get_all_items()

# Convert database results into a DataFrame
columns = [
    "ID", "Name", "Location", "Quantity",
    "Unit", "Category", "Expiration Date", "Notes"
]

df = pd.DataFrame(items, columns=columns)

# Application header
st.title("🥑 PantryPal")
st.caption("Your kitchen, organized.")

# Navigation
dashboard, inventory, add_item, manage, recipe_generator, import_excel = st.tabs([
    "🏠 Dashboard",
    "📦 My Inventory",
    "➕ Add Item",
    "✏️ Manage Items",
    "🥞Recipe Generator",
    "🖇️Import Excel"
])

# -------------------------
# DASHBOARD
# -------------------------

with dashboard:
    st.markdown("""
    <div style="
        background-color: #25292B;
        padding: 28px;
        border-radius: 6px;
        margin-bottom: 25px;
        border-left: 8px solid #B94C35;
    ">
        <div style="
            color: #D6C18D;
            font-size: 12px;
            letter-spacing: 3px;
            font-weight: bold;
        ">
            BACK OF HOUSE / INVENTORY MANAGEMENT
        </div>
        <h1 style="
            color: #F0EDE5 !important;
            font-size: 42px;
            margin: 8px 0 0 0;
            letter-spacing: 2px;
        ">
            PANTRYPAL
        </h1>
        <div style="
            color: #AEB4B5;
            font-size: 14px;
            margin-top: 5px;
        ">
            KNOW YOUR STOCK. WASTE LESS. COOK MORE.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## TODAY'S PREP SHEET")
    st.caption("YOUR CURRENT KITCHEN INVENTORY")

    items = db.get_all_items()

    total_items = len(items)
    pantry_count = sum(1 for item in items if item[2] == "Pantry")
    fridge_count = sum(1 for item in items if item[2] == "Fridge")
    freezer_count = sum(1 for item in items if item[2] == "Freezer")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("TOTAL STOCK", total_items)
    col2.metric("DRY STORAGE", pantry_count)
    col3.metric("COLD STORAGE", fridge_count)
    col4.metric("FROZEN STOCK", freezer_count)

    st.divider()

    st.markdown("## ⚠️ USE FIRST")
    st.caption("INGREDIENTS APPROACHING THEIR EXPIRATION DATE")

    from datetime import date, timedelta

    today = date.today()
    upcoming_items = []

    for item in items:
        expiration = item[6]

        if expiration:
            try:
                expiration_date = date.fromisoformat(str(expiration))
                days_remaining = (expiration_date - today).days

                if 0 <= days_remaining <= 5:
                    upcoming_items.append((item, days_remaining))
            except ValueError:
                pass

    if upcoming_items:
        upcoming_items.sort(key=lambda x: x[1])

        for item, days_remaining in upcoming_items:
            if days_remaining == 0:
                urgency = "USE TODAY"
                color = "#B94C35"
            elif days_remaining == 1:
                urgency = "USE TOMORROW"
                color = "#C17A35"
            else:
                urgency = f"{days_remaining} DAYS LEFT"
                color = "#777D67"

            st.markdown(f"""
            <div style="
                background-color: #F3EBD8;
                border-left: 6px solid {color};
                padding: 14px 18px;
                margin-bottom: 10px;
                border-radius: 3px;
                box-shadow: 1px 2px 4px rgba(0,0,0,0.08);
            ">
                <div style="
                    font-size: 11px;
                    font-weight: bold;
                    letter-spacing: 2px;
                    color: {color};
                ">
                    {urgency}
                </div>
                <div style="
                    font-size: 20px;
                    font-weight: bold;
                    color: #25292B;
                    margin-top: 4px;
                ">
                    {item[1]}
                </div>
                <div style="
                    font-size: 13px;
                    color: #555;
                ">
                    {item[3]} {item[4]} &nbsp; / &nbsp; {item[2]}
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.success("ALL CLEAR — NO INGREDIENTS EXPIRING IN THE NEXT FIVE DAYS.")

    st.divider()

    st.markdown("## KITCHEN STATUS")
    st.caption("KEEP YOUR INVENTORY UP TO DATE.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("＋ ADD INGREDIENT", use_container_width=True):
            st.info("Head to the Add Item tab to stock your kitchen.")

    with col2:
        if st.button("VIEW INVENTORY", use_container_width=True):
            st.info("Head to My Inventory to review your stock.")


# -------------------------
# INVENTORY
# -------------------------


with inventory:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div class="tape-label">STOCK ROOM / INVENTORY LOG</div>
        <h2 style="margin-top: 8px;">What's in the Kitchen?</h2>
        <p style="color: #777D67; font-size: 13px;">
            CURRENT INGREDIENTS • STORAGE • QUANTITIES
        </p>
    </div>
    """, unsafe_allow_html=True); 

    if df.empty:
        st.info("No ingredients added yet. Your shelves are looking a little empty!")

    else:
        # Inventory counts
        pantry_count = len(df[df["Location"] == "Pantry"])
        fridge_count = len(df[df["Location"] == "Fridge"])
        freezer_count = len(df[df["Location"] == "Freezer"])

        col1, col2, col3 = st.columns(3)

        col1.metric("DRY STORAGE", pantry_count)
        col2.metric("WALK-IN / FRIDGE", fridge_count)
        col3.metric("FREEZER", freezer_count)

        st.divider()

        # Search and filters
        st.markdown("### FIND AN INGREDIENT")

        col1, col2 = st.columns([1, 2])

        with col1:
            selected_location = st.selectbox(
                "Storage location",
                ["All", "Pantry", "Fridge", "Freezer"]
            )

        with col2:
            search = st.text_input(
                "Search stock",
                placeholder="Search by ingredient name..."
            )

        filtered = df.copy()

        if selected_location != "All":
            filtered = filtered[
                filtered["Location"] == selected_location
            ]

        if search:
            filtered = filtered[
                filtered["Name"].str.contains(
                    search, case=False, na=False
                )
            ]

        st.divider()

        # Inventory list
        st.markdown("""
        <div class="tape-label">CURRENT STOCK</div>
        """, unsafe_allow_html=True)

        st.caption(
            f"SHOWING {len(filtered)} OF {len(df)} INGREDIENTS"
        )

        if filtered.empty:
            st.warning("No ingredients match your search.")
        else:
            st.dataframe(
                filtered.drop(columns=["ID", "Notes"]),
                hide_index=True,
                use_container_width=True
            )


# -------------------------
# ADD ITEM
# -------------------------



with add_item:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div class="tape-label">STOCK ROOM / NEW ITEM</div>
        <h2 style="margin-top: 8px;">Stock the Kitchen</h2>
        <p style="color: #777D67; font-size: 13px;">
            NEW INGREDIENT INTAKE • STORAGE LABEL • INVENTORY LOG
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### INGREDIENT INFORMATION")
    st.caption("ENTER THE DETAILS FOR YOUR NEW STOCK")

    name = st.text_input(
        "Ingredient Name",
        placeholder="e.g. Roma tomatoes"
    )

    col1, col2 = st.columns(2)

    with col1:
        location = st.selectbox(
            "Storage Location",
            ["Pantry", "Fridge", "Freezer"]
        )

    with col2:
        category = st.selectbox(
            "Ingredient Category",
            [
                "Produce",
                "Meat",
                "Dairy",
                "Grains",
                "Beans",
                "Nuts/Seeds",
                "Canned Goods",
                "Frozen",
                "Other"
            ]
        )

    st.divider()

    st.markdown("### STOCK QUANTITY")

    col1, col2 = st.columns(2)

    with col1:
        quantity = st.number_input(
            "Quantity",
            min_value=0.0,
            value=1.0
        )

    with col2:
        unit = st.text_input(
            "Unit",
            placeholder="lbs, cups, cans, etc."
        )

    st.divider()

    st.markdown("### EXPIRATION & PREP NOTES")

    has_expiration = st.checkbox(
        "I know the expiration date"
    )

    expiration = None

    if has_expiration:
        expiration = st.date_input(
            "Expiration Date",
            min_value=date.today(),
            value=date.today()
        )

    notes = st.text_area(
        "Prep Notes / Additional Information",
        placeholder="e.g. Opened Monday, stored in top shelf..."
    )

    st.divider()

    st.markdown("""
    <div style="
        background-color: #F3EBD8;
        border-left: 5px solid #D6C18D;
        padding: 12px 16px;
        margin-bottom: 15px;
        color: #25292B;
    ">
        <strong>NEW STOCK ENTRY</strong><br>
        <span style="font-size: 12px;">
            Double-check your ingredient details before adding it to inventory.
        </span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋ ADD TO INVENTORY", type="primary"):

        if not name.strip():
            st.error("Please enter an ingredient name.")

        elif not unit.strip():
            st.error("Please enter a unit.")

        else:
            db.add_item(
                name.strip(),
                location,
                quantity,
                unit.strip(),
                category,
                expiration.isoformat() if expiration else None,
                notes
            )

            st.success(f"{name} added to your inventory!")

            st.rerun()

# -------------------------
# MANAGE ITEMS
# -------------------------


# -------------------------
# MANAGE ITEMS
# -------------------------

with manage:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div class="tape-label">BACK OF HOUSE / STOCK CONTROL</div>
        <h2 style="margin-top: 8px;">Inventory Control</h2>
        <p style="color: #777D67; font-size: 13px;">
            EDIT STOCK • UPDATE STORAGE • REMOVE ITEMS
        </p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("Your inventory is empty. Add ingredients before managing stock.")

    else:
        st.markdown("### SELECT STOCK ITEM")

        item_options = {
            f"{row['Name']} — {row['Location']} (ID: {row['ID']})":
            int(row["ID"])
            for _, row in df.iterrows()
        }

        selected_label = st.selectbox(
            "Choose an ingredient to manage",
            list(item_options.keys())
        )

        selected_id = item_options[selected_label]
        selected_row = df[df["ID"] == selected_id].iloc[0]

        st.divider()

        st.markdown("""
        <div class="tape-label">EDIT INVENTORY LABEL</div>
        """, unsafe_allow_html=True)

        # Preserve existing units and categories
        units = [
            "items", "lbs", "oz", "g", "kg",
            "cups", "tbsp", "tsp", "liters",
            "gallons", "packages", "cans"
        ]

        current_unit = selected_row["Unit"]

        if current_unit not in units:
            units.append(current_unit)

        categories = [
            "Produce", "Meat", "Dairy", "Grains",
            "Beans", "Nuts/Seeds", "Canned Goods",
            "Frozen", "Frozen Foods", "Condiments",
            "Baking", "Other"
        ]

        current_category = selected_row["Category"]

        if pd.isna(current_category) or not current_category:
            current_category = "Other"

        if current_category not in categories:
            categories.append(current_category)

        with st.form("edit_ingredient"):

            edit_name = st.text_input(
                "Ingredient Name",
                value=selected_row["Name"]
            )

            col1, col2 = st.columns(2)

            with col1:
                edit_location = st.selectbox(
                    "Storage Location",
                    ["Pantry", "Fridge", "Freezer"],
                    index=["Pantry", "Fridge", "Freezer"].index(
                        selected_row["Location"]
                    )
                )

            with col2:
                edit_category = st.selectbox(
                    "Category",
                    categories,
                    index=categories.index(current_category)
                )

            col1, col2 = st.columns(2)

            with col1:
                edit_quantity = st.number_input(
                    "Quantity",
                    min_value=0.01,
                    value=max(0.01, float(selected_row["Quantity"]))
                )

            with col2:
                edit_unit = st.selectbox(
                    "Unit",
                    units,
                    index=units.index(current_unit)
                )

            current_expiration = selected_row["Expiration Date"]

            if pd.isna(current_expiration):
                current_expiration = None

            has_edit_expiration = st.checkbox(
                "Track expiration date",
                value=bool(current_expiration)
            )

            edit_expiration = None

            if has_edit_expiration:
                default_date = (
                    date.fromisoformat(str(current_expiration))
                    if current_expiration
                    else date.today()
                )

                edit_expiration = st.date_input(
                    "Expiration Date",
                    value=default_date
                )

            edit_notes = st.text_area(
                "Prep Notes / Additional Information",
                value=selected_row["Notes"] or ""
            )

            save = st.form_submit_button(
                "SAVE INVENTORY CHANGES",
                use_container_width=True
            )

            if save:
                if not edit_name.strip():
                    st.error("Ingredient name cannot be empty.")

                else:
                    db.update_item(
                        selected_id,
                        edit_name.strip(),
                        edit_location,
                        edit_quantity,
                        edit_unit,
                        edit_category,
                        edit_expiration.isoformat()
                        if edit_expiration else None,
                        edit_notes.strip()
                    )

                    st.success("Inventory updated successfully!")
                    st.rerun()

        st.divider()

        st.markdown("""
        <div class="tape-label">REMOVE FROM STOCK</div>
        """, unsafe_allow_html=True)

        st.warning(
            f"You are managing: {selected_row['Name']} "
            f"({selected_row['Location']})"
        )

        if st.button("DELETE SELECTED INGREDIENT", type="secondary"):
            db.delete_item(selected_id)
            st.success("Ingredient removed from inventory!")
            st.rerun()



# -----------------------------
# RECIPE GENERATOR
# -----------------------------


with recipe_generator:
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <div class="tape-label">KITCHEN / RECIPE FILE</div>
        <h2 style="margin-top: 8px;">What's Cooking?</h2>
        <p style="color: #777D67; font-size: 13px;">
            DAILY SPECIALS • INVENTORY-INSPIRED • MADE TO ORDER
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### RECIPE PARAMETERS")
    st.caption("SET YOUR PORTIONS AND AVAILABLE STOCK")

    col1, col2 = st.columns(2)

    with col1:
        servings = st.selectbox(
            "Number of servings",
            [1, 2, 4, 6, 8],
            index=1
        )

    with col2:
        max_extra = st.selectbox(
            "Maximum additional ingredients",
            [0, 1, 2, 3, 5],
            index=2
        )

    st.divider()

    st.markdown("""
    <div class="tape-label">FROM THE RECIPE BOX</div>
    """, unsafe_allow_html=True)

    if st.button("GENERATE RECIPES", type="primary"):

        if not items:
            st.warning(
                "Your inventory is empty. Stock the kitchen first!"
            )

        else:
            with st.spinner("Working the kitchen..."):

                try:
                    recipes = generate_recipes(
                        items,
                        servings=servings,
                        max_extra_ingredients=max_extra
                    )

                    st.markdown("""
                    <div style="
                        background-color: #F3EBD8;
                        border: 1px solid #C6BDAA;
                        border-left: 7px solid #B94C35;
                        padding: 16px 20px;
                        margin: 20px 0 12px 0;
                        box-shadow: 2px 3px 5px rgba(0,0,0,0.10);
                    ">
                        <div style="
                            font-size: 11px;
                            letter-spacing: 3px;
                            font-weight: bold;
                            color: #777D67;
                        ">
                            PANTRYPAL / KITCHEN NOTES
                        </div>
                        <div style="
                            font-size: 24px;
                            font-weight: bold;
                            color: #25292B;
                            margin-top: 5px;
                        ">
                            Today's Recipe Suggestions
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(recipes)

                except Exception as e:
                    st.error(
                        f"Something went wrong while generating recipes: {e}"
                    )



# -----------------------------
# EXCEL IMPORT
# -----------------------------

with import_excel:

    st.subheader("Export Your Inventory")

    current_items = db.get_all_items()

    if current_items:
        excel_file = export_inventory_to_excel(current_items)

        st.download_button(
            label="Download Inventory as Excel",
            data=excel_file,
            file_name="pantrypal_inventory.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
    else:
        st.info("Your inventory is empty. Add ingredients before exporting.")

    if "excel_import_message" in st.session_state:
        st.success(st.session_state.pop("excel_import_message")),
        st.header("Import Inventory from Excel")

        st.write(
            "Upload an Excel spreadsheet to add multiple ingredients to your PantryPal inventory."
    )

    # Create a downloadable Excel template
    template = pd.DataFrame(columns=[
        "Name",
        "Location",
        "Quantity",
        "Unit",
        "Category",
        "Expiration Date",
        "Notes"
    ])

    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        template.to_excel(
            writer,
            index=False,
            sheet_name="Inventory"
        )

    st.download_button(
        label="Download Excel Template",
        data=excel_buffer.getvalue(),
        file_name="pantrypal_inventory_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.divider()

    # Upload spreadsheet
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=["xlsx"]
    )

    if uploaded_file is not None:

        try:
            df = pd.read_excel(uploaded_file)

            # Normalize column names
            df.columns = [
                str(column).strip().lower()
                for column in df.columns
            ]

            # Required columns
            required_columns = [
                "name",
                "location",
                "quantity",
                "unit"
            ]

            missing_columns = [
                column for column in required_columns
                if column not in df.columns
            ]

            if missing_columns:
                st.error(
                    "Your spreadsheet is missing these required columns: "
                    + ", ".join(missing_columns)
                )

            else:
                # Add optional columns if they are missing
                optional_columns = [
                    "category",
                    "expiration date",
                    "notes"
                ]

                for column in optional_columns:
                    if column not in df.columns:
                        df[column] = None

                st.subheader("Spreadsheet Preview")
                st.dataframe(df, use_container_width=True)

                valid_records = []
                errors = []
                existing_keys = set()
                seen_keys = set()
                duplicate_count = 0

                # Check existing inventory for duplicates
                existing_items = db.get_all_items()

                def make_key(
                    name, location, quantity, unit,
                    category, expiration, notes
                ):
                    return (
                        name.strip().casefold(),
                        location.strip().casefold(),
                        round(float(quantity), 6),
                        unit.strip().casefold(),
                        (category or "").strip().casefold(),
                        expiration or "",
                        (notes or "").strip().casefold()
                    )

                for item in existing_items:
                    existing_keys.add(
                        make_key(
                            item[1],
                            item[2],
                            item[3],
                            item[4],
                            item[5] or "",
                            item[6] or "",
                            item[7] or ""
                        )
                    )

                # Validate each spreadsheet row
                for index, row in df.iterrows():

                    excel_row = index + 2

                    try:
                        name = (
                            "" if pd.isna(row["name"])
                            else str(row["name"]).strip()
                        )

                        location_value = (
                            "" if pd.isna(row["location"])
                            else str(row["location"]).strip()
                        )

                        unit = (
                            "" if pd.isna(row["unit"])
                            else str(row["unit"]).strip()
                        )

                        if not name:
                            raise ValueError("Ingredient name is missing.")

                        if not unit:
                            raise ValueError("Unit is missing.")

                        locations = {
                            "pantry": "Pantry",
                            "fridge": "Fridge",
                            "freezer": "Freezer"
                        }

                        location = locations.get(
                            location_value.casefold()
                        )

                        if not location:
                            raise ValueError(
                                "Location must be Pantry, Fridge, or Freezer."
                            )

                        quantity = float(row["quantity"])

                        if not pd.notna(quantity) or quantity <= 0:
                            raise ValueError(
                                "Quantity must be greater than zero."
                            )

                        category_value = row["category"]

                        category = (
                            "" if pd.isna(category_value)
                            else str(category_value).strip()
                        )

                        notes_value = row["notes"]

                        notes = (
                            "" if pd.isna(notes_value)
                            else str(notes_value).strip()
                        )

                        # Convert Excel dates into ISO date strings
                        expiration_value = row["expiration date"]

                        if pd.isna(expiration_value):
                            expiration = None
                        else:
                            parsed_date = pd.to_datetime(
                                expiration_value,
                                errors="coerce"
                            )

                            if pd.isna(parsed_date):
                                raise ValueError(
                                    "Expiration date is invalid."
                                )

                            expiration = parsed_date.date().isoformat()

                        # Check for duplicate records
                        record_key = make_key(
                            name,
                            location,
                            quantity,
                            unit,
                            category,
                            expiration,
                            notes
                        )

                        if (
                            record_key in existing_keys
                            or record_key in seen_keys
                        ):
                            duplicate_count += 1
                            continue

                        seen_keys.add(record_key)

                        valid_records.append((
                            name,
                            location,
                            quantity,
                            unit,
                            category,
                            expiration,
                            notes
                        ))

                    except (ValueError, TypeError) as error:
                        errors.append({
                            "Excel Row": excel_row,
                            "Ingredient": str(row["name"]),
                            "Problem": str(error)
                        })

                # Display import summary
                st.divider()
                st.subheader("Import Summary")

                col1, col2, col3 = st.columns(3)

                col1.metric("Valid Ingredients", len(valid_records))
                col2.metric("Duplicates Skipped", duplicate_count)
                col3.metric("Rows With Errors", len(errors))

                if errors:
                    st.warning(
                        "Some rows need attention before they can be imported."
                    )

                    st.dataframe(
                        pd.DataFrame(errors),
                        use_container_width=True
                    )

                if valid_records:

                    if st.button(
                        f"Import {len(valid_records)} Ingredients",
                        type="primary"
                    ):

                        for record in valid_records:
                            db.add_item(*record)

                        st.session_state["excel_import_message"] = (
                            f"Successfully imported {len(valid_records)} ingredients!"
                        )

                        st.rerun()

                elif not errors:
                    st.info(
                        "No new ingredients to import."
                    )

        except Exception as error:
            st.error(
                f"Unable to read this Excel file: {error}"
            )
